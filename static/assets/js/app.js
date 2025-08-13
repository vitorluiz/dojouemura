// ===== DOJÔ UEMURA - JAVASCRIPT INTERATIVO =====

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== SCROLL SUAVE PARA LINKS INTERNOS =====
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Ajuste para o navbar fixo
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ===== ANIMAÇÕES AO SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar elementos com animação
    const animatedElements = document.querySelectorAll('.animate-fade-in-up, .animate-slide-in-left, .animate-slide-in-right');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
        observer.observe(el);
    });
    
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
    
    galleryCards.forEach(card => {
        card.addEventListener('click', function() {
            const eventType = this.getAttribute('data-event');
            const eventData = galleryData[eventType];
            
            if (eventData) {
                // Atualizar título do modal
                document.getElementById('galleryModalLabel').textContent = `${eventData.title} - ${eventData.location}`;
                
                // Limpar conteúdo anterior
                modalGalleryContent.innerHTML = '';
                
                // Adicionar imagens ao modal
                eventData.images.forEach(image => {
                    const imageCol = document.createElement('div');
                    imageCol.className = 'col-lg-4 col-md-6';
                    imageCol.innerHTML = `
                        <div class="modal-gallery-item">
                            <img src="${image.src}" 
                                 alt="${image.alt}" 
                                 class="img-fluid rounded shadow-sm"
                                 style="width: 100%; height: 200px; object-fit: cover; cursor: pointer;">
                            <div class="modal-gallery-caption">
                                <p class="small text-muted mt-2">${image.caption}</p>
                            </div>
                        </div>
                    `;
                    
                                         // Adicionar funcionalidade de lightbox para cada imagem
                     const modalImg = imageCol.querySelector('img');
                     modalImg.addEventListener('click', function() {
                         showLightbox(this.src, this.alt, eventType);
                     });
                    
                    modalGalleryContent.appendChild(imageCol);
                });
            }
        });
    });
    
         // Função para mostrar lightbox com navegação
     function showLightbox(src, alt, eventType) {
         const eventData = galleryData[eventType];
         if (!eventData) return;
         
         let currentImageIndex = eventData.images.findIndex(img => img.src === src);
         if (currentImageIndex === -1) currentImageIndex = 0;
         
         const lightbox = document.createElement('div');
         lightbox.className = 'lightbox-overlay';
         lightbox.innerHTML = `
             <div class="lightbox-content">
                 <button class="lightbox-close">&times;</button>
                 <button class="lightbox-nav lightbox-prev" ${currentImageIndex === 0 ? 'disabled' : ''}>&lt;</button>
                 <button class="lightbox-nav lightbox-next" ${currentImageIndex === eventData.images.length - 1 ? 'disabled' : ''}>&gt;</button>
                 <img src="${src}" alt="${alt}" class="lightbox-image">
                 <div class="lightbox-info">
                     <h4>${eventData.title}</h4>
                     <p>${eventData.location}</p>
                     <p class="lightbox-counter">${currentImageIndex + 1} de ${eventData.images.length}</p>
                     <p class="lightbox-caption">${eventData.images[currentImageIndex].caption}</p>
                 </div>
             </div>
         `;
         
         document.body.appendChild(lightbox);
         document.body.style.overflow = 'hidden';
         
         // Navegação entre imagens
         const prevBtn = lightbox.querySelector('.lightbox-prev');
         const nextBtn = lightbox.querySelector('.lightbox-next');
         const lightboxImage = lightbox.querySelector('.lightbox-image');
         const lightboxCounter = lightbox.querySelector('.lightbox-counter');
         const lightboxCaption = lightbox.querySelector('.lightbox-caption');
         
         function updateImage(index) {
             const image = eventData.images[index];
             lightboxImage.src = image.src;
             lightboxImage.alt = image.alt;
             lightboxCounter.textContent = `${index + 1} de ${eventData.images.length}`;
             lightboxCaption.textContent = image.caption;
             
             // Atualizar estado dos botões
             prevBtn.disabled = index === 0;
             nextBtn.disabled = index === eventData.images.length - 1;
         }
         
         prevBtn.addEventListener('click', function() {
             if (currentImageIndex > 0) {
                 currentImageIndex--;
                 updateImage(currentImageIndex);
             }
         });
         
         nextBtn.addEventListener('click', function() {
             if (currentImageIndex < eventData.images.length - 1) {
                 currentImageIndex++;
                 updateImage(currentImageIndex);
             }
         });
         
         // Navegação por teclado
         document.addEventListener('keydown', function(e) {
             if (e.key === 'Escape') {
                 lightbox.remove();
                 document.body.style.overflow = '';
             } else if (e.key === 'ArrowLeft' && currentImageIndex > 0) {
                 currentImageIndex--;
                 updateImage(currentImageIndex);
             } else if (e.key === 'ArrowRight' && currentImageIndex < eventData.images.length - 1) {
                 currentImageIndex++;
                 updateImage(currentImageIndex);
             }
         });
         
         // Fechar lightbox
         lightbox.addEventListener('click', function(e) {
             if (e.target === lightbox || e.target.classList.contains('lightbox-close')) {
                 lightbox.remove();
                 document.body.style.overflow = '';
             }
         });
     }
    
    // ===== NAVBAR SCROLL EFFECT =====
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // ===== FORMULÁRIO DE CONTATO =====
    const contactForm = document.querySelector('#contato form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simular envio do formulário
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Enviando...';
            submitBtn.disabled = true;
            
            // Simular delay de envio
            setTimeout(() => {
                showNotification('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success');
                this.reset();
                
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
    
    // ===== NOTIFICAÇÕES =====
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Adicionar estilos
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'success' ? '#D1FAE5' : type === 'error' ? '#FEE2E2' : '#DBEAFE'};
            color: ${type === 'success' ? '#065F46' : type === 'error' ? '#991B1B' : '#1E40AF'};
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            z-index: 9999;
            transform: translateX(100%);
            transition: transform 0.3s ease-out;
            max-width: 400px;
        `;
        
        document.body.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Fechar notificação
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            closeNotification();
        });
        
        // Auto-fechar após 5 segundos
        setTimeout(() => {
            closeNotification();
        }, 5000);
        
        function closeNotification() {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }
    }
    
    // ===== COUNTER ANIMATION =====
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        
        updateCounter();
    }
    
    // ===== LAZY LOADING PARA IMAGENS =====
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ===== SCROLL TO TOP BUTTON =====
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    scrollTopBtn.className = 'scroll-top-btn';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--primary-red);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(255, 44, 0, 0.3);
    `;
    
    document.body.appendChild(scrollTopBtn);
    
    // Mostrar/ocultar botão
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.opacity = '1';
            scrollTopBtn.style.visibility = 'visible';
        } else {
            scrollTopBtn.style.opacity = '0';
            scrollTopBtn.style.visibility = 'hidden';
        }
    });
    
    // Scroll to top
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ===== MOBILE MENU TOGGLE =====
    const mobileMenuToggle = document.querySelector('.navbar-toggler');
    const mobileMenu = document.querySelector('.navbar-collapse');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
        });
        
        // Fechar menu ao clicar em um link
        const mobileLinks = mobileMenu.querySelectorAll('.nav-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('show');
            });
        });
    }
    
    // ===== PRELOADER =====
    window.addEventListener('load', function() {
        const preloader = document.querySelector('.preloader');
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 300);
        }
    });
    
    // ===== PARALLAX EFFECT PARA HERO =====
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    console.log('🚀 Dojô Uemura - JavaScript carregado com sucesso!');
});

// ===== ESTILOS CSS DINÂMICOS PARA LIGHTBOX =====
const lightboxStyles = `
    .lightbox-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        animation: fadeIn 0.3s ease-out forwards;
    }
    
    .lightbox-content {
        position: relative;
        max-width: 90%;
        max-height: 90%;
        text-align: center;
    }
    
    .lightbox-image {
        max-width: 100%;
        max-height: 70vh;
        border-radius: 12px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .lightbox-info {
        margin-top: 1rem;
        color: white;
    }
    
    .lightbox-close {
        position: absolute;
        top: -40px;
        right: 0;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
        padding: 0;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.3s ease;
    }
    
    .lightbox-close:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;

// Adicionar estilos ao head
const styleSheet = document.createElement('style');
styleSheet.textContent = lightboxStyles;
document.head.appendChild(styleSheet);
