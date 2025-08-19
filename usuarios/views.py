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
from .models import Usuario, Dependente, TipoMatricula, Modalidade, StatusMatricula
from .forms import UsuarioRegistroForm, UsuarioLoginForm, DependenteForm
import requests
from datetime import date, datetime
import logging

# Configurar logger
logger = logging.getLogger(__name__)


def home(request):
    """Página inicial"""
    if request.user.is_authenticated:
        dependentes = Dependente.objects.filter(usuario=request.user)
        return render(request, 'usuarios/usuario/painel.html', {'dependentes': dependentes})
    return render(request, 'usuarios/usuario/home.html')


def registro_usuario(request):
    """Registro de novo usuário"""
    if request.method == 'POST':
        print(f"DEBUG: POST recebido - {request.POST}")
        form = UsuarioRegistroForm(request.POST)
        print(f"DEBUG: Formulário criado - {form}")
        print(f"DEBUG: Formulário válido? {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: Erros do formulário: {form.errors}")
        
        if form.is_valid():
            print("DEBUG: Formulário válido, criando usuário...")
            usuario = form.save(commit=False)
            # Usar email como username temporariamente
            usuario.username = usuario.email
            
            # Gerar senha temporária aleatória
            import secrets
            import string
            senha_temp = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            usuario.set_password(senha_temp)
            
            usuario.is_active = False  # Usuário inativo até verificar email
            usuario.save()
            print(f"DEBUG: Usuário criado com ID: {usuario.id}")
            
            # Enviar email de verificação com senha temporária
            enviar_email_verificacao(request, usuario, senha_temp)
            
            messages.success(request, 'Cadastro realizado com sucesso! Verifique seu email para ativar sua conta.')
            return redirect('login')
        else:
            print("DEBUG: Formulário inválido, renderizando com erros...")
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
                    return redirect('usuarios:home')
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
    return redirect('usuarios:login')


def esqueceu_senha(request):
    """Recuperação de senha"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.email_verificado:
                # Gerar token para reset de senha
                token = default_token_generator.make_token(usuario)
                uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                
                # Enviar email com link para reset
                reset_url = request.build_absolute_uri(
                    reverse('usuarios:reset_senha', kwargs={'uidb64': uid, 'token': token})
                )
                
                assunto = "Recuperação de Senha - Dojô Uemura"
                mensagem = f"""
                Olá {usuario.first_name},
                
                Você solicitou a recuperação de senha para sua conta no Dojô Uemura.
                
                Para redefinir sua senha, clique no link abaixo:
                {reset_url}
                
                Se você não solicitou esta recuperação, ignore este email.
                
                Atenciosamente,
                Equipe Dojô Uemura
                """
                
                send_mail(
                    subject=assunto,
                    message=mensagem,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Email de recuperação enviado! Verifique sua caixa de entrada.')
                return redirect('usuarios:login')
            else:
                messages.error(request, 'Este email ainda não foi verificado. Verifique sua caixa de entrada primeiro.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email não encontrado em nossa base de dados.')
    
    return render(request, 'usuarios/esqueceu_senha.html')


def reset_senha(request, uidb64, token):
    """Reset de senha com token"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None
    
    if usuario is not None and default_token_generator.check_token(usuario, token):
        if request.method == 'POST':
            senha1 = request.POST.get('senha1')
            senha2 = request.POST.get('senha2')
            
            if senha1 == senha2 and len(senha1) >= 8:
                usuario.set_password(senha1)
                usuario.save()
                messages.success(request, 'Senha alterada com sucesso! Faça login com sua nova senha.')
                return redirect('usuarios:login')
            else:
                messages.error(request, 'As senhas não coincidem ou são muito curtas (mínimo 8 caracteres).')
        
        return render(request, 'usuarios/reset_senha.html')
    else:
        messages.error(request, 'Link de recuperação inválido ou expirado.')
        return redirect('usuarios:login')


def enviar_email_verificacao(request, usuario, senha_temporaria):
    """Envia email de verificação para o usuário"""
    token = default_token_generator.make_token(usuario)
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    
    verification_url = request.build_absolute_uri(
        reverse('usuarios:verificar_email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = 'Verificação de Email - Cadastro Dojô Uemura'
    nome_completo = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    message = f'''
    Olá {nome_completo},
    
    Para ativar sua conta, clique no link abaixo:
    {verification_url}
    
    Sua senha temporária para login é: {senha_temporaria}
    
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
        
        # Fazer login automático do usuário
        login(request, usuario)
        
        messages.success(request, 'Email verificado com sucesso! Bem-vindo ao seu portal.')
        return redirect('usuarios:dashboard')
    else:
        messages.error(request, 'Link de verificação inválido ou expirado.')
        return redirect('usuarios:login')


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
        logger.info("=== INÍCIO DO PROCESSAMENTO DE MATRÍCULA PROJETO SOCIAL ===")
        
        # Log de todos os dados recebidos
        logger.info(f"POST data recebida: {request.POST}")
        logger.info(f"FILES data recebida: {request.FILES}")
        
        # Verificar campos obrigatórios
        required_fields = [
            'nome_completo', 'data_nascimento', 'cpf', 'parentesco', 'foto',
            'escolaridade', 'escola', 'turno', 'cep', 'logradouro', 'numero',
            'bairro', 'cidade', 'uf', 'termo_responsabilidade', 'termo_uso_imagem', 'termo_saude'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field == 'foto':
                if field not in request.FILES:
                    missing_fields.append(field)
                    logger.warning(f"Campo obrigatório ausente: {field}")
            else:
                if not request.POST.get(field):
                    missing_fields.append(field)
                    logger.warning(f"Campo obrigatório ausente: {field}")
        
        if missing_fields:
            logger.error(f"Campos obrigatórios ausentes: {missing_fields}")
            return render(request, 'usuarios/matricula_projeto_social.html', {
                'error_message': f'Campos obrigatórios ausentes: {", ".join(missing_fields)}'
            })
        
        logger.info("Todos os campos obrigatórios estão preenchidos")
        
        try:
            # Processar dados do formulário
            nome_completo = request.POST.get('nome_completo')
            data_nascimento = request.POST.get('data_nascimento')
            cpf = request.POST.get('cpf')
            parentesco = request.POST.get('parentesco')
            foto = request.FILES.get('foto')
            escolaridade = request.POST.get('escolaridade')
            escola = request.POST.get('escola')
            turno = request.POST.get('turno')
            cep = request.POST.get('cep')
            logradouro = request.POST.get('logradouro')
            numero = request.POST.get('numero')
            bairro = request.POST.get('bairro')
            cidade = request.POST.get('cidade')
            uf = request.POST.get('uf')
            condicoes_medicas = request.POST.get('condicoes_medicas', '')
            
            logger.info(f"Dados processados - Nome: {nome_completo}, Data: {data_nascimento}, CPF: {cpf}")
            
            # Validações
            if not request.user.is_authenticated:
                logger.error("Usuário não autenticado")
                return render(request, 'usuarios/matricula_projeto_social.html', {
                    'error_message': 'Usuário não autenticado'
                })
            
            # ✅ Criar dependente E sua primeira matrícula
            from .models import Matricula
            
            dependente = Dependente.objects.create(
                usuario=request.user,
                nome=nome_completo,
                data_nascimento=data_nascimento,
                cpf=cpf,
                parentesco=parentesco,
                foto=foto,
                escolaridade=escolaridade,
                escola=escola,
                turno=turno,
                cep=cep,
                logradouro=logradouro,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                condicoes_medicas=condicoes_medicas
            )
            
            # Criar primeira matrícula (Projeto Social)
            primeira_matricula = Matricula.objects.create(
                atleta=dependente,
                tipo_matricula=TipoMatricula.objects.get(nome='Projeto Social'),
                modalidade=Modalidade.objects.get(nome='Jiu-Jitsu'),
                status_matricula=StatusMatricula.objects.get(nome='Pendente'),
                data_matricula=date.today()
            )
            
            logger.info(f"Dependente criado com primeira matrícula: {dependente.id} - Matrícula: {primeira_matricula.id}")
            
            # Redirecionar para dashboard
            return redirect('usuarios:dashboard')
            
        except Exception as e:
            logger.error(f"Erro ao criar dependente: {str(e)}")
            return render(request, 'usuarios/matricula_projeto_social.html', {
                'error_message': f'Erro ao processar matrícula: {str(e)}'
            })
    
    logger.info("Renderizando formulário de matrícula projeto social")
    return render(request, 'usuarios/matricula_projeto_social.html')


@login_required
def matricula_modalidade_paga(request):
    if request.method == 'POST':
        logger.info("=== INÍCIO DO PROCESSAMENTO DE MATRÍCULA MODALIDADE PAGA ===")
        
        # Log de todos os dados recebidos
        logger.info(f"POST data recebida: {request.POST}")
        logger.info(f"FILES data recebida: {request.FILES}")
        
        # Verificar se é busca por CPF ou nova matrícula
        if 'buscar_cpf' in request.POST:
            # Busca por CPF existente - NÃO LIMPAR O CPF!
            cpf_busca = request.POST.get('cpf_busca', '').strip()
            logger.info(f"=== BUSCA POR CPF INICIADA ===")
            logger.info(f"CPF recebido: '{cpf_busca}'")
            logger.info(f"Tipo do CPF: {type(cpf_busca)}")
            logger.info(f"Tamanho do CPF: {len(cpf_busca)}")
            
            try:
                # Buscar primeiro pelo CPF exato (com formatação)
                logger.info(f"Tentando buscar pelo CPF exato: '{cpf_busca}'")
                atleta_existente = Dependente.objects.get(cpf=cpf_busca)
                logger.info(f"[SUCESSO] ATLETA ENCONTRADO pelo CPF exato: {atleta_existente.nome}")
                logger.info(f"   CPF no banco: '{atleta_existente.cpf}'")
                logger.info(f"   Tipo CPF no banco: {type(atleta_existente.cpf)}")
                
            except Dependente.DoesNotExist:
                logger.info(f"[BUSCA] CPF exato não encontrado, tentando limpo...")
                try:
                    # Se não encontrar, tentar com CPF limpo
                    cpf_limpo = cpf_busca.replace('.', '').replace('-', '')
                    logger.info(f"Tentando buscar pelo CPF limpo: '{cpf_limpo}'")
                    atleta_existente = Dependente.objects.get(cpf=cpf_limpo)
                    logger.info(f"[SUCESSO] ATLETA ENCONTRADO pelo CPF limpo: {atleta_existente.nome}")
                    logger.info(f"   CPF no banco: '{atleta_existente.cpf}'")
                    
                except Dependente.DoesNotExist:
                    logger.warning(f"[ERRO] CPF não encontrado nem exato nem limpo: '{cpf_busca}'")
                    logger.info(f"CPFs no banco:")
                    for dep in Dependente.objects.all():
                        logger.info(f"   '{dep.cpf}' - {dep.nome}")
                    
                    return render(request, 'usuarios/matricula_modalidade_paga.html', {
                        'modalidades': Modalidade.objects.all(),
                        'error_message': 'CPF não encontrado. Preencha todos os dados para nova matrícula.'
                    })
            
            # Retornar dados do atleta para preenchimento automático
            logger.info(f"[CONTROLE] Retornando template com atleta_existente: {atleta_existente.nome}")
            logger.info(f"   Contexto: atleta_existente={atleta_existente}, modalidades={Modalidade.objects.count()}")
            
            return render(request, 'usuarios/matricula_modalidade_paga.html', {
                'atleta_existente': atleta_existente,
                'modalidades': Modalidade.objects.all(),
                'success_message': f'Atleta encontrado: {atleta_existente.nome}. Preencha apenas a modalidade desejada.'
            })
        
        # Processar matrícula (nova ou existente)
        cpf_original = request.POST.get('cpf', '')
        cpf_limpo = cpf_original.replace('.', '').replace('-', '')
        modalidade_id = request.POST.get('modalidade')
        
        logger.info(f"[CPF] CPF original recebido: '{cpf_original}'")
        logger.info(f"[CPF] CPF limpo para busca: '{cpf_limpo}'")
        
        # VARIÁVEL DE CONTROLE: Verificar se atleta já existe
        is_atleta_existente = False
        atleta_existente = None
        
        # Buscar atleta por CPF (usando a mesma lógica da busca)
        try:
            # Primeiro: tentar CPF exato (com formatação)
            atleta_existente = Dependente.objects.get(cpf=cpf_original)
            is_atleta_existente = True
            logger.info(f"[SUCESSO] ATLETA EXISTENTE encontrado pelo CPF exato: {atleta_existente.nome}")
        except Dependente.DoesNotExist:
            try:
                # Segundo: tentar CPF limpo
                atleta_existente = Dependente.objects.get(cpf=cpf_limpo)
                is_atleta_existente = True
                logger.info(f"[SUCESSO] ATLETA EXISTENTE encontrado pelo CPF limpo: {atleta_existente.nome}")
            except Dependente.DoesNotExist:
                is_atleta_existente = False
                logger.info("Novo atleta sendo cadastrado")
        
        # LOGGING DE CONTROLE
        logger.info(f"[CONTROLE] VARIÁVEL DE CONTROLE: is_atleta_existente = {is_atleta_existente}")
        logger.info(f"[CONTROLE] Atleta existente: {atleta_existente.nome if atleta_existente else 'Nenhum'}")
        
        # Verificar campos obrigatórios baseado na variável de controle
        required_fields = ['nome', 'data_nascimento', 'cpf', 'parentesco', 'modalidade']
        
        # Para modalidade paga, escola, turma e turno são opcionais
        if not request.POST.get('escola') or not request.POST.get('turno'):
            logger.info("Modalidade paga: campos escolares são opcionais")
        
        # Foto só é obrigatória para novos atletas (usando variável de controle)
        if not is_atleta_existente:
            required_fields.append('foto')
            logger.info("[FOTO] Foto obrigatória para NOVO atleta")
        else:
            logger.info("[FOTO] Foto OPCIONAL para atleta EXISTENTE")
        
        missing_fields = []
        for field in required_fields:
            if field == 'foto':
                # Só validar foto se for obrigatória (novo atleta)
                if field in required_fields and field not in request.FILES:
                    missing_fields.append(field)
                    logger.warning(f"[ERRO] Campo obrigatório ausente: {field}")
            else:
                if not request.POST.get(field):
                    missing_fields.append(field)
                    logger.warning(f"[ERRO] Campo obrigatório ausente: {field}")
        
        if missing_fields:
            logger.error(f"Campos obrigatórios ausentes: {missing_fields}")
            return render(request, 'usuarios/matricula_modalidade_paga.html', {
                'modalidades': Modalidade.objects.all(),
                'error_message': f'Campos obrigatórios ausentes: {", ".join(missing_fields)}'
            })
        
        logger.info("Todos os campos obrigatórios estão preenchidos")
        
        try:
            
            # Processar dados do formulário
            nome_completo = request.POST.get('nome')
            data_nascimento = request.POST.get('data_nascimento')
            parentesco = request.POST.get('parentesco')
            foto = request.FILES.get('foto')
            escolaridade = request.POST.get('escolaridade', '')
            escola = request.POST.get('escola', '')
            turno = request.POST.get('turno', '')
            cep = request.POST.get('cep')
            logradouro = request.POST.get('logradouro')
            numero = request.POST.get('numero')
            bairro = request.POST.get('bairro')
            cidade = request.POST.get('cidade')
            uf = request.POST.get('uf')
            condicoes_medicas = request.POST.get('condicoes_medicas', '')
            
            logger.info(f"Dados processados - Nome: {nome_completo}, Modalidade: {modalidade_id}")
            
            # Validações
            if not request.user.is_authenticated:
                logger.error("Usuário não autenticado")
                return render(request, 'usuarios/matricula_modalidade_paga.html', {
                    'modalidades': Modalidade.objects.all(),
                    'error_message': 'Usuário não autenticado'
                })
            
            if atleta_existente:
                # ✅ CRIAR NOVA MATRÍCULA para atleta existente
                from .models import Matricula
                
                # Verificar se já existe matrícula ativa para esta modalidade
                matricula_existente = Matricula.objects.filter(
                    atleta=atleta_existente,
                    modalidade_id=modalidade_id,
                    ativa=True
                ).first()
                
                if matricula_existente:
                    logger.info(f"Matrícula já existe para esta modalidade: {matricula_existente.id}")
                    return render(request, 'usuarios/matricula_modalidade_paga.html', {
                        'modalidades': Modalidade.objects.all(),
                        'error_message': f'Atleta já possui matrícula ativa na modalidade {matricula_existente.modalidade.nome}'
                    })
                
                # Criar nova matrícula
                nova_matricula = Matricula.objects.create(
                    atleta=atleta_existente,
                    tipo_matricula=TipoMatricula.objects.get(nome='Modalidade Paga'),
                    modalidade=Modalidade.objects.get(id=modalidade_id),
                    status_matricula=StatusMatricula.objects.get(nome='Pendente'),
                    data_matricula=date.today()
                )
                
                logger.info(f"Nova matrícula criada para atleta existente: {nova_matricula.id}")
                
            else:
                # ✅ Criar novo atleta E sua primeira matrícula
                from .models import Matricula
                
                dependente = Dependente.objects.create(
                    usuario=request.user,
                    nome=nome_completo,
                    data_nascimento=data_nascimento,
                    cpf=cpf,
                    parentesco=parentesco,
                    foto=foto,
                    escolaridade=escolaridade,
                    escola=escola,
                    turno=turno,
                    cep=cep,
                    logradouro=logradouro,
                    numero=numero,
                    bairro=bairro,
                    cidade=cidade,
                    uf=uf,
                    condicoes_medicas=condicoes_medicas
                )
                
                # Criar primeira matrícula
                primeira_matricula = Matricula.objects.create(
                    atleta=dependente,
                    tipo_matricula=TipoMatricula.objects.get(nome='Modalidade Paga'),
                    modalidade=Modalidade.objects.get(id=modalidade_id),
                    status_matricula=StatusMatricula.objects.get(nome='Pendente'),
                    data_matricula=date.today()
                )
                
                logger.info(f"Novo atleta criado com primeira matrícula: {dependente.id} - Matrícula: {primeira_matricula.id}")
            
            # Redirecionar para dashboard
            return redirect('usuarios:dashboard')
            
        except Exception as e:
            logger.error(f"Erro ao processar matrícula: {str(e)}")
            return render(request, 'usuarios/matricula_modalidade_paga.html', {
                'modalidades': Modalidade.objects.all(),
                'error_message': f'Erro ao processar matrícula: {str(e)}'
            })
    
    logger.info("Renderizando formulário de matrícula modalidade paga")
    return render(request, 'usuarios/matricula_modalidade_paga.html', {
        'modalidades': Modalidade.objects.all()
    })


def dashboard(request):
    """Dashboard do usuário logado"""
    usuario = request.user
    dependentes = Dependente.objects.filter(usuario=usuario).prefetch_related('matriculas__modalidade', 'matriculas__tipo_matricula', 'matriculas__status_matricula')
    
    context = {
        'usuario': usuario,
        'dependentes': dependentes,
        'nome_completo': f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    }
    
    return render(request, 'usuarios/usuario/painel.html', context)

