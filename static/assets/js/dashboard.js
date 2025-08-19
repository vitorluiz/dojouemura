// ===== DOJÔ UEMURA - DASHBOARD JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== CONFIRMAÇÃO DE EXCLUSÃO =====
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este dependente? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });
    
    // ===== TOOLTIPS =====
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ===== POPOVERS =====
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // ===== ANIMAÇÕES DE CARDS =====
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // ===== FILTROS DE TABELA =====
    const searchInput = document.getElementById('search-dependentes');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.table tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                    row.style.animation = 'fadeIn 0.3s ease';
                } else {
                    row.style.animation = 'fadeOut 0.3s ease';
                    setTimeout(() => {
                        row.style.display = 'none';
                    }, 300);
                }
            });
        });
    }
    
    // ===== SORTING DE TABELA =====
    const sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(this.parentElement.children).indexOf(this);
            const isAscending = this.classList.contains('asc');
            
            // Remove classes de ordenação anteriores
            sortableHeaders.forEach(h => {
                h.classList.remove('asc', 'desc');
                h.innerHTML = h.innerHTML.replace(' ▲', '').replace(' ▼', '');
            });
            
            // Adiciona classe e seta
            if (isAscending) {
                this.classList.add('desc');
                this.innerHTML += ' ▼';
                rows.reverse();
            } else {
                this.classList.add('asc');
                this.innerHTML += ' ▲';
                rows.sort((a, b) => {
                    const aValue = a.children[columnIndex].textContent.trim();
                    const bValue = b.children[columnIndex].textContent.trim();
                    return aValue.localeCompare(bValue, 'pt-BR');
                });
            }
            
            // Reaplica as linhas ordenadas
            rows.forEach(row => tbody.appendChild(row));
        });
    });
    
    // ===== EXPANSÃO DE LINHAS =====
    const expandableRows = document.querySelectorAll('.expandable-row');
    expandableRows.forEach(row => {
        const expandButton = row.querySelector('.expand-btn');
        const detailsRow = row.nextElementSibling;
        
        if (expandButton && detailsRow) {
            expandButton.addEventListener('click', function() {
                const isExpanded = detailsRow.style.display === 'table-row';
                
                if (isExpanded) {
                    detailsRow.style.display = 'none';
                    this.innerHTML = '<i class="bi bi-chevron-down"></i>';
                    this.title = 'Expandir detalhes';
                } else {
                    detailsRow.style.display = 'table-row';
                    this.innerHTML = '<i class="bi bi-chevron-up"></i>';
                    this.title = 'Recolher detalhes';
                }
            });
        }
    });
    
    // ===== ATUALIZAÇÃO AUTOMÁTICA =====
    let autoRefreshInterval;
    
    function startAutoRefresh() {
        autoRefreshInterval = setInterval(() => {
            // Atualiza apenas os dados dinâmicos
            updateDashboardStats();
        }, 30000); // 30 segundos
    }
    
    function stopAutoRefresh() {
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
        }
    }
    
    function updateDashboardStats() {
        // Aqui você pode implementar uma chamada AJAX para atualizar as estatísticas
        // Por enquanto, apenas simulamos uma atualização
        console.log('Atualizando estatísticas do dashboard...');
    }
    
    // Inicia atualização automática
    startAutoRefresh();
    
    // Para atualização automática quando a página não está visível
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            stopAutoRefresh();
        } else {
            startAutoRefresh();
        }
    });
    
    // ===== NOTIFICAÇÕES =====
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // ===== EXPORTAR DADOS =====
    const exportButtons = document.querySelectorAll('.btn-export');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const format = this.dataset.format || 'csv';
            const tableId = this.dataset.table || 'dependentes-table';
            
            if (format === 'csv') {
                exportToCSV(tableId);
            } else if (format === 'pdf') {
                exportToPDF(tableId);
            }
        });
    });
    
    function exportToCSV(tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const rows = Array.from(table.querySelectorAll('tr'));
        let csv = '';
        
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('th, td'));
            const rowData = cells.map(cell => {
                let text = cell.textContent.trim();
                // Escapa aspas duplas
                text = text.replace(/"/g, '""');
                return `"${text}"`;
            });
            csv += rowData.join(',') + '\n';
        });
        
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'dependentes.csv';
        link.click();
    }
    
    function exportToPDF(tableId) {
        // Implementar exportação para PDF
        showNotification('Exportação para PDF em desenvolvimento', 'info');
    }
    
    // ===== RESPONSIVIDADE =====
    function handleResponsiveTable() {
        const tables = document.querySelectorAll('.table-responsive');
        tables.forEach(table => {
            const isMobile = window.innerWidth < 768;
            
            if (isMobile) {
                table.classList.add('mobile-table');
            } else {
                table.classList.remove('mobile-table');
            }
        });
    }
    
    // Executa na inicialização e no redimensionamento
    handleResponsiveTable();
    window.addEventListener('resize', handleResponsiveTable);
    
    // ===== ANIMAÇÕES CSS =====
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(10px); }
        }
        
        .mobile-table .table {
            font-size: 0.875rem;
        }
        
        .mobile-table .table th,
        .mobile-table .table td {
            padding: 0.5rem 0.25rem;
        }
    `;
    document.head.appendChild(style);
    
    // ===== INICIALIZAÇÃO FINAL =====
    console.log('Dashboard JavaScript carregado com sucesso!');
    
    // Mostra notificação de carregamento
    showNotification('Dashboard carregado com sucesso!', 'success');
});
