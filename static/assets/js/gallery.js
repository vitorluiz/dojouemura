// ===== DOJÔ UEMURA - GALERIA INTERATIVA =====

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== GALERIA INTERATIVA COM MODAL =====
    const galleryCards = document.querySelectorAll('.gallery-card');
    const modalGalleryContent = document.getElementById('modalGalleryContent');
    
    // Dados das galerias para cada evento
    const galleryData = {
        'graduacao-julho': {
            title: 'Graduação Julho 2025',
            location: 'Dojô Uemura',
            images: [
                { src: '/static/assets/img/galeria/dojo_imagem_01.jpg', alt: 'Graduação 1', caption: 'Cerimônia de graduação' },
                { src: '/static/assets/img/galeria/dojo_imagem_02.jpg', alt: 'Graduação 2', caption: 'Entrega de faixas' },
                { src: '/static/assets/img/galeria/dojo_imagem_03.jpg', alt: 'Graduação 3', caption: 'Festa de comemoração' },
                { src: '/static/assets/img/galeria/dojo_imagem_04.jpg', alt: 'Graduação 4', caption: 'Grupo de formandos' },
                { src: '/static/assets/img/galeria/dojo_imagem_05.jpg', alt: 'Graduação 5', caption: 'Momentos especiais' },
                { src: '/static/assets/img/galeria/dojo_imagem_06.jpg', alt: 'Graduação 6', caption: 'Família unida' }
            ]
        },
        'competicao-marco': {
            title: 'Competição Março 2025',
            location: 'Ginásio Municipal',
            images: [
                { src: '/static/assets/img/galeria/dojo_imagem_07.jpg', alt: 'Competição 1', caption: 'Aquecimento' },
                { src: '/static/assets/img/galeria/dojo_imagem_08.jpg', alt: 'Competição 2', caption: 'Lutas emocionantes' },
                { src: '/static/assets/img/galeria/dojo_imagem_09.jpg', alt: 'Competição 3', caption: 'Pódio' },
                { src: '/static/assets/img/galeria/dojo_imagem_10.jpg', alt: 'Competição 4', caption: 'Equipe vencedora' },
                { src: '/static/assets/img/galeria/dojo_imagem_11.jpg', alt: 'Competição 5', caption: 'Celebração' },
                { src: '/static/assets/img/galeria/dojo_imagem_12.jpg', alt: 'Competição 6', caption: 'Troféus' }
            ]
        },
        'treino-especial': {
            title: 'Treino Especial Maio 2025',
            location: 'Dojô Uemura',
            images: [
                { src: '/static/assets/img/galeria/dojo_imagem_01.jpg', alt: 'Treino 1', caption: 'Aula especial' },
                { src: '/static/assets/img/galeria/dojo_imagem_02.jpg', alt: 'Treino 2', caption: 'Técnicas avançadas' },
                { src: '/static/assets/img/galeria/dojo_imagem_03.jpg', alt: 'Treino 3', caption: 'Mestre convidado' },
                { src: '/static/assets/img/galeria/dojo_imagem_04.jpg', alt: 'Treino 4', caption: 'Grupo unido' },
                { src: '/static/assets/img/galeria/dojo_imagem_05.jpg', alt: 'Treino 5', caption: 'Aprendizado' },
                { src: '/static/assets/img/galeria/dojo_imagem_06.jpg', alt: 'Treino 6', caption: 'Momento especial' }
            ]
        },
        'campeonato-junho': {
            title: 'Campeonato Junho 2025',
            location: 'Arena Esportiva',
            images: [
                { src: '/static/assets/img/galeria/dojo_imagem_07.jpg', alt: 'Campeonato 1', caption: 'Aquecimento' },
                { src: '/static/assets/img/galeria/dojo_imagem_08.jpg', alt: 'Campeonato 2', caption: 'Lutas emocionantes' },
                { src: '/static/assets/img/galeria/dojo_imagem_09.jpg', alt: 'Campeonato 3', caption: 'Pódio' },
                { src: '/static/assets/img/galeria/dojo_imagem_10.jpg', alt: 'Campeonato 4', caption: 'Equipe vencedora' },
                { src: '/static/assets/img/galeria/dojo_imagem_11.jpg', alt: 'Campeonato 5', caption: 'Celebração' },
                { src: '/static/assets/img/galeria/dojo_imagem_12.jpg', alt: 'Campeonato 6', caption: 'Troféus' }
            ]
        }
    };
    
    // Adicionar eventos de clique aos cards da galeria
    galleryCards.forEach(card => {
        card.addEventListener('click', function() {
            const eventId = this.dataset.event;
            const eventData = galleryData[eventId];
            
            if (eventData && modalGalleryContent) {
                openGalleryModal(eventData);
            }
        });
    });
    
    // Função para abrir modal da galeria
    function openGalleryModal(eventData) {
        // Criar conteúdo do modal
        let modalHTML = `
            <div class="modal-header">
                <h5 class="modal-title">${eventData.title}</h5>
                <p class="modal-subtitle text-muted mb-0">${eventData.location}</p>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="gallery-grid">
        `;
        
        // Adicionar imagens
        eventData.images.forEach(image => {
            modalHTML += `
                <div class="gallery-item" data-caption="${image.caption}">
                    <img src="${image.src}" alt="${image.alt}" class="img-fluid rounded">
                    <div class="gallery-caption">
                        <p class="mb-0">${image.caption}</p>
                    </div>
                </div>
            `;
        });
        
        modalHTML += `
                </div>
            </div>
        `;
        
        // Atualizar modal
        modalGalleryContent.innerHTML = modalHTML;
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('galleryModal'));
        modal.show();
        
        // Adicionar eventos de clique nas imagens
        const galleryItems = modalGalleryContent.querySelectorAll('.gallery-item');
        galleryItems.forEach(item => {
            item.addEventListener('click', function() {
                const caption = this.dataset.caption;
                const img = this.querySelector('img');
                
                // Mostrar caption em tooltip ou modal menor
                showImageCaption(img.src, caption);
            });
        });
    }
    
    // Função para mostrar caption da imagem
    function showImageCaption(imageSrc, caption) {
        // Criar modal para imagem individual
        const imageModal = document.createElement('div');
        imageModal.className = 'modal fade';
        imageModal.id = 'imageModal';
        imageModal.innerHTML = `
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h6 class="modal-title">${caption}</h6>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <img src="${imageSrc}" alt="${caption}" class="img-fluid rounded">
                    </div>
                </div>
            </div>
        `;
        
        // Adicionar ao DOM
        document.body.appendChild(imageModal);
        
        // Mostrar modal
        const modal = new bootstrap.Modal(imageModal);
        modal.show();
        
        // Remover modal do DOM após fechar
        imageModal.addEventListener('hidden.bs.modal', function() {
            document.body.removeChild(imageModal);
        });
    }
    
    // ===== FILTROS DE GALERIA =====
    const filterButtons = document.querySelectorAll('.gallery-filter');
    const allGalleryItems = document.querySelectorAll('.gallery-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Atualizar botões ativos
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filtrar itens
            allGalleryItems.forEach(item => {
                if (filter === 'all' || item.dataset.category === filter) {
                    item.style.display = 'block';
                    item.classList.add('animate-fade-in');
                } else {
                    item.style.display = 'none';
                    item.classList.remove('animate-fade-in');
                }
            });
        });
    });
    
    // ===== LAZY LOADING PARA IMAGENS DA GALERIA =====
    const galleryImages = document.querySelectorAll('.gallery-item img');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            }
        });
    });
    
    galleryImages.forEach(img => {
        if (img.dataset.src) {
            imageObserver.observe(img);
        }
    });
    
    // ===== ZOOM NAS IMAGENS =====
    const zoomableImages = document.querySelectorAll('.gallery-item img[data-zoom]');
    zoomableImages.forEach(img => {
        img.addEventListener('click', function() {
            if (this.classList.contains('zoomed')) {
                this.classList.remove('zoomed');
            } else {
                // Remover zoom de outras imagens
                zoomableImages.forEach(otherImg => otherImg.classList.remove('zoomed'));
                this.classList.add('zoomed');
            }
        });
    });
    
    // ===== DOWNLOAD DE IMAGENS =====
    const downloadButtons = document.querySelectorAll('.gallery-download');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const imageSrc = this.dataset.image;
            const imageName = this.dataset.filename || 'imagem.jpg';
            
            // Criar link de download
            const link = document.createElement('a');
            link.href = imageSrc;
            link.download = imageName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    });
});
