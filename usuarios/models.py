from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from utils.get_alphanumeric import get_alphanumeric

from utils.validacoes import validar_cpf, validar_idade_usuario, validar_idade_atleta,buscar_cep,validar_cep
from utils.uuid7 import uuid7


class Usuario(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )

    class TipoConta(models.TextChoices):
        RESPONSAVEL = 'RESPONSAVEL', 'Responsável'
        PROFESSOR = 'PROFESSOR', 'Professor'
        GESTOR = 'GESTOR', 'Gestor'
        FUNCIONARIO = 'FUNCIONARIO', 'Funcionário'
        ADMIN = 'ADMIN', 'Administrador'

    
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
        )

    email_verificado = models.BooleanField(
        default=False,
        verbose_name='Email Verificado',
        help_text='Indica se o email foi verificado pelo usuário'
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        validators=[validar_cpf],
        null=True,
        blank=True
    )
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        validators=[validar_idade_usuario],
        null=True,
        blank=True
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Telefone deve estar no formato (XX) XXXXX-XXXX'
        )],
        null=True,
        blank=True
    )


    tipo_conta = models.CharField(
        max_length=20,
        choices=TipoConta.choices,
        default=TipoConta.RESPONSAVEL,
        verbose_name='Tipo de Conta'
    )

   
    # Usar email como username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    @property
    def nome_completo(self):
        """Retorna o nome completo do usuário"""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def save(self, *args, **kwargs):
        """Salva o usuário e ajusta o tipo de conta para superusuários"""
        # Se for superusuário, definir tipo como ADMIN
        if self.is_superuser:
            self.tipo_conta = self.TipoConta.ADMIN
        
        super().save(*args, **kwargs)


class Atleta(models.Model):
    """Modelo para atletas dos usuários"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    
    PARENTESCO_CHOICES = [
        ('filho', 'Filho(a)'),
        ('enteado', 'Enteado(a)'),
        ('neto', 'Neto(a)'),
        ('sobrinho', 'Sobrinho(a)'),
        ('outro', 'Outro'),
    ]
    
    ESCOLARIDADE_CHOICES = [
        ('fundamental_1', 'Ensino Fundamental I (1º ao 5º ano)'),
        ('fundamental_2', 'Ensino Fundamental II (6º ao 9º ano)'),
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Ensino Técnico'),
    ]
    
    TURNO_CHOICES = [
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
        ('noturno', 'Noturno'),
        ('integral', 'Integral'),
    ]
    
    # Relacionamento com usuário
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='atletas',
        verbose_name='Usuário Responsável'
    )
    codigo_alfanumerico = models.CharField(max_length=9, unique=True, editable=False)

    # Dados pessoais
    nome = models.CharField(
        max_length=200,
        verbose_name='Nome Completo do atleta'
    )
    
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        validators=[validar_idade_atleta]
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        validators=[validar_cpf]
    )
    rg = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='RG'
    )
    sexo = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino')],
        verbose_name='Sexo'
    )
    estado_civil = models.CharField(
        max_length=20,
        choices=[
            ('solteiro', 'Solteiro(a)'),
            ('casado', 'Casado(a)'),
            ('divorciado', 'Divorciado(a)'),
            ('viuvo', 'Viúvo(a)')
        ],
        blank=True,
        verbose_name='Estado Civil'
    )
    parentesco = models.CharField(
        max_length=20,
        choices=PARENTESCO_CHOICES,
        verbose_name='Parentesco'
    )
    
    # Foto
    foto = models.ImageField(
        upload_to='atletas/fotos/',
        verbose_name='Foto',
        help_text='Foto do atleta (obrigatório)',
        null=True,
        blank=True
    )
    # QR Code
    qr_code_imagem = models.ImageField(
        upload_to='atletas/qrcodes/',
        verbose_name='QR Code',
        null=True,
        blank=True,
        help_text='QR Code gerado automaticamente a partir do código do atleta'
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9,
        verbose_name='CEP',
        validators=[validar_cep]
    )
    
    endereco = models.CharField(
        max_length=200,
        verbose_name='Endereço',
        help_text='Será preenchido automaticamente pelo CEP'
        )

    numero = models.CharField(
        max_length=10,
        verbose_name='Número'
        )

    complemento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Complemento'
        )

    bairro = models.CharField(
        max_length=100,
        verbose_name='Bairro',
        help_text='Será preenchido automaticamente pelo CEP'
        )

    cidade = models.CharField(
        max_length=100,
        verbose_name='Cidade',
        help_text='Será preenchido automaticamente pelo CEP'
        )

    estado = models.CharField(
        max_length=2,
        verbose_name='Estado',
        help_text='Será preenchido automaticamente pelo CEP',
        validators=[RegexValidator(
            regex=r'^[A-Z]{2}$',
            message='Estado deve ter 2 letras maiúsculas'
        )]
        )
    
    # Dados escolares
    escolaridade = models.CharField(
        max_length=20,
        choices=ESCOLARIDADE_CHOICES,
        verbose_name='Escolaridade'
        )

    escola = models.CharField(
        max_length=200,
        verbose_name='Escola'
        )
    
    serie = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Série/Ano'
    )
    
    turno = models.CharField(
        max_length=15,
        choices=TURNO_CHOICES,
        verbose_name='Turno'
        )
    
    # Dados médicos e termos
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-')
        ],
        blank=True,
        verbose_name='Tipo Sanguíneo'
    )
    alergias = models.TextField(
        blank=True,
        verbose_name='Alergias'
    )
    condicoes_medicas = models.TextField(
        blank=True,
        verbose_name='Condições Médicas para Prática de Esportes',
        help_text='Descreva qualquer condição médica relevante para a prática de esportes'
    )
    termo_responsabilidade = models.BooleanField(
        default=False,
        verbose_name='Aceito os Termos de Responsabilidade'
    )
    termo_uso_imagem = models.BooleanField(
        default=False,
        verbose_name='Autorizo o Uso de Imagem'
    )
    
    
    # Metadados
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
        )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'cpf'],
                name='unique_atleta_por_usuario'
            )
        ]
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['usuario__first_name', 'data_nascimento']
   
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Validar se os termos foram aceitos
        if not self.termo_responsabilidade:
            raise ValidationError('É obrigatório aceitar os termos de responsabilidade')
        
        if not self.termo_uso_imagem:
            raise ValidationError('É obrigatório autorizar o uso de imagem')
    
    # Dentro da classe Usuario(AbstractUser)
    @property
    def nome_completo(self):
        """Retorna o nome completo do atleta"""
        return self.nome

    @property
    def idade(self):
        """Calcula a idade do atleta"""
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
    
    @property
    def endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.endereco}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f" - {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"
        return endereco
    
    def save(self, *args, **kwargs):
        """Gera um código alfanumérico único e busca dados do CEP antes de salvar.
        Após salvar, garante que a imagem do QR Code exista.
        """
        # Gerar código alfanumérico se não existir
        if not self.codigo_alfanumerico:
            # Loop para garantir que o código gerado seja único
            while True:
                codigo = get_alphanumeric()
                # Verifica se já existe um atleta com este código
                if not Atleta.objects.filter(codigo_alfanumerico=codigo).exists():
                    self.codigo_alfanumerico = codigo
                    break
        
        # Buscar dados do CEP se foi fornecido e os campos de endereço estão vazios
        if self.cep and (not self.endereco or not self.bairro or not self.cidade or not self.estado):
            try:
                from utils.validacoes import buscar_cep
                cep_data = buscar_cep(self.cep.replace('-', ''))
                if cep_data:
                    self.endereco = cep_data.get('logradouro', self.endereco)
                    self.bairro = cep_data.get('bairro', self.bairro)
                    self.cidade = cep_data.get('localidade', self.cidade)
                    self.estado = cep_data.get('uf', self.estado)
            except Exception as e:
                # Se houver erro na busca do CEP, continuar sem preencher automaticamente
                pass
        # Verificar se precisamos gerar o QR Code após salvar (requer ID para path estável)
        precisa_qr = not self.qr_code_imagem

        super().save(*args, **kwargs)

        if precisa_qr:
            try:
                self.gerar_qr_code()
                # Salvar somente o campo do QR para evitar loop
                super().save(update_fields=['qr_code_imagem'])
            except Exception:
                # Em caso de erro ao gerar o QR, não impedir o save do restante
                pass
    
    def buscar_cep_automatico(self):
        """Busca dados do CEP e preenche os campos de endereço automaticamente"""
        if self.cep:
            try:
                from utils.validacoes import buscar_cep
                cep_data = buscar_cep(self.cep.replace('-', ''))
                if cep_data:
                    self.endereco = cep_data.get('logradouro', '')
                    self.bairro = cep_data.get('bairro', '')
                    self.cidade = cep_data.get('localidade', '')
                    self.estado = cep_data.get('uf', '')
                    return True
            except Exception as e:
                return False
        return False

    def gerar_qr_code(self, force: bool = False) -> bool:
        """Gera a imagem do QR Code a partir do codigo_alfanumerico.

        Parameters
        ----------
        force: bool
            Se True, força a geração mesmo que já exista a imagem.

        Returns
        -------
        bool
            True se gerou/salvou, False caso contrário.
        """
        from io import BytesIO
        from django.core.files.base import ContentFile
        try:
            if self.qr_code_imagem and not force:
                return False
            # Import local para evitar dependência em import global
            import qrcode
            from qrcode.constants import ERROR_CORRECT_M

            qr = qrcode.QRCode(
                version=1,
                error_correction=ERROR_CORRECT_M,
                box_size=10,
                border=2,
            )
            qr.add_data(self.codigo_alfanumerico)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f"{self.codigo_alfanumerico}.png"
            self.qr_code_imagem.save(filename, ContentFile(buffer.getvalue()), save=False)
            return True
        except Exception:
            return False

    def __str__(self):
        nome_atleta = self.nome_completo if hasattr(self, 'nome_completo') else "atleta"
        nome_usuario = f"{self.usuario.first_name} {self.usuario.last_name}".strip() or self.usuario.email
        return f"{nome_atleta} ({nome_usuario})"


# MODELOS PARA CHOICES - Permitem gerenciar opções via admin
class Modalidade(models.Model):
    """Modelo para modalidades esportivas disponíveis"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome da Modalidade')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    imagem = models.ImageField(
        upload_to='modalidades/',
        blank=True,
        null=True,
        verbose_name='Imagem da Modalidade',
        help_text='Imagem representativa da modalidade (recomendado: 300x300px)'
    )
    ativa = models.BooleanField(default=True, verbose_name='Modalidade Ativa')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class TipoMatricula(models.Model):
    """Modelo para tipos de matrícula disponíveis"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Tipo')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    gratuito = models.BooleanField(default=False, verbose_name='Matrícula Gratuita')
    taxa_inscricao = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        verbose_name='Taxa de Inscrição'
    )
    ativo = models.BooleanField(default=True, verbose_name='Tipo Ativo')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Tipo de Matrícula'
        verbose_name_plural = 'Tipos de Matrícula'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class StatusMatricula(models.Model):
    """Modelo para status de matrícula disponíveis"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Status')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    cor = models.CharField(
        max_length=7, 
        default='#007bff',
        verbose_name='Cor do Status',
        help_text='Código hexadecimal da cor (ex: #007bff)'
    )
    ativo = models.BooleanField(default=True, verbose_name='Status Ativo')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Status de Matrícula'
        verbose_name_plural = 'Status de Matrícula'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class Matricula(models.Model):
    """Modelo para matrículas dos atletas - permite múltiplas matrículas por atleta"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    atleta = models.ForeignKey(
        'atleta',
        on_delete=models.CASCADE,
        related_name='matriculas',
        verbose_name='Atleta'
    )
    tipo_matricula = models.ForeignKey(
        TipoMatricula,
        on_delete=models.PROTECT,
        verbose_name='Tipo de Matrícula'
    )
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        verbose_name='Modalidade'
    )
    status_matricula = models.ForeignKey(
        StatusMatricula,
        on_delete=models.PROTECT,
        verbose_name='Status da Matrícula'
    )
    data_matricula = models.DateField(
        default=date.today,
        verbose_name='Data da Matrícula'
    )
    data_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Início das Aulas'
    )
    data_fim = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término das Aulas'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Matrícula Ativa'
    )
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['-data_matricula', 'atleta__nome']
        # Um atleta pode ter apenas uma matrícula ativa por modalidade
        unique_together = ['atleta', 'modalidade', 'ativa']
    
    def __str__(self):
        return f"{self.atleta.nome} - {self.modalidade.nome} ({self.tipo_matricula.nome})"
    
    @property
    def duracao_dias(self):
        """Retorna a duração da matrícula em dias"""
        if self.data_inicio and self.data_fim:
            return (self.data_fim - self.data_inicio).days
        return None
    
    @property
    def status_color(self):
        """Retorna a cor do status da matrícula"""
        return self.status_matricula.cor if self.status_matricula else '#007bff'