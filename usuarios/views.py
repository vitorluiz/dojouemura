from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from .models import Usuario, Dependente
from .forms import UsuarioRegistroForm, UsuarioLoginForm, DependenteForm
import requests


def home(request):
    """Página inicial"""
    if request.user.is_authenticated:
        dependentes = Dependente.objects.filter(usuario=request.user)
        return render(request, 'usuarios/dashboard.html', {'dependentes': dependentes})
    return render(request, 'usuarios/home.html')


def registro_usuario(request):
    """Registro de novo usuário"""
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.username = usuario.nome_completo
            usuario.is_active = False  # Usuário inativo até verificar email
            usuario.save()
            
            # Enviar email de verificação
            enviar_email_verificacao(request, usuario)
            
            messages.success(request, 'Cadastro realizado com sucesso! Verifique seu email para ativar sua conta.')
            return redirect('login')
    else:
        form = UsuarioRegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})


def login_usuario(request):
    """Login do usuário"""
    if request.method == 'POST':
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.email_verificado:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Por favor, verifique seu email antes de fazer login.')
            else:
                messages.error(request, 'Email ou senha incorretos.')
    else:
        form = UsuarioLoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_usuario(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')


def enviar_email_verificacao(request, usuario):
    """Envia email de verificação para o usuário"""
    token = default_token_generator.make_token(usuario)
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    
    verification_url = request.build_absolute_uri(
        reverse('verificar_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = 'Verificação de Email - Cadastro de Pessoas'
    message = f'''
    Olá {usuario.nome_completo},
    
    Para ativar sua conta, clique no link abaixo:
    {verification_url}
    
    Se você não se cadastrou em nosso site, ignore este email.
    
    Atenciosamente,
    Equipe Cadastro de Pessoas
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )


def verificar_email(request, uidb64, token):
    """Verifica o email do usuário"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None
    
    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.email_verificado = True
        usuario.save()
        
        messages.success(request, 'Email verificado com sucesso! Agora você pode fazer login.')
        return redirect('login')
    else:
        messages.error(request, 'Link de verificação inválido ou expirado.')
        return redirect('login')


@login_required
def cadastrar_dependente(request):
    """Cadastro de dependente"""
    if request.method == 'POST':
        form = DependenteForm(request.POST, request.FILES)
        if form.is_valid():
            dependente = form.save(commit=False)
            dependente.usuario = request.user
            
            # Buscar dados do CEP
            cep_data = buscar_cep(dependente.cep.replace('-', ''))
            if cep_data:
                dependente.logradouro = cep_data.get('logradouro', dependente.logradouro)
                dependente.bairro = cep_data.get('bairro', dependente.bairro)
                dependente.cidade = cep_data.get('localidade', dependente.cidade)
                dependente.uf = cep_data.get('uf', dependente.uf)
            
            dependente.save()
            messages.success(request, 'Dependente cadastrado com sucesso!')
            return redirect('home')
    else:
        form = DependenteForm()
    
    return render(request, 'usuarios/cadastrar_dependente.html', {'form': form})


@login_required
def editar_dependente(request, dependente_id):
    """Editar dependente"""
    dependente = get_object_or_404(Dependente, id=dependente_id, usuario=request.user)
    
    if request.method == 'POST':
        form = DependenteForm(request.POST, request.FILES, instance=dependente)
        if form.is_valid():
            dependente = form.save(commit=False)
            
            # Buscar dados do CEP se foi alterado
            cep_data = buscar_cep(dependente.cep.replace('-', ''))
            if cep_data:
                dependente.logradouro = cep_data.get('logradouro', dependente.logradouro)
                dependente.bairro = cep_data.get('bairro', dependente.bairro)
                dependente.cidade = cep_data.get('localidade', dependente.cidade)
                dependente.uf = cep_data.get('uf', dependente.uf)
            
            dependente.save()
            messages.success(request, 'Dependente atualizado com sucesso!')
            return redirect('home')
    else:
        form = DependenteForm(instance=dependente)
    
    return render(request, 'usuarios/editar_dependente.html', {'form': form, 'dependente': dependente})


@login_required
def excluir_dependente(request, dependente_id):
    """Excluir dependente"""
    dependente = get_object_or_404(Dependente, id=dependente_id, usuario=request.user)
    
    if request.method == 'POST':
        dependente.delete()
        messages.success(request, 'Dependente excluído com sucesso!')
        return redirect('home')
    
    return render(request, 'usuarios/excluir_dependente.html', {'dependente': dependente})


def buscar_cep(cep):
    """Busca dados do CEP na API ViaCEP"""
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return data
    except requests.RequestException:
        pass
    return None


def buscar_cep_ajax(request):
    """Busca CEP via AJAX"""
    if request.method == 'GET':
        cep = request.GET.get('cep', '').replace('-', '')
        if len(cep) == 8:
            data = buscar_cep(cep)
            if data:
                return JsonResponse(data)
    
    return JsonResponse({'erro': 'CEP não encontrado'}, status=404)

