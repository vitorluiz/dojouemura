from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Modalidade, Dependente

def home(request):
    """Página inicial pública"""
    context = {
        'title': 'Dojô Uemura - Formando Campeões no Tatame e na Vida',
        'modalidades': Modalidade.objects.filter(ativa=True),
        'total_atletas': Dependente.objects.count(),
    }
    return render(request, 'publico/home.html', context)

def projeto_social(request):
    """Página do projeto social"""
    context = {
        'title': 'Projeto Social - Dojô Uemura',
    }
    return render(request, 'publico/projeto_social.html', context)

def galeria(request):
    """Página da galeria pública"""
    context = {
        'title': 'Galeria - Dojô Uemura',
    }
    return render(request, 'publico/galeria.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def contato(request):
    """Página de contato"""
    if request.method == 'POST':
        # Processar formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Validar dados
        if not all([nome, email, assunto, mensagem]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('publico:contato')
        
        try:
            # Salvar mensagem no banco de dados
            from empresa.models import Empresa, MensagemContato
            
            # Criar mensagem
            mensagem_contato = MensagemContato.objects.create(
                nome=nome,
                email=email,
                telefone=telefone,
                assunto=assunto,
                mensagem=mensagem
            )
            
            # Buscar dados da empresa para o email de destino
            empresa = Empresa.objects.filter(ativo=True).first()
            email_destino = empresa.email if empresa else 'contato@dojouemura.com'
            
            # Preparar conteúdo do email
            assunto_email = f"Contato via Site - {assunto}"
            
            # Corpo do email
            corpo_email = f"""
            Nova mensagem de contato recebida via site:
            
            Nome: {nome}
            Email: {email}
            Telefone: {telefone or 'Não informado'}
            Assunto: {assunto}
            
            Mensagem:
            {mensagem}
            
            ---
            Enviado automaticamente pelo site do Dojô Uemura
            """
            
            # Enviar email
            send_mail(
                subject=assunto_email,
                message=corpo_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_destino],
                fail_silently=False,
            )
            
            # Email de confirmação para o usuário
            confirmação_email = f"""
            Olá {nome},
            
            Recebemos sua mensagem com sucesso!
            
            Assunto: {assunto}
            Mensagem: {mensagem}
            
            Entraremos em contato em breve.
            
            Atenciosamente,
            Equipe Dojô Uemura
            """
            
            send_mail(
                subject="Confirmação de Contato - Dojô Uemura",
                message=confirmação_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            messages.success(request, 'Mensagem enviada com sucesso! Em breve entraremos em contato.')
            return redirect('publico:contato')
            
        except Exception as e:
            messages.error(request, f'Erro ao enviar mensagem: {str(e)}')
            return redirect('publico:contato')
    
    context = {
        'title': 'Contato - Dojô Uemura',
    }
    return render(request, 'publico/contato.html', context)

def registro(request):
    """Página de registro público"""
    context = {
        'title': 'Registro - Dojô Uemura',
    }
    return render(request, 'publico/registro.html', context)

def login(request):
    """Página de login público"""
    context = {
        'title': 'Login - Dojô Uemura',
    }
    return render(request, 'publico/login.html', context)

@login_required
def perfil(request):
    """Página de perfil do usuário logado"""
    context = {
        'title': 'Meu Perfil - Dojô Uemura',
        'user': request.user,
    }
    return render(request, 'publico/perfil.html', context)
