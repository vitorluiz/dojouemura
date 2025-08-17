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
from datetime import date, datetime


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
    if request.method == 'POST':
        # Processar dados do formulário
        nome_completo = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')
        escola = request.POST.get('escola')
        turma = request.POST.get('turma')
        turno = request.POST.get('turno')
        cep = request.POST.get('cep')
        logradouro = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        uf = request.POST.get('uf')
        
        # Validações básicas
        if not all([nome_completo, data_nascimento, cpf, escola, turma, turno, cep, logradouro, numero, bairro, cidade, uf]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return render(request, 'usuarios/matricula_projeto_social.html')
        
        # Validar idade (6-18 anos para projeto social)
        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            idade = (date.today() - data_nasc).days // 365
            if idade < 6 or idade > 18:
                messages.error(request, 'Para o projeto social, o dependente deve ter entre 6 e 18 anos.')
                return render(request, 'usuarios/matricula_projeto_social.html')
        except ValueError:
            messages.error(request, 'Data de nascimento inválida.')
            return render(request, 'usuarios/matricula_projeto_social.html')
        
        # Validar se escola foi informada (obrigatória para projeto social)
        if not escola.strip():
            messages.error(request, 'A escola é obrigatória para o projeto social.')
            return render(request, 'usuarios/matricula_projeto_social.html')
        
        try:
            # Buscar os objetos necessários
            tipo_matricula = TipoMatricula.objects.get(nome='Projeto Social')
            status_matricula = StatusMatricula.objects.get(nome='Pendente')
            modalidade_jiujitsu = Modalidade.objects.get(nome='Jiu-Jitsu')
            
            # Criar o dependente
            dependente = Dependente.objects.create(
                usuario=request.user,
                nome_completo=nome_completo,
                data_nascimento=data_nasc,
                cpf=cpf,
                escola=escola,
                turma=turma,
                turno=turno,
                cep=cep,
                logradouro=logradouro,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                tipo_matricula=tipo_matricula,
                modalidade=modalidade_jiujitsu,  # Projeto social sempre é Jiu-Jitsu
                status_matricula=status_matricula,
                data_matricula=date.today()
            )
            
            messages.success(request, f'Matrícula no projeto social realizada com sucesso! {nome_completo} está inscrito no Jiu-Jitsu gratuito.')
            return redirect('dashboard')
            
        except (TipoMatricula.DoesNotExist, StatusMatricula.DoesNotExist, Modalidade.DoesNotExist):
            messages.error(request, 'Erro ao processar a matrícula. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, 'usuarios/matricula_projeto_social.html')


@login_required
def matricula_modalidade_paga(request):
    if request.method == 'POST':
        # Processar dados do formulário
        nome_completo = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')
        escola = request.POST.get('escola')
        turma = request.POST.get('turma')
        turno = request.POST.get('turno')
        modalidade = request.POST.get('modalidade')
        plano = request.POST.get('plano')
        
        # Validações básicas
        if not all([nome_completo, data_nascimento, cpf, escola, turma, turno, modalidade, plano]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return render(request, 'usuarios/matricula_modalidade_paga.html')
        
        # Validar idade mínima (6 anos)
        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            idade = (date.today() - data_nasc).days // 365
            if idade < 6:
                messages.error(request, 'O dependente deve ter pelo menos 6 anos para se matricular.')
                return render(request, 'usuarios/matricula_modalidade_paga.html')
        except ValueError:
            messages.error(request, 'Data de nascimento inválida.')
            return render(request, 'usuarios/matricula_paga.html')
        
        try:
            # Buscar os objetos necessários
            tipo_matricula = TipoMatricula.objects.get(nome='Modalidade Paga')
            status_matricula = StatusMatricula.objects.get(nome='Pendente')
            modalidade_obj = Modalidade.objects.get(nome=modalidade.title())
            
            # Criar o dependente
            dependente = Dependente.objects.create(
                usuario=request.user,
                nome_completo=nome_completo,
                data_nascimento=data_nasc,
                cpf=cpf,
                escola=escola,
                turma=turma,
                turno=turno,
                tipo_matricula=tipo_matricula,
                modalidade=modalidade_obj,
                status_matricula=status_matricula,
                data_matricula=date.today()
            )
            
            messages.success(request, f'Matrícula de {nome_completo} realizada com sucesso! Status: Pendente de Pagamento.')
            return redirect('dashboard')
            
        except (TipoMatricula.DoesNotExist, StatusMatricula.DoesNotExist, Modalidade.DoesNotExist):
            messages.error(request, 'Erro ao processar a matrícula. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, 'usuarios/matricula_modalidade_paga.html')

