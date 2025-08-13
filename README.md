# 🥋 Dojô Uemura - Sistema de Gestão Completo

## 📋 Visão Geral

O **Dojô Uemura** é um sistema de gestão completo para academias de artes marciais, com foco especial em projetos sociais. O sistema oferece uma interface moderna, responsiva e profissional para gerenciar alunos, professores, modalidades, turmas e muito mais.

## ✨ Características Principais

### 🎨 Frontend Profissional
- **Design Moderno**: Interface inspirada no design japonês com cores vibrantes
- **Totalmente Responsivo**: Funciona perfeitamente em todos os dispositivos
- **Animações Suaves**: Transições e efeitos visuais elegantes
- **Galeria Interativa**: Lightbox para visualização de imagens
- **Navegação Intuitiva**: Menu completo com todas as funcionalidades

### 🏠 Páginas Implementadas
- **Home**: Página principal com hero section e informações gerais
- **Contato**: Formulário de contato e informações da academia
- **Professores**: Perfis dos instrutores com fotos e especialidades
- **Galeria**: Fotos dos eventos, aulas e graduações
- **Modalidades**: Descrição das artes marciais oferecidas
- **Projeto Social**: Informações sobre o programa gratuito
- **Portal do Aluno**: Acesso ao progresso e frequência
- **Painel Administrativo**: Gestão completa da academia

### 🎯 Funcionalidades Administrativas
- **Cadastros**: Alunos, Professores, Modalidades, Turmas
- **Gestão**: Financeiro, Frequência, Mensagens, Estoque
- **Dashboard**: Visão geral e estatísticas
- **Relatórios**: Frequência e progresso dos alunos

## 🚀 Tecnologias Utilizadas

### Frontend
- **HTML5**: Estrutura semântica e acessível
- **CSS3**: Estilos modernos com variáveis CSS e Flexbox/Grid
- **JavaScript ES6+**: Funcionalidades interativas e animações
- **Bootstrap 5**: Framework CSS para layout responsivo
- **Bootstrap Icons**: Ícones vetoriais profissionais

### Backend
- **Django**: Framework Python robusto e seguro
- **SQLite**: Banco de dados para desenvolvimento
- **Python 3.8+**: Linguagem de programação

## 📁 Estrutura do Projeto

```
uemura/
├── cadastro_pessoas/          # Configurações do Django
├── usuarios/                  # App principal
│   ├── templates/            # Templates HTML
│   ├── static/              # Arquivos estáticos
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Lógica de negócio
│   └── urls.py              # Roteamento
├── static/                   # Arquivos estáticos globais
│   └── assets/
│       ├── css/             # Estilos CSS
│       ├── js/              # JavaScript
│       └── img/             # Imagens
├── utils/                    # Utilitários
└── manage.py                 # Script de gerenciamento
```

## 🎨 Design System

### Cores Principais
- **Vermelho Primário**: #FF2C00 (energia e paixão)
- **Dourado Japonês**: #D4AF37 (tradição e excelência)
- **Azul Marinho**: #1B365D (confiança e estabilidade)
- **Verde Floresta**: #2D5016 (crescimento e natureza)

### Tipografia
- **Fonte Principal**: Inter (moderna e legível)
- **Fonte Japonesa**: Noto Sans JP (autenticidade)

### Componentes
- **Cards**: Bordas arredondadas e sombras suaves
- **Botões**: Gradientes e efeitos hover
- **Formulários**: Validação visual e feedback
- **Navegação**: Menu dropdown responsivo

## 🖼️ Galeria de Imagens

O sistema inclui uma galeria interativa com:
- **Lightbox**: Visualização em tela cheia
- **Overlay**: Informações sobre cada imagem
- **Responsividade**: Adaptação automática para mobile
- **Lazy Loading**: Carregamento otimizado

## 📱 Responsividade

### Breakpoints
- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: 320px - 767px

### Recursos Mobile
- Menu hambúrguer colapsável
- Touch gestures para galeria
- Otimização de performance
- Layout adaptativo

## 🎭 Animações e Interações

### Efeitos Visuais
- **Fade In**: Elementos aparecem suavemente
- **Slide**: Movimentos laterais elegantes
- **Hover**: Transformações nos elementos
- **Parallax**: Efeito de profundidade no hero

### JavaScript Interativo
- Scroll suave para links internos
- Observador de interseção para animações
- Sistema de notificações
- Lightbox para galeria
- Botão "voltar ao topo"

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd uemura
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

### Configuração de Imagens

Para usar suas próprias imagens na galeria:

1. Coloque as imagens em `static/assets/img/`
2. Atualize os caminhos no template `home.html`
3. Use o formato: `{% static 'assets/img/sua_imagem.jpg' %}`

## 📊 Funcionalidades do Sistema

### Para Alunos
- Visualização de frequência
- Acompanhamento de progresso
- Comunicação com professores
- Acesso a documentos

### Para Professores
- Gestão de turmas
- Controle de frequência
- Comunicação com alunos
- Relatórios de progresso

### Para Administradores
- Cadastro completo de usuários
- Gestão financeira
- Controle de estoque
- Relatórios gerenciais

## 🎯 Projeto Social

O Dojô Uemura oferece:
- **Aulas gratuitas** de Jiu-Jitsu para crianças
- **Faixa etária**: 6 a 18 anos
- **Requisitos**: Matrícula escolar e responsável legal
- **Horários**: Manhã, tarde e noite
- **Material**: Incluso no projeto

## 🌟 Diferenciais

### Técnicos
- Código limpo e bem documentado
- Arquitetura escalável
- Segurança implementada
- Performance otimizada

### Visuais
- Design único e memorável
- Identidade visual consistente
- Experiência do usuário excepcional
- Acessibilidade implementada

## 🔮 Roadmap Futuro

### Próximas Versões
- [ ] Sistema de pagamentos online
- [ ] App mobile nativo
- [ ] Integração com redes sociais
- [ ] Sistema de gamificação
- [ ] Relatórios avançados
- [ ] API REST para integrações

### Melhorias Planejadas
- [ ] Chat em tempo real
- [ ] Sistema de notificações push
- [ ] Integração com wearables
- [ ] Análise de dados avançada
- [ ] Machine Learning para recomendações

## 🤝 Contribuição

### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Padrões de Código
- Siga as convenções PEP 8 (Python)
- Use nomes descritivos para variáveis
- Documente funções complexas
- Teste suas mudanças

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

### Contato
- **Email**: contato@dojouemura.com
- **Telefone**: (65) 99999-9999
- **Endereço**: Chapada dos Guimarães - MT

### Comunidade
- **GitHub Issues**: Para bugs e sugestões
- **Documentação**: Wiki do projeto
- **Fórum**: Comunidade de desenvolvedores

## 🙏 Agradecimentos

- **VNETWORKS**: Licenciamento e suporte
- **Comunidade Django**: Framework robusto
- **Bootstrap**: Componentes responsivos
- **Contribuidores**: Todos que ajudaram no projeto

---

**Dojô Uemura** - Formando Campeões da Vida 🥋

*Desenvolvido com ❤️ para transformar vidas através das artes marciais*

