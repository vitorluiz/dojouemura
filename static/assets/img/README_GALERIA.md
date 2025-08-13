# 📸 Configuração da Galeria - Dojô Uemura

## 🎯 Como Configurar as Imagens da Galeria

### 1. Preparar as Imagens

Para usar suas próprias imagens na galeria, siga estas etapas:

#### Formato Recomendado
- **Formato**: JPG ou PNG
- **Resolução**: Mínimo 800x600px (recomendado 1200x800px)
- **Tamanho**: Máximo 2MB por imagem
- **Qualidade**: Alta (80-90%)

#### Nomenclatura
Use nomes descritivos para facilitar a organização:
```
jiujitsu1.jpg          - Aula de Jiu-Jitsu
jiujitsu2.jpg          - Competição
graduacao1.jpg         - Cerimônia de Graduação
treino1.jpg            - Treino em Grupo
meditacao1.jpg         - Meditação
familia1.jpg           - Evento Familiar
```

### 2. Colocar as Imagens

1. **Copie suas imagens** para o diretório:
   ```
   static/assets/img/
   ```

2. **Ou crie um subdiretório** para organizar melhor:
   ```
   static/assets/img/galeria/
   ```

### 3. Atualizar o Template

No arquivo `usuarios/templates/usuarios/home.html`, localize a seção da galeria e atualize os caminhos:

#### Exemplo com Imagens no Diretório Principal
```html
<img src="{% static 'assets/img/jiujitsu1.jpg' %}" 
     alt="Aula de Jiu-Jitsu" 
     class="img-fluid rounded shadow-sm">
```

#### Exemplo com Imagens em Subdiretório
```html
<img src="{% static 'assets/img/galeria/jiujitsu1.jpg' %}" 
     alt="Aula de Jiu-Jitsu" 
     class="img-fluid rounded shadow-sm">
```

### 4. Estrutura Recomendada

```
static/assets/img/
├── logo.png                    # Logo do Dojô
├── hero.jpg                    # Imagem principal da home
├── favicon-64-64.ico          # Favicon
├── galeria/                    # Subdiretório para galeria
│   ├── jiujitsu1.jpg         # Aula de Jiu-Jitsu
│   ├── jiujitsu2.jpg         # Competição
│   ├── graduacao1.jpg        # Graduação
│   ├── treino1.jpg           # Treino em Grupo
│   ├── meditacao1.jpg        # Meditação
│   └── familia1.jpg          # Evento Familiar
└── README_GALERIA.md          # Este arquivo
```

## 🖼️ Tipos de Imagens Recomendados

### Para a Galeria Principal
- **Aulas**: Fotos de alunos treinando
- **Eventos**: Competições e graduações
- **Comunidade**: Momentos de união e amizade
- **Técnicas**: Demonstrações de movimentos
- **Medalhas**: Conquistas e premiações

### Para o Hero Section
- **Imagem Principal**: Dojô em atividade ou grupo de alunos
- **Resolução**: Mínimo 1920x1080px
- **Formato**: JPG para melhor compressão
- **Contraste**: Boa visibilidade para texto sobreposto

## 🔧 Otimização de Imagens

### Ferramentas Recomendadas
- **Online**: TinyPNG, Compressor.io
- **Desktop**: GIMP, Photoshop, Affinity Photo
- **Mobile**: Snapseed, Lightroom

### Configurações de Otimização
- **Qualidade JPG**: 80-85%
- **Redimensionamento**: Máximo 1200px de largura
- **Compressão**: Manter qualidade visual

## 📱 Responsividade

### Breakpoints de Imagem
- **Desktop**: 1200px+ (imagens originais)
- **Tablet**: 768px-1199px (redimensionar para 800px)
- **Mobile**: 320px-767px (redimensionar para 600px)

### CSS Responsivo
O sistema já inclui CSS responsivo para as imagens:
```css
.gallery-item img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

@media (max-width: 768px) {
    .gallery-item img {
        height: 200px;
    }
}

@media (max-width: 576px) {
    .gallery-item img {
        height: 180px;
    }
}
```

## 🎨 Personalização da Galeria

### Alterar Cores e Estilos
No arquivo `static/assets/css/estilo.css`, você pode personalizar:

```css
.gallery-item {
    border-radius: 16px;        /* Bordas arredondadas */
    transition: 0.3s ease;      /* Velocidade da transição */
}

.gallery-overlay {
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
    color: white;
}
```

### Adicionar Mais Imagens
Para adicionar mais imagens à galeria:

1. **Adicione a imagem** ao diretório
2. **Copie o bloco HTML** da galeria
3. **Atualize o caminho** da imagem
4. **Altere o título** e descrição

## 🚀 Dicas de Performance

### Lazy Loading
O sistema já implementa lazy loading para melhor performance:

```html
<img data-src="{% static 'assets/img/imagem.jpg' %}" 
     alt="Descrição" 
     class="lazy">
```

### Compressão
- Use formatos modernos (WebP quando possível)
- Comprima imagens antes de fazer upload
- Considere diferentes tamanhos para diferentes dispositivos

## 🔍 Solução de Problemas

### Imagem Não Aparece
1. **Verifique o caminho**: Confirme se o arquivo existe
2. **Permissões**: Verifique se o arquivo tem permissões de leitura
3. **Cache**: Limpe o cache do navegador
4. **Console**: Verifique erros no console do navegador

### Imagem Muito Grande
1. **Redimensione**: Use ferramentas de edição de imagem
2. **Comprima**: Reduza a qualidade sem perder muito detalhe
3. **Formato**: Considere usar WebP para melhor compressão

### Galeria Não Funciona
1. **JavaScript**: Verifique se o arquivo `app.js` está carregado
2. **Console**: Procure por erros JavaScript
3. **Dependências**: Confirme se Bootstrap está funcionando

## 📞 Suporte

Para dúvidas sobre a configuração da galeria:
- **Email**: contato@dojouemura.com
- **Documentação**: Consulte o README principal
- **Issues**: Abra uma issue no GitHub

---

**Dojô Uemura** - Transformando vidas através das artes marciais 🥋
