from datetime import timedelta
import time
from django.shortcuts import render, redirect
import logging
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm

from .models import Usuario, OTP

logger = logging.getLogger("accounts")


def registro_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()

        if not first_name or not last_name or not email:
            messages.error(request, "Preencha nome e email.")
            return render(request, "accounts/registro.html")

        # Evita enumeração: não informa se já existe, apenas cria/usa usuário inativo
        user = Usuario.objects.filter(email=email).first()
        if not user:
            user = Usuario.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=False,
            )
            logger.info("Usuário criado inativo para registro: %s", user.email)
        else:
            logger.info("Registro solicitado para email já existente (inativo ou ativo): %s", user.email)

        # Invalida OTPs anteriores e cria um novo
        OTP.objects.filter(user=user, tipo=OTP.OTPType.REGISTRO, usado=False).update(usado=True)
        otp = OTP.objects.create(
            user=user,
            code=_gerar_codigo_otp(),
            expira_em=timezone.now() + timedelta(minutes=10),
            tipo=OTP.OTPType.REGISTRO,
        )

        # Envia email com OTP no console
        send_mail(
            subject="Seu código OTP",
            message=f"Seu OTP é: {otp.code}",
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
        logger.info("OTP gerado e enviado para %s | otp_id=%s expira_em=%s", user.email, otp.id, otp.expira_em)
        # Guarda email na sessão para confirmação do OTP
        request.session["pending_email"] = email
        # Metadados de sessão para rate-limit/expiração do fluxo
        request.session["pending_set_at"] = int(time.time())
        request.session.pop("otp_attempts", None)
        request.session.pop("otp_window_started_at", None)
        messages.success(request, "Verifique seu e-mail para obter o código OTP.")
        return redirect(reverse("accounts:confirmar_otp"))

    return render(request, "accounts/registro.html")


def confirmar_otp_view(request: HttpRequest) -> HttpResponse:
    pending_email = request.session.get("pending_email")
    if not pending_email:
        messages.error(request, "Sessão expirada. Faça o registro novamente.")
        logger.warning("Sessão expirada em confirmar_otp sem pending_email")
        return redirect(reverse("accounts:registro"))

    # Expira sessão após 30 minutos
    set_at = request.session.get("pending_set_at")
    if isinstance(set_at, int) and (int(time.time()) - set_at) > 30 * 60:
        for k in ("pending_email", "pending_set_at", "otp_attempts", "otp_window_started_at"):
            request.session.pop(k, None)
        messages.error(request, "Sessão expirada. Faça o registro novamente.")
        return redirect(reverse("accounts:registro"))

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        # Rate limit: 5 tentativas a cada 5 minutos
        attempts = int(request.session.get("otp_attempts", 0))
        win_start = int(request.session.get("otp_window_started_at", int(time.time())))
        now_i = int(time.time())
        if (now_i - win_start) > 5 * 60:
            attempts = 0
            win_start = now_i
        if attempts >= 5:
            messages.error(request, "Muitas tentativas. Aguarde alguns minutos e tente novamente.")
            request.session["otp_attempts"] = attempts
            request.session["otp_window_started_at"] = win_start
            return render(request, "accounts/confirmar_otp.html")
        try:
            user = Usuario.objects.get(email=pending_email)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            logger.warning("Usuário não encontrado ao confirmar OTP: %s", pending_email)
            return render(request, "accounts/confirmar_otp.html")

        otp = (
            OTP.objects.filter(user=user, code=code, tipo=OTP.OTPType.REGISTRO, usado=False)
            .order_by("-criado_em")
            .first()
        )
        if not otp or not otp.esta_valido():
            attempts += 1
            request.session["otp_attempts"] = attempts
            request.session["otp_window_started_at"] = win_start
            messages.error(request, "OTP inválido ou expirado. Você pode solicitar um novo código.")
            logger.warning("OTP inválido/expirado | email=%s tentativas=%s", user.email, attempts)
            return render(request, "accounts/confirmar_otp.html")

        otp.marcar_usado()
        user.is_active = True
        user.save(update_fields=["is_active"])
        logger.info("Usuário ativado via OTP: %s", user.email)
        # Reseta contadores após sucesso
        request.session.pop("otp_attempts", None)
        request.session.pop("otp_window_started_at", None)
        return redirect(reverse("accounts:definir_senha"))

    return render(request, "accounts/confirmar_otp.html")


def ativar_view(request: HttpRequest) -> HttpResponse:
    token = request.GET.get("t")
    if token:
        try:
            data = signing.loads(token, max_age=60 * 30)  # 30 minutos
            if data.get("purpose") != "ativacao":
                raise signing.BadSignature
            email = data.get("email", "")
            user = Usuario.objects.get(email=email)
        except (signing.BadSignature, signing.SignatureExpired, Usuario.DoesNotExist):
            messages.error(request, "Link de ativação inválido ou expirado.")
            return render(request, "accounts/ativar.html")

        user.is_active = True
        user.save(update_fields=["is_active"])
        return redirect(reverse("accounts:definir_senha"))

    # Mantido por compatibilidade; no novo fluxo, ativação ocorre na confirmação do OTP
    return render(request, "accounts/ativar.html")


def definir_senha_view(request: HttpRequest) -> HttpResponse:
    pending_email = request.session.get("pending_email")
    if not pending_email:
        messages.error(request, "Sessão expirada. Solicite um novo código ou faça o registro novamente.")
        return redirect(reverse("accounts:registro"))

    if request.method == "POST":
        senha1 = request.POST.get("senha1", "").strip()
        senha2 = request.POST.get("senha2", "").strip()

        if not senha1 or not senha2:
            messages.error(request, "Informe e confirme a nova senha.")
            return render(request, "accounts/definir_senha.html")
        if senha1 != senha2:
            messages.error(request, "As senhas não conferem.")
            return render(request, "accounts/definir_senha.html")

        try:
            user = Usuario.objects.get(email=pending_email)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return render(request, "accounts/definir_senha.html")

        user.set_password(senha1)
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])
        # Finaliza o fluxo apagando o email da sessão
        try:
            del request.session["pending_email"]
        except KeyError:
            pass
        return redirect(reverse("login"))

    return render(request, "accounts/definir_senha.html")


def _gerar_codigo_otp() -> str:
    from secrets import token_hex

    return token_hex(3)


def login_view(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if getattr(user, "must_change_password", False):
            messages.info(request, "Defina uma nova senha para continuar.")
            return redirect(reverse("accounts:definir_senha"))
        login(request, user)
        return redirect("/")
    return render(request, "accounts/login.html", {"form": form})


def reenviar_otp_view(request: HttpRequest) -> HttpResponse:
    pending_email = request.session.get("pending_email")
    if not pending_email:
        messages.error(request, "Sessão expirada. Faça o registro novamente.")
        logger.warning("Sessão expirada em reenviar_otp sem pending_email")
        return redirect(reverse("accounts:registro"))

    try:
        user = Usuario.objects.get(email=pending_email)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        logger.warning("Usuário não encontrado ao reenviar OTP: %s", pending_email)
        return redirect(reverse("accounts:registro"))

    ultimo = OTP.objects.filter(user=user, tipo=OTP.OTPType.REGISTRO).order_by("-criado_em").first()
    if ultimo and (timezone.now() - ultimo.criado_em) < timedelta(seconds=60):
        restante = 60 - int((timezone.now() - ultimo.criado_em).total_seconds())
        messages.error(request, f"Aguarde {restante}s para solicitar um novo código.")
        logger.info("Reenvio bloqueado por janela de 60s | email=%s restante=%ss", user.email, restante)
        return redirect(reverse("accounts:confirmar_otp"))

    # Invalida anteriores e cria novo
    OTP.objects.filter(user=user, tipo=OTP.OTPType.REGISTRO, usado=False).update(usado=True)
    otp = OTP.objects.create(
        user=user,
        code=_gerar_codigo_otp(),
        expira_em=timezone.now() + timedelta(minutes=10),
        tipo=OTP.OTPType.REGISTRO,
    )
    send_mail(
        subject="Seu novo código OTP",
        message=f"Seu OTP é: {otp.code}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )
    messages.success(request, "Novo OTP enviado ao seu email.")
    logger.info("Novo OTP enviado | email=%s otp_id=%s expira_em=%s", user.email, otp.id, otp.expira_em)
    return redirect(reverse("accounts:confirmar_otp"))


# Create your views here.
