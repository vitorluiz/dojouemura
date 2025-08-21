from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail

from .models import Usuario, OTP


def registro_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()

        if not first_name or not last_name or not email:
            messages.error(request, "Preencha nome e email.")
            return render(request, "accounts/registro.html")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado.")
            return render(request, "accounts/registro.html")

        user = Usuario.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=False,
        )

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
        messages.success(request, "OTP enviado ao seu email.")
        return redirect(reverse("accounts:confirmar_otp"))

    return render(request, "accounts/registro.html")


def confirmar_otp_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        code = request.POST.get("code", "").strip()

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return render(request, "accounts/confirmar_otp.html")

        otp = (
            OTP.objects.filter(user=user, code=code, tipo=OTP.OTPType.REGISTRO, usado=False)
            .order_by("-criado_em")
            .first()
        )
        if not otp or not otp.esta_valido():
            messages.error(request, "OTP inválido ou expirado.")
            return render(request, "accounts/confirmar_otp.html")

        otp.marcar_usado()
        token = signing.dumps({"email": user.email, "purpose": "ativacao"})
        activation_link = request.build_absolute_uri(reverse("accounts:ativar")) + f"?t={token}"
        send_mail(
            subject="Ative sua conta",
            message=f"Clique para ativar sua conta: {activation_link}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True,
        )
        messages.success(request, "OTP confirmado. Link de ativação enviado ao seu email.")
        return redirect(reverse("accounts:ativar"))

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

    return render(request, "accounts/ativar.html")


def definir_senha_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        senha = request.POST.get("senha", "").strip()
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return render(request, "accounts/definir_senha.html")

        if not senha:
            messages.error(request, "Informe a nova senha.")
            return render(request, "accounts/definir_senha.html")

        user.set_password(senha)
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])
        return redirect("/login")

    return render(request, "accounts/definir_senha.html")


def _gerar_codigo_otp() -> str:
    from secrets import token_hex

    return token_hex(3)


# Create your views here.
