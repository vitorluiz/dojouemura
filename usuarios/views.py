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
    
    subject = 'Verificação de Email - Cadastro Dojô Uemura'
    message = f'''
    Olá {usuario.nome_completo},
    
    Para ativar sua conta, clique no link abaixo:
    {verification_url}
    
    Se você não se cadastrou em nosso site, ignore este email.
    
    Atenciosamente,
    Equipe Dojô Uemura
    '''
    
    #send_mail(
    #    subject,
    #    message,
    #    settings.DEFAULT_FROM_EMAIL,
    #    [usuario.email],
    #    fail_silently=False,
    #)
     # --- INÍCIO DO CÓDIGO DE DIAGNÓSTICO ---
    print("\n" + "="*60)
    print("DIAGNÓSTICO DE E-MAIL DENTRO DA VIEW DO DJANGO")
    print(f"  Remetente (From) que será usado: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  Usuário de Autenticação (Host User): {settings.EMAIL_HOST_USER}")
    print(f"  Senha de Autenticação (Host Password): {'*' * len(settings.EMAIL_HOST_PASSWORD) if hasattr(settings, 'EMAIL_HOST_PASSWORD') else 'NAO DEFINIDA'}")
    print("="*60 + "\n")
    # --- FIM DO CÓDIGO DE DIAGNÓSTICO ---
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, # Usando a configuração do settings
            [usuario.email],
            fail_silently=False,
        )
        print(">>> SUCESSO: O comando send_mail do Django foi executado.")
    except Exception as e:
        print(f">>> ERRO: O comando send_mail do Django falhou. Erro: {e}")


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


def galeria_completa(request):
    """View para a página completa da galeria"""
    return render(request, 'usuarios/galeria_completa.html')


@login_required
def matricula_projeto_social(request):
    """View para matrícula no projeto social"""
    if request.method == 'POST':
        # Processar formulário de matrícula no projeto social
        form_data = request.POST
        files = request.FILES
        
        try:
            # Criar dependente com dados do projeto social
            dependente = Dependente()
            dependente.usuario = request.user
            
            # Dados pessoais
            dependente.nome_completo = form_data.get('nome_completo')
            dependente.data_nascimento = form_data.get('data_nascimento')
            dependente.cpf = form_data.get('cpf')
            dependente.parentesco = form_data.get('parentesco')
            
            # Foto
            if 'foto' in files:
                dependente.foto = files['foto']
            
            # Endereço
            dependente.cep = form_data.get('cep')
            dependente.logradouro = form_data.get('logradouro')
            dependente.numero = form_data.get('numero')
            dependente.complemento = form_data.get('complemento', '')
            dependente.bairro = form_data.get('bairro')
            dependente.cidade = form_data.get('cidade')
            dependente.uf = form_data.get('uf')
            
            # Dados escolares
            dependente.escolaridade = form_data.get('escolaridade')
            dependente.escola = form_data.get('escola')
            dependente.turno = form_data.get('turno')
            
            # Informações médicas
            dependente.condicoes_medicas = form_data.get('condicoes_medicas', '')
            
            # Termos
            dependente.termo_responsabilidade = form_data.get('termo_responsabilidade') == 'on'
            dependente.termo_uso_imagem = form_data.get('termo_uso_imagem') == 'on'
            
            # Configurações de matrícula para projeto social
            from .models import TipoMatricula, StatusMatricula
            
            # Buscar tipo "Projeto Social"
            tipo_projeto_social = TipoMatricula.objects.filter(nome='Projeto Social').first()
            if tipo_projeto_social:
                dependente.tipo_matricula = tipo_projeto_social
            
            # Buscar status "Pendente"
            status_pendente = StatusMatricula.objects.filter(nome='Pendente').first()
            if status_pendente:
                dependente.status_matricula = status_pendente
            
            # Modalidade será Jiu-Jitsu (projeto social)
            modalidade_jiujitsu = Modalidade.objects.filter(nome='Jiu-Jitsu').first()
            if modalidade_jiujitsu:
                dependente.modalidade = modalidade_jiujitsu
            
            # Salvar dependente
            dependente.save()
            
            messages.success(
                request, 
                'Matrícula no projeto social solicitada com sucesso! '
                'Aguarde a análise e aprovação. Taxa de inscrição: R$ 50,00'
            )
            return redirect('home')
            
        except Exception as e:
            messages.error(
                request, 
                f'Erro ao processar matrícula: {str(e)}. '
                'Tente novamente ou entre em contato conosco.'
            )
    
    # GET request - mostrar formulário
    return render(request, 'usuarios/matricula_projeto_social.html')


@login_required
def matricula_modalidade_paga(request):
    """View para matrícula em modalidade paga"""
    if request.method == 'POST':
        # Processar formulário de matrícula paga
        form_data = request.POST
        files = request.FILES
        
        try:
            # Criar dependente com dados da modalidade paga
            dependente = Dependente()
            dependente.usuario = request.user
            
            # Dados pessoais
            dependente.nome_completo = form_data.get('nome_completo')
            dependente.data_nascimento = form_data.get('data_nascimento')
            dependente.cpf = form_data.get('cpf')
            dependente.parentesco = form_data.get('parentesco')
            
            # Foto
            if 'foto' in files:
                dependente.foto = files['foto']
            
            # Endereço
            dependente.cep = form_data.get('cep')
            dependente.logradouro = form_data.get('logradouro')
            dependente.numero = form_data.get('numero')
            dependente.complemento = form_data.get('complemento', '')
            dependente.bairro = form_data.get('bairro')
            dependente.cidade = form_data.get('cidade')
            dependente.uf = form_data.get('uf')
            
            # Dados escolares (opcional para modalidade paga)
            dependente.escolaridade = form_data.get('escolaridade', '')
            dependente.escola = form_data.get('escola', '')
            dependente.turno = form_data.get('turno', '')
            
            # Informações médicas
            dependente.condicoes_medicas = form_data.get('condicoes_medicas', '')
            
            # Termos (opcionais para modalidade paga)
            dependente.termo_responsabilidade = form_data.get('termo_responsabilidade') == 'on'
            dependente.termo_uso_imagem = form_data.get('termo_uso_imagem') == 'on'
            
            # Configurações de matrícula para modalidade paga
            from .models import TipoMatricula, StatusMatricula, Modalidade
            
            # Buscar tipo "Modalidade Paga"
            tipo_modalidade_paga = TipoMatricula.objects.filter(nome='Modalidade Paga').first()
            if tipo_modalidade_paga:
                dependente.tipo_matricula = tipo_modalidade_paga
            
            # Buscar status "Pendente"
            status_pendente = StatusMatricula.objects.filter(nome='Pendente').first()
            if status_pendente:
                dependente.status_matricula = status_pendente
            
            # Modalidade escolhida (obrigatória para modalidade paga)
            modalidade_id = form_data.get('modalidade')
            if modalidade_id:
                modalidade = Modalidade.objects.filter(id=modalidade_id).first()
                if modalidade:
                    dependente.modalidade = modalidade
            
            # Salvar dependente
            dependente.save()
            
            messages.success(
                request, 
                'Matrícula em modalidade paga solicitada com sucesso! '
                'Aguarde a análise e aprovação. Mensalidade será informada após aprovação.'
            )
            return redirect('home')
            
        except Exception as e:
            messages.error(
                request, 
                f'Erro ao processar matrícula: {str(e)}. '
                'Tente novamente ou entre em contato conosco.'
            )
    
    # GET request - mostrar formulário
    # Por enquanto, redirecionar para o formulário geral
    # TODO: Criar template específico para modalidade paga
    return redirect('cadastrar_dependente')

