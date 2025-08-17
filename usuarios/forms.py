from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Dependente
from utils.validacoes import validar_cpf
import re


class UsuarioRegistroForm(UserCreationForm):
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


class DependenteForm(forms.ModelForm):
    """Formulário de cadastro/edição de dependente"""
    
    nome_completo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome completo do dependente'
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
    
    parentesco = forms.ChoiceField(
        choices=Dependente.PARENTESCO_CHOICES,
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
        help_text='Foto do dependente (Obrigatória para cadastro de dependentes)'
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
    
    logradouro = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, Avenida, etc.',
            'id': 'id_logradouro'
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
    
    uf = forms.CharField(
        max_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UF',
            'id': 'id_uf',
            'style': 'text-transform: uppercase;'
        })
    )
    
    escolaridade = forms.ChoiceField(
        choices=Dependente.ESCOLARIDADE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    escola = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da escola'
        })
    )
    
    turno = forms.ChoiceField(
        choices=Dependente.TURNO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # NOVOS CAMPOS DE MATRÍCULA
    tipo_matricula = forms.ModelChoiceField(
        queryset=None,  # Será definido no __init__
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_matricula'
        }),
        label='Tipo de Matrícula',
        help_text='Escolha entre Projeto Social (gratuito) ou Modalidade Paga'
    )
    
    modalidade = forms.ModelChoiceField(
        queryset=None,  # Será definido no __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_modalidade'
        }),
        label='Modalidade',
        help_text='Escolha a modalidade esportiva (apenas para matrícula paga)'
    )
    
    status_matricula = forms.ModelChoiceField(
        queryset=None,  # Será definido no __init__
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Status da Matrícula'
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
        
        # Definir querysets para os campos de matrícula
        from .models import TipoMatricula, Modalidade, StatusMatricula
        
        self.fields['tipo_matricula'].queryset = TipoMatricula.objects.filter(ativo=True)
        self.fields['modalidade'].queryset = Modalidade.objects.filter(ativa=True)
        self.fields['status_matricula'].queryset = StatusMatricula.objects.filter(ativo=True)
        
        # Definir valor padrão para status (Pendente)
        status_pendente = StatusMatricula.objects.filter(nome='Pendente').first()
        if status_pendente:
            self.fields['status_matricula'].initial = status_pendente
    
    class Meta:
        model = Dependente
        fields = [
            'nome_completo', 'data_nascimento', 'cpf', 'parentesco', 'foto',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf',
            'escolaridade', 'escola', 'turno',
            'tipo_matricula', 'modalidade', 'status_matricula',
            'condicoes_medicas', 'termo_responsabilidade', 'termo_uso_imagem'
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
        if Dependente.objects.filter(usuario=self.usuario, cpf=cpf_formatado).exists():
            raise ValidationError('Você já cadastrou um dependente com este CPF.')

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
    
    def clean_uf(self):
        uf = self.cleaned_data.get('uf')
        if uf:
            return uf.upper()
        return uf

