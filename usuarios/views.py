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
from .models import Usuario, Atleta, TipoMatricula, Modalidade, StatusMatricula
from .forms import UsuarioRegistroForm, UsuarioLoginForm, AtletaForm
from utils.validacoes import buscar_cep
import requests
from datetime import date, datetime
import logging
import secrets
import string

# Configurar logger
logger = logging.getLogger(__name__)


def home(request):
    """Página inicial"""
    if request.user.is_authenticated:
        atletas = Atleta.objects.filter(usuario=request.user)
        return render(request, 'usuarios/usuario/painel.html', {'atletas': atletas})
    return render(request, 'usuarios/usuario/home.html')


def registro_usuario(request):
    """Registro de novo usuário"""
    import logging
    logger = logging.getLogger('usuarios.views')
    
    if request.method == 'POST':
        logger.debug(f"POST recebido - {request.POST}")
        form = UsuarioRegistroForm(request.POST)
        logger.debug(f"Formulário criado - {form}")
        logger.debug(f"Formulário válido? {form.is_valid()}")
        if not form.is_valid():
            logger.debug(f"Erros do formulário: {form.errors}")
        
        if form.is_valid():
            logger.info("Formulário válido, criando usuário...")
            usuario = form.save(commit=False)
            # Usar email como username temporariamente
            usuario.username = usuario.email
            
            # Gerar senha temporária aleatória
            senha_temp = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            usuario.set_password(senha_temp)
            
            usuario.is_active = False  # Usuário inativo até verificar email
            usuario.save()
            logger.info(f"Usuário criado com ID: {usuario.id}")
            
            # Enviar email de verificação com senha temporária
            logger.info("Tentando enviar email de verificação...")
            email_enviado = enviar_email_verificacao(request, usuario, senha_temp)
            
            if email_enviado:
                logger.info(f"Email de verificação agendado com sucesso para {usuario.email}")
                messages.success(request, 'Cadastro realizado com sucesso! Verifique seu email para ativar sua conta.')
                return redirect('usuarios:login')
            else:
                # Se o email falhou, ainda criar o usuário mas informar sobre o problema
                logger.warning(f"Falha ao agendar email de verificação para {usuario.email}")
                messages.warning(request, 'Cadastro realizado, mas houve um problema ao enviar o email de verificação. Entre em contato com o suporte.')
                return redirect('usuarios:login')
        else:
            logger.debug("Formulário inválido, renderizando com erros...")
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
    import logging
    logger = logging.getLogger('usuarios.views')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        acao = request.POST.get('acao', 'recuperar')  # 'recuperar' ou 'reenviar_verificacao'
        
        try:
            usuario = Usuario.objects.get(email=email)
            
            if acao == 'reenviar_verificacao' and not usuario.email_verificado:
                # Reenviar email de verificação
                senha_temp = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                usuario.set_password(senha_temp)
                usuario.save()
                
                # Usar Celery para reenviar email de verificação
                from .tasks import enviar_email_verificacao_task
                
                # Criar tarefa para reenviar email
                task = enviar_email_verificacao_task.delay(usuario.id, senha_temp)
                
                logger.info(f"Tarefa de reenvio de verificação criada: {task.id} para {usuario.email}")
                messages.success(request, 'Email de verificação reenviado! Verifique sua caixa de entrada.')
                return redirect('usuarios:login')
                
            elif acao == 'recuperar':
                if usuario.email_verificado:
                    # Usuário verificado - processo normal de recuperação
                    token = default_token_generator.make_token(usuario)
                    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                    
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
                    
                    # Usar Celery para enviar email em background
                    from .tasks import enviar_email_recuperacao_senha_task
                    
                    # Criar tarefa para enviar email de recuperação
                    task = enviar_email_recuperacao_senha_task.delay(usuario.id, reset_url)
                    
                    logger.info(f"Tarefa de recuperação de senha criada: {task.id} para {usuario.email}")
                    
                    messages.success(request, 'Email de recuperação enviado! Verifique sua caixa de entrada.')
                    return redirect('usuarios:login')
                else:
                    # Usuário não verificado - mostrar opções
                    messages.warning(request, 'Este email ainda não foi verificado. Você pode reenviar o email de verificação ou prosseguir com a recuperação de senha.')
                    return render(request, 'usuarios/esqueceu_senha.html', {
                        'email': email,
                        'usuario_nao_verificado': True,
                        'usuario': usuario
                    })
                    
        except Usuario.DoesNotExist:
            messages.error(request, 'Email não encontrado em nossa base de dados.')
    
    return render(request, 'usuarios/esqueceu_senha.html')


def reenviar_verificacao(request):
    """Reenvia email de verificação para usuário não verificado"""
    import logging
    logger = logging.getLogger('usuarios.views')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            if not usuario.email_verificado:
                # Gerar nova senha temporária
                import secrets
                import string
                senha_temp = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                usuario.set_password(senha_temp)
                usuario.save()
                
                # Usar Celery para reenviar email de verificação
                from .tasks import enviar_email_verificacao_task
                
                # Criar tarefa para reenviar email
                task = enviar_email_verificacao_task.delay(usuario.id, senha_temp)
                
                logger.info(f"Tarefa de reenvio de verificação criada: {task.id} para {usuario.email}")
                messages.success(request, 'Email de verificação reenviado! Verifique sua caixa de entrada.')
                return redirect('usuarios:login')
            else:
                messages.info(request, 'Este email já foi verificado.')
                return redirect('usuarios:login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email não encontrado em nossa base de dados.')
    
    return redirect('usuarios:esqueceu_senha')


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
    """Envia email de verificação para o usuário usando Celery"""
    import logging
    logger = logging.getLogger('usuarios.views')
    
    try:
        logger.info(f"Iniciando envio de email de verificação via Celery para {usuario.email}")
        
        # Importar a tarefa do Celery
        from .tasks import enviar_email_verificacao_task
        
        # Executar a tarefa em background
        task = enviar_email_verificacao_task.delay(usuario.id, senha_temporaria)
        
        logger.info(f"Tarefa Celery criada com ID: {task.id} para usuário {usuario.email}")
        logger.debug(f"Email será enviado em background para: {usuario.email}")
        
        return True
        
    except Exception as e:
        logger.error(f"Falha ao criar tarefa Celery para usuário {usuario.email}: {e}", exc_info=True)
        return False


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
def cadastrar_atleta(request):
    """Cadastro de atleta"""
    if request.method == 'POST':
        form = AtletaForm(request.POST, request.FILES, usuario=request.user)
        if form.is_valid():
            atleta = form.save(commit=False)
            atleta.usuario = request.user
            
            # Se "outra" escola foi selecionada, usar o valor do campo escola_outra
            if atleta.escola == 'outra':
                escola_outra = request.POST.get('escola_outra', '')
                if escola_outra:
                    atleta.escola = escola_outra
            
            # Buscar dados do CEP
            cep_data = buscar_cep(atleta.cep.replace('-', ''))
            if cep_data:
                atleta.logradouro = cep_data.get('logradouro', atleta.logradouro)
                atleta.bairro = cep_data.get('bairro', atleta.bairro)
                atleta.cidade = cep_data.get('localidade', atleta.cidade)
                atleta.uf = cep_data.get('uf', atleta.uf)
            
            atleta.save()
            messages.success(request, 'Atleta cadastrado com sucesso!')
            return redirect('usuarios:home')
    else:
        form = AtletaForm(usuario=request.user)
    
    return render(request, 'usuarios/cadastrar_atleta.html', {'form': form})


@login_required
def editar_atleta(request, atleta_id):
    """Editar atleta"""
    atleta = get_object_or_404(Atleta, id=atleta_id, usuario=request.user)
    
    if request.method == 'POST':
        form = AtletaForm(request.POST, request.FILES, instance=atleta, usuario=request.user)
        if form.is_valid():
            atleta = form.save(commit=False)
            
            # Se "outra" escola foi selecionada, usar o valor do campo escola_outra
            if atleta.escola == 'outra':
                escola_outra = request.POST.get('escola_outra', '')
                if escola_outra:
                    atleta.escola = escola_outra
            
            # Buscar dados do CEP se foi alterado
            cep_data = buscar_cep(atleta.cep.replace('-', ''))
            if cep_data:
                atleta.logradouro = cep_data.get('logradouro', atleta.logradouro)
                atleta.bairro = cep_data.get('bairro', atleta.bairro)
                atleta.cidade = cep_data.get('localidade', atleta.cidade)
                atleta.uf = cep_data.get('uf', atleta.uf)
            
            atleta.save()
            messages.success(request, 'Atleta atualizado com sucesso!')
            return redirect('usuarios:home')
    else:
        form = AtletaForm(instance=atleta, usuario=request.user)
    
    return render(request, 'usuarios/editar_atleta.html', {'form': form, 'atleta': atleta})


@login_required
def excluir_atleta(request, atleta_id):
    """Excluir atleta"""
    atleta = get_object_or_404(Atleta, id=atleta_id, usuario=request.user)
    
    if request.method == 'POST':
        atleta.delete()
        messages.success(request, 'Atleta excluído com sucesso!')
        return redirect('usuarios:home')
    
    return render(request, 'usuarios/excluir_atleta.html', {'atleta': atleta})


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
            
            # ✅ Criar atleta E sua primeira matrícula
            from .models import Matricula
            
            atleta = Atleta.objects.create(
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
                atleta=atleta,
                tipo_matricula=TipoMatricula.objects.get(nome='Projeto Social'),
                modalidade=Modalidade.objects.get(nome='Jiu-Jitsu'),
                status_matricula=StatusMatricula.objects.get(nome='Pendente'),
                data_matricula=date.today()
            )
            
            logger.info(f"Atleta criado com primeira matrícula: {atleta.id} - Matrícula: {primeira_matricula.id}")
            
            # Redirecionar para dashboard
            return redirect('usuarios:dashboard')
            
        except Exception as e:
            logger.error(f"Erro ao criar atleta: {str(e)}")
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
                atleta_existente = Atleta.objects.get(cpf=cpf_busca)
                logger.info(f"[SUCESSO] ATLETA ENCONTRADO pelo CPF exato: {atleta_existente.nome}")
                logger.info(f"   CPF no banco: '{atleta_existente.cpf}'")
                logger.info(f"   Tipo CPF no banco: {type(atleta_existente.cpf)}")
                
            except Atleta.DoesNotExist:
                logger.info(f"[BUSCA] CPF exato não encontrado, tentando limpo...")
                try:
                    # Se não encontrar, tentar com CPF limpo
                    cpf_limpo = cpf_busca.replace('.', '').replace('-', '')
                    logger.info(f"Tentando buscar pelo CPF limpo: '{cpf_limpo}'")
                    atleta_existente = Atleta.objects.get(cpf=cpf_limpo)
                    logger.info(f"[SUCESSO] ATLETA ENCONTRADO pelo CPF limpo: {atleta_existente.nome}")
                    logger.info(f"   CPF no banco: '{atleta_existente.cpf}'")
                    
                except Atleta.DoesNotExist:
                    logger.warning(f"[ERRO] CPF não encontrado nem exato nem limpo: '{cpf_busca}'")
                    logger.info(f"CPFs no banco:")
                    for dep in Atleta.objects.all():
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
            atleta_existente = Atleta.objects.get(cpf=cpf_original)
            is_atleta_existente = True
            logger.info(f"[SUCESSO] ATLETA EXISTENTE encontrado pelo CPF exato: {atleta_existente.nome}")
        except Atleta.DoesNotExist:
            try:
                # Segundo: tentar CPF limpo
                atleta_existente = Atleta.objects.get(cpf=cpf_limpo)
                is_atleta_existente = True
                logger.info(f"[SUCESSO] ATLETA EXISTENTE encontrado pelo CPF limpo: {atleta_existente.nome}")
            except Atleta.DoesNotExist:
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
            cpf = request.POST.get('cpf')  # Definir a variável cpf aqui
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
                
                atleta = Atleta.objects.create(
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
                    atleta=atleta,
                    tipo_matricula=TipoMatricula.objects.get(nome='Modalidade Paga'),
                    modalidade=Modalidade.objects.get(id=modalidade_id),
                    status_matricula=StatusMatricula.objects.get(nome='Pendente'),
                    data_matricula=date.today()
                )
                
                logger.info(f"Novo atleta criado com primeira matrícula: {atleta.id} - Matrícula: {primeira_matricula.id}")
            
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
    atletas = Atleta.objects.filter(usuario=usuario).prefetch_related('matriculas__modalidade', 'matriculas__tipo_matricula', 'matriculas__status_matricula')
    
    context = {
        'usuario': usuario,
        'atletas': atletas,
        'nome_completo': f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    }
    
    return render(request, 'usuarios/usuario/painel.html', context)

