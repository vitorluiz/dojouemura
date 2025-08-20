from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Atleta
from utils.validacoes import validar_cpf
import re

# Constantes de choices para o formulário
SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
]

ESTADO_CIVIL_CHOICES = [
    ('solteiro', 'Solteiro(a)'),
    ('casado', 'Casado(a)'),
    ('divorciado', 'Divorciado(a)'),
    ('viuvo', 'Viúvo(a)'),
]

TIPO_SANGUINEO_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

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


class UsuarioRegistroForm(forms.ModelForm):
    """Formulário de registro de usuário"""
    
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primeiro nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXX.XXX.XXX-XX',
            'data-mask': '000.000.000-00'
        })
    )
    
    telefone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(XX) XXXXX-XXXX',
            'data-mask': '(00) 00000-0000'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'data_nascimento', 'cpf', 'telefone')
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remover caracteres especiais
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            
            # Verificar se já existe
            if Usuario.objects.filter(cpf=cpf).exists():
                raise ValidationError('Este CPF já está cadastrado.')
            
            # Usar validação real de CPF
            try:
                validar_cpf(cpf)
            except ValidationError as e:
                raise ValidationError(f'CPF inválido: {e.message}')
            
            # Formatar CPF
            if len(cpf_limpo) == 11:
                return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remover caracteres especiais
            telefone_limpo = re.sub(r'[^0-9]', '', telefone)
            
            # Formatar telefone
            if len(telefone_limpo) == 11:
                return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
            elif len(telefone_limpo) == 10:
                return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone


class UsuarioLoginForm(forms.Form):
    """Formulário de login"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )


class AtletaForm(forms.ModelForm):
    """Formulário de cadastro/edição de atleta"""
    
    nome = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome completo do atleta'
        })
    )
    
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXX.XXX.XXX-XX',
            'data-mask': '000.000.000-00'
        })
    )
    
    rg = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'RG (opcional)'
        })
    )
    
    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    estado_civil = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    parentesco = forms.ChoiceField(
        choices=PARENTESCO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    foto = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Foto do atleta (opcional)'
    )
    
    cep = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXXX-XXX',
            'data-mask': '00000-000',
            'id': 'id_cep'
        })
    )
    
    endereco = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, Avenida, etc.',
            'id': 'id_endereco'
        })
    )
    
    numero = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número'
        })
    )
    
    complemento = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartamento, bloco, etc. (opcional)'
        })
    )
    
    bairro = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bairro',
            'id': 'id_bairro'
        })
    )
    
    cidade = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade',
            'id': 'id_cidade'
        })
    )
    
    estado = forms.CharField(
        max_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estado',
            'id': 'id_estado',
            'style': 'text-transform: uppercase;'
        })
    )
    
    escolaridade = forms.ChoiceField(
        choices=ESCOLARIDADE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    escola = forms.ChoiceField(
        choices=[
            ('', 'Selecione a escola...'),
            ('Escola Municipal Água Branca', 'Escola Municipal Água Branca'),
            ('Escola Municipal Casca III', 'Escola Municipal Casca III'),
            ('Escola Municipal Córrego do Campo', 'Escola Municipal Córrego do Campo'),
            ('Escola Municipal Cristo Rei', 'Escola Municipal Cristo Rei'),
            ('Escola Municipal JJ', 'Escola Municipal JJ'),
            ('Escola Municipal Monteiro Lobato', 'Escola Municipal Monteiro Lobato'),
            ('Escola Municipal Professor Jacondino Bezerra', 'Escola Municipal Professor Jacondino Bezerra'),
            ('Escola Municipal Professora Abinel Freitas Pereira', 'Escola Municipal Professora Abinel Freitas Pereira'),
            ('Escola Municipal Professora Elba Xavier Ferreira', 'Escola Municipal Professora Elba Xavier Ferreira'),
            ('Escola Municipal Professora Irene Ferreira da Silva', 'Escola Municipal Professora Irene Ferreira da Silva'),
            ('Escola Municipal Professora Maria Luiza de Araújo Gomes', 'Escola Municipal Professora Maria Luiza de Araújo Gomes'),
            ('Escola Municipal Santa Helena', 'Escola Municipal Santa Helena'),
            ('Escola Municipal Thermozina de Siqueira', 'Escola Municipal Thermozina de Siqueira'),
            ('Escola Estadual Cel Rafael de Siqueira', 'Escola Estadual Cel Rafael de Siqueira'),
            ('Escola Estadual Professor Ana Tereza Albernaz', 'Escola Estadual Professor Ana Tereza Albernaz'),
            ('Escola Estadual Reunidas de Cachoeira Rica', 'Escola Estadual Reunidas de Cachoeira Rica'),
            ('Escola Estadual São José', 'Escola Estadual São José'),
            ('Colégio Tales de Mileto', 'Colégio Tales de Mileto'),
            ('Centro Educacional Sebastião Albernaz', 'Centro Educacional Sebastião Albernaz'),
            ('outra', 'Outra escola (especificar)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    serie = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Série/Ano (opcional)'
        })
    )
    
    turno = forms.ChoiceField(
        choices=TURNO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    tipo_sanguineo = forms.ChoiceField(
        choices=TIPO_SANGUINEO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    alergias = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ex: Pólen, alimentos, medicamentos... (opcional)'
        })
    )
    
    condicoes_medicas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descreva qualquer condição médica relevante para a prática de esportes (opcional)'
        })
    )
    
    termo_responsabilidade = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        error_messages={
            'required': 'É obrigatório aceitar os termos de responsabilidade.'
        }
    )
    
    termo_uso_imagem = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        error_messages={
            'required': 'É obrigatório autorizar o uso de imagem.'
        }
    )
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Atleta
        fields = [
            'nome', 'data_nascimento', 'cpf', 'rg', 'sexo', 'estado_civil', 'parentesco', 'foto',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'escolaridade', 'escola', 'serie', 'turno',
            'tipo_sanguineo', 'alergias', 'condicoes_medicas', 
            'termo_responsabilidade', 'termo_uso_imagem'
        ]
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            return cpf


        # limpa só números
        cpf_numeros = re.sub(r'[^0-9]', '', cpf)
        if len(cpf_numeros) != 11:
            raise ValidationError('Formato de CPF inválido.')

        # formata de volta
        cpf_formatado = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        
        # checa duplicata para ESTE USUÁRIO
        if Atleta.objects.filter(usuario=self.usuario, cpf=cpf_formatado).exists():
            raise ValidationError('Você já cadastrou um atleta com este CPF.')

        return cpf_formatado

    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remover caracteres especiais
            cep_limpo = re.sub(r'[^0-9]', '', cep)
            
            # Formatar CEP
            if len(cep_limpo) == 8:
                return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
        
        return cep
    
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            return estado.upper()
        return estado

