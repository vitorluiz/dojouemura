# Galeria Atualizada - Dojô Uemura

## O que foi implementado

### 1. Cards de Eventos
A galeria foi transformada de uma grade simples de imagens para **cards de eventos** com:
- **Título do evento** (ex: "Graduação Julho 2025")
- **Local** (ex: "Dojô Uemura", "Ginásio Municipal")
- **Imagem de apresentação** clicável
- **Descrição** do evento

### 2. Eventos Disponíveis
- **Graduação Julho 2025** - Dojô Uemura
- **Competição Março 2025** - Ginásio Municipal  
- **Treino Especial Maio 2025** - Dojô Uemura
- **Campeonato Junho 2025** - Arena Esportiva

### 3. Funcionalidade Modal
- Cada card é **clicável**
- Abre um **modal responsivo** com todas as fotos do evento
- **6 imagens por evento** organizadas em grade
- Cada imagem no modal é **clicável** para lightbox

### 4. Lightbox
- **Visualização em tela cheia** das imagens
- **Fechamento** com clique fora ou tecla ESC
- **Navegação intuitiva**

## Como funciona

### Para o Usuário
1. **Visualizar cards** na página inicial
2. **Clicar em um card** para ver todas as fotos do evento
3. **Clicar em uma foto** no modal para visualização ampliada
4. **Fechar** com X, clique fora ou ESC

### Para o Desenvolvedor
- **HTML**: Cards com `data-event` para identificação
- **JavaScript**: Dados dos eventos e funcionalidade modal
- **CSS**: Estilos para cards, modal e lightbox

## Estrutura dos Arquivos

### HTML (home.html)
```html
<div class="card gallery-card" data-bs-toggle="modal" data-bs-target="#galleryModal" data-event="graduacao-julho">
    <!-- Conteúdo do card -->
</div>
```

### JavaScript (app.js)
```javascript
const galleryData = {
    'graduacao-julho': {
        title: 'Graduação Julho 2025',
        location: 'Dojô Uemura',
        images: [/* array de imagens */]
    }
    // ... outros eventos
};
```

### CSS (estilo.css)
- `.gallery-card` - Estilos dos cards
- `.modal-gallery-item` - Itens do modal
- `.lightbox-overlay` - Lightbox em tela cheia

## Personalização

### Adicionar Novo Evento
1. **Adicionar card** no HTML com `data-event="novo-evento"`
2. **Adicionar dados** no JavaScript em `galleryData`
3. **Incluir imagens** no diretório `static/assets/img/galeria/`

### Modificar Eventos Existentes
- **Alterar títulos** no JavaScript
- **Trocar imagens** alterando os caminhos
- **Modificar descrições** nos captions

## Responsividade
- **Cards**: 2 por linha em desktop, 1 em mobile
- **Modal**: Tamanho adaptativo (`modal-xl`)
- **Imagens**: 3 por linha no modal, responsivas

## Navegação
- **Menu dropdown** "Modalidades" inclui links para cada evento
- **Scroll suave** para as seções
- **Animações** de hover e transições

## Diferenciais
- **Interface moderna** com cards
- **Organização por eventos** em vez de fotos soltas
- **Modal responsivo** com navegação intuitiva
- **Lightbox** para visualização detalhada
- **Integração** com menu de navegação
