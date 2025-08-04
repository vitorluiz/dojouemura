# Sistema de Cadastro de Pessoas

Um sistema web completo desenvolvido em Django para cadastro de usuários responsáveis e seus dependentes, com validações específicas de idade, autenticação por email e integração com API de CEP.

## 🚀 Funcionalidades

### Usuário Responsável
- **Cadastro com validações rigorosas**: Nome completo, email, CPF, telefone e data de nascimento
- **Validação de idade**: Apenas maiores de 18 anos podem se cadastrar
- **Autenticação por email**: Login usando email como username
- **Verificação obrigatória**: Email deve ser verificado antes do primeiro login
- **Validação de CPF**: Algoritmo completo de validação de CPF brasileiro

### Dependentes
- **Cadastro completo**: Dados pessoais, endereço, informações escolares e médicas
- **Validação de idade**: Dependentes devem ter entre 6 e 18 anos
- **Relacionamento**: Cada dependente pertence a um usuário responsável
- **Dados de endereço**: Integração com API ViaCEP para preenchimento automático
- **Informações escolares**: Escolaridade, escola e turno
- **Condições médicas**: Campo para informações relevantes para prática de esportes
- **Termos obrigatórios**: Aceite de termos de responsabilidade e uso de imagem

### Sistema
- **Interface moderna**: Design responsivo com Bootstrap 5
- **Validações em tempo real**: Máscaras de input e validação de CEP
- **Segurança**: Proteção CSRF, validações server-side
- **Usabilidade**: Mensagens de feedback, navegação intuitiva

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript/jQuery
- **Banco de Dados**: SQLite (desenvolvimento)
- **APIs Externas**: ViaCEP para consulta de endereços
- **Validações**: CPF, email, idade, CEP
- **Autenticação**: Sistema customizado do Django

## 📋 Requisitos

- Python 3.11+
- Django 5.2.4
- Requests (para API ViaCEP)
- Conexão com internet (para API de CEP e CDNs)

## 🚀 Como Executar

### 1. Navegue até o diretório do projeto
```bash
cd cadastro_pessoas
```

### 2. Execute as migrações (se necessário)
```bash
python3 manage.py migrate
```

### 3. Inicie o servidor de desenvolvimento
```bash
python3 manage.py runserver 0.0.0.0:8000
```

### 4. Acesse a aplicação
Abra seu navegador e acesse: `http://localhost:8000`

## 📁 Estrutura do Projeto

```
cadastro_pessoas/
├── cadastro_pessoas/          # Configurações do projeto
│   ├── settings.py           # Configurações principais
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # Configuração WSGI
├── usuarios/                 # App principal
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views/Controllers
│   ├── forms.py             # Formulários
│   ├── urls.py              # URLs do app
│   ├── templates/           # Templates HTML
│   │   └── usuarios/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── dashboard.html
│   │       ├── login.html
│   │       ├── registro.html
│   │       ├── cadastrar_dependente.html
│   │       ├── editar_dependente.html
│   │       └── excluir_dependente.html
│   └── migrations/          # Migrações do banco
├── db.sqlite3              # Banco de dados
└── manage.py               # Script de gerenciamento
```

## 🔧 Modelos de Dados

### Usuario (Modelo Customizado)
- `nome_completo`: CharField(200)
- `email`: EmailField(unique=True) - usado como username
- `data_nascimento`: DateField - com validação de maioridade
- `cpf`: CharField(14, unique=True) - com validação de CPF
- `telefone`: CharField(15) - com máscara (XX) XXXXX-XXXX
- `email_verificado`: BooleanField - controla acesso ao sistema

### Dependente
- `usuario`: ForeignKey(Usuario) - relacionamento com responsável
- `nome_completo`: CharField(200)
- `data_nascimento`: DateField - validação entre 6 e 18 anos
- `parentesco`: CharField - choices (filho, enteado, neto, sobrinho, outro)
- **Endereço**:
  - `cep`: CharField(9) - formato XXXXX-XXX
  - `logradouro`: CharField(200)
  - `numero`: CharField(10)
  - `complemento`: CharField(100, opcional)
  - `bairro`: CharField(100)
  - `cidade`: CharField(100)
  - `uf`: CharField(2)
- **Dados Escolares**:
  - `escolaridade`: CharField - choices (fundamental I/II, médio, técnico)
  - `escola`: CharField(200)
  - `turno`: CharField - choices (matutino, vespertino, noturno, integral)
- `condicoes_medicas`: TextField(opcional)
- `termo_responsabilidade`: BooleanField(obrigatório)
- `termo_uso_imagem`: BooleanField(obrigatório)

## 🔐 Validações Implementadas

### Usuário
- **Idade**: Deve ser maior de 18 anos
- **CPF**: Validação completa com dígitos verificadores
- **Email**: Formato válido e único no sistema
- **Telefone**: Formato brasileiro (XX) XXXXX-XXXX

### Dependente
- **Idade**: Entre 6 e 18 anos
- **CEP**: Formato brasileiro XXXXX-XXX
- **UF**: Duas letras maiúsculas
- **Termos**: Obrigatório aceitar ambos os termos

## 🌐 Integração com APIs

### ViaCEP
- **Endpoint**: `https://viacep.com.br/ws/{cep}/json/`
- **Funcionalidade**: Preenchimento automático de endereço
- **Implementação**: JavaScript no frontend + view AJAX no backend
- **Tratamento de erros**: Fallback para preenchimento manual

## 🎨 Interface de Usuário

### Design
- **Framework**: Bootstrap 5.3.0
- **Tema**: Gradiente roxo/azul moderno
- **Responsividade**: Compatível com desktop e mobile
- **Ícones**: Bootstrap Icons
- **Efeitos**: Transições suaves, hover states, cards com sombra

### Páginas
1. **Home**: Apresentação do sistema e funcionalidades
2. **Cadastro**: Formulário de registro de usuário
3. **Login**: Autenticação com email/senha
4. **Dashboard**: Visão geral dos dependentes cadastrados
5. **Cadastrar Dependente**: Formulário completo com seções organizadas
6. **Editar Dependente**: Atualização de dados existentes
7. **Excluir Dependente**: Confirmação de exclusão com avisos

### Recursos de UX
- **Máscaras de input**: CPF, telefone, CEP
- **Preenchimento automático**: Endereço via CEP
- **Validação em tempo real**: Feedback imediato
- **Mensagens de status**: Sucesso, erro, informação
- **Navegação intuitiva**: Breadcrumbs, botões de ação claros

## 📧 Sistema de Email

### Configuração
- **Backend**: Console (desenvolvimento)
- **Produção**: Configurar SMTP real no settings.py

### Funcionalidades
- **Verificação de cadastro**: Email automático com link de ativação
- **Token de segurança**: Geração segura de tokens de verificação
- **Expiração**: Links com validade limitada

## 🔒 Segurança

### Implementadas
- **Proteção CSRF**: Tokens em todos os formulários
- **Validação server-side**: Todas as entradas são validadas
- **Sanitização**: Prevenção de XSS
- **Autenticação**: Sistema robusto do Django
- **Autorização**: Usuários só acessam seus próprios dados

### Recomendações para Produção
- Configurar `DEBUG = False`
- Usar banco de dados robusto (PostgreSQL)
- Configurar HTTPS
- Implementar rate limiting
- Configurar logs de segurança

## 🚀 Deploy

### Desenvolvimento
O projeto está configurado para execução local com:
- `ALLOWED_HOSTS = ['*']`
- SQLite como banco
- Email backend console

### Produção
Para deploy em produção, ajustar:
1. **settings.py**: DEBUG, ALLOWED_HOSTS, banco de dados
2. **Servidor web**: Nginx + Gunicorn
3. **Banco**: PostgreSQL ou MySQL
4. **Email**: Configurar SMTP real
5. **Estáticos**: Configurar coleta de arquivos estáticos

## 📝 Como Usar

### 1. Cadastro de Usuário
1. Acesse a página inicial
2. Clique em "Criar Conta"
3. Preencha todos os dados obrigatórios
4. Verifique seu email
5. Faça login

### 2. Cadastro de Dependente
1. Após login, acesse o dashboard
2. Clique em "Cadastrar Dependente"
3. Preencha os dados pessoais
4. Digite o CEP (preenchimento automático)
5. Complete dados escolares e médicos
6. Aceite os termos obrigatórios
7. Salve o cadastro

### 3. Gerenciamento
- **Visualizar**: Dashboard lista todos os dependentes
- **Editar**: Clique no ícone de lápis
- **Excluir**: Clique no ícone de lixeira (com confirmação)

## 🐛 Solução de Problemas

### Erro de Migração
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Erro de Dependências
```bash
pip3 install django requests
```

### Erro de Porta
Altere a porta no comando runserver:
```bash
python3 manage.py runserver 0.0.0.0:8080
```

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e demonstrativos.

## 👥 Contribuição

Para contribuir com o projeto:
1. Faça um fork
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique a documentação
- Consulte os logs do Django
- Teste em ambiente limpo

---

**Desenvolvido com Django 5.2.4 | Bootstrap 5 | ViaCEP API**

