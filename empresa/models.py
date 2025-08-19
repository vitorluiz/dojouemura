from django.db import models
from utils.uuid7 import uuid7


class Empresa(models.Model):
    """Modelo para dados fiscais da empresa"""
    
    # Campos obrigatórios
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    nome_empresarial = models.CharField(max_length=200, verbose_name="Nome Empresarial")
    nome_fantasia = models.CharField(max_length=200, verbose_name="Nome Fantasia")
    logradouro = models.CharField(max_length=200, verbose_name="Logradouro")
    numero = models.CharField(max_length=20, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    municipio = models.CharField(max_length=100, verbose_name="Município")
    uf = models.CharField(max_length=2, verbose_name="UF")
    email = models.EmailField(verbose_name="Email")
    telefone1 = models.CharField(max_length=15, verbose_name="Telefone 1")
    telefone2 = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone 2")
    situacao_cadastral = models.CharField(max_length=50, verbose_name="Situação Cadastral")
    
    # Horários de atendimento por dia da semana
    segunda_feira = models.CharField(max_length=100, blank=True, null=True, verbose_name="Segunda-feira")
    terca_feira = models.CharField(max_length=100, blank=True, null=True, verbose_name="Terça-feira")
    quarta_feira = models.CharField(max_length=100, blank=True, null=True, verbose_name="Quarta-feira")
    quinta_feira = models.CharField(max_length=100, blank=True, null=True, verbose_name="Quinta-feira")
    sexta_feira = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sexta-feira")
    sabado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sábado")
    domingo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Domingo")
    
    # Horário geral (para compatibilidade)
    horarios_atendimento = models.TextField(blank=True, null=True, verbose_name="Horários Gerais")
    
    # Campos opcionais (redes sociais)
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook")
    youtube = models.URLField(blank=True, null=True, verbose_name="YouTube")
    
    # Campos de controle
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nome_fantasia']
    
    def __str__(self):
        return self.nome_fantasia
    
    def get_endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f" - {self.complemento}"
        endereco += f" - {self.bairro}, {self.municipio}/{self.uf} - CEP: {self.cep}"
        return endereco
    
    def get_telefones(self):
        """Retorna todos os telefones ativos"""
        telefones = [self.telefone1]
        if self.telefone2:
            telefones.append(self.telefone2)
        return telefones
    
    def get_horarios_formatados(self):
        """Retorna os horários formatados por dia da semana"""
        dias_semana = {
            'Segunda-feira': self.segunda_feira,
            'Terça-feira': self.terca_feira,
            'Quarta-feira': self.quarta_feira,
            'Quinta-feira': self.quinta_feira,
            'Sexta-feira': self.sexta_feira,
            'Sábado': self.sabado,
            'Domingo': self.domingo
        }
        
        horarios = []
        for dia, horario in dias_semana.items():
            if horario:
                horarios.append(f"{dia}: {horario}")
        
        return horarios
    
    def get_horarios_ativos(self):
        """Retorna apenas os dias com horários definidos"""
        return self.get_horarios_formatados()


class MensagemContato(models.Model):
    """Modelo para armazenar mensagens de contato"""
    
    ASSUNTO_CHOICES = [
        ('matricula', 'Matrícula'),
        ('projeto_social', 'Projeto Social'),
        ('horarios', 'Horários'),
        ('precos', 'Preços'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    assunto = models.CharField(max_length=50, choices=ASSUNTO_CHOICES, verbose_name="Assunto")
    mensagem = models.TextField(verbose_name="Mensagem")
    
    # Campos de controle
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    lida = models.BooleanField(default=False, verbose_name="Mensagem Lida")
    respondida = models.BooleanField(default=False, verbose_name="Respondida")
    
    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"{self.nome} - {self.assunto} ({self.data_envio.strftime('%d/%m/%Y %H:%M')})"

class TermosCondicoes(models.Model):
    TIPO_CHOICES = [
        ('responsabilidade', 'Termos de Responsabilidade'),
        ('medicas', 'Termos de Condições Médicas'),
        ('imagem', 'Direito de Uso de Imagem'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(help_text="Use {{NOME_EMPRESA}}, {{DATA_ATUAL}}, {{RESPONSAVEL}} como variáveis")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Termos e Condições"
        verbose_name_plural = "Termos e Condições"
        ordering = ['tipo']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"
    
    def get_conteudo_processado(self, **kwargs):
        """
        Processa o conteúdo substituindo variáveis pelos valores fornecidos
        """
        conteudo = self.conteudo
        
        # Substituições padrão
        from django.utils import timezone
        conteudo = conteudo.replace('{{DATA_ATUAL}}', timezone.now().strftime('%d/%m/%Y'))
        
        # Substituições personalizadas
        for key, value in kwargs.items():
            conteudo = conteudo.replace(f'{{{{{key}}}}}', str(value))
        
        return conteudo
