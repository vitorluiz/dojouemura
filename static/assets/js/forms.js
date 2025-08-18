// ===== DOJÔ UEMURA - FORMULÁRIOS =====

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== MÁSCARAS DE INPUT =====
    
    // Máscara para CPF
    const cpfInputs = document.querySelectorAll('input[name="cpf"], input[name="cpf_busca"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
                e.target.value = value;
            }
        });
    });
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[name="cep"]');
    cepInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 8) {
                value = value.replace(/(\d{5})(\d{3})/, '$1-$2');
                e.target.value = value;
            }
        });
    });
    
    // Máscara para telefone
    const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
    telefoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{2})(\d{4,5})(\d{4})/, '($1) $2-$3');
                e.target.value = value;
            }
        });
    });
    
    // ===== VALIDAÇÃO DE IDADE =====
    
    const dataNascimentoInputs = document.querySelectorAll('input[name="data_nascimento"]');
    dataNascimentoInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Limpar classes de validação
            this.classList.remove('is-valid', 'is-invalid');
            
            // Não validar se campo estiver vazio
            if (!this.value) {
                return;
            }
            
            // Verificar se a data está no formato correto (YYYY-MM-DD)
            const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
            if (!dateRegex.test(this.value)) {
                return; // Formato inválido, não validar
            }
            
            // Verificar se a data é válida
            const nascimento = new Date(this.value);
            if (isNaN(nascimento.getTime())) {
                return; // Data inválida, não validar
            }
            
            // Verificar se a data não é no futuro
            const hoje = new Date();
            if (nascimento > hoje) {
                return; // Data futura, não validar
            }
            
            // Calcular idade
            let idade = hoje.getFullYear() - nascimento.getFullYear();
            const mes = hoje.getMonth() - nascimento.getMonth();
            
            if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
                idade--;
            }
            
            // Validar faixa etária (6-18 anos para projeto social)
            if (this.closest('form').action.includes('projeto-social')) {
                if (idade < 6 || idade > 18) {
                    this.classList.add('is-invalid');
                    alert('Para o projeto social, o dependente deve ter entre 6 e 18 anos.');
                    this.value = '';
                } else {
                    this.classList.add('is-valid');
                }
            } else {
                // Para modalidade paga, mínimo 6 anos
                if (idade < 6) {
                    this.classList.add('is-invalid');
                    alert('O dependente deve ter pelo menos 6 anos.');
                    this.value = '';
                } else {
                    this.classList.add('is-valid');
                }
            }
        });
        
        // Adicionar validação também no evento 'input' para teclado numérico
        input.addEventListener('input', function() {
            // Só validar se o campo tiver 10 caracteres (formato completo: YYYY-MM-DD)
            if (this.value.length === 10) {
                // Simular o evento 'change' para validar
                this.dispatchEvent(new Event('change'));
            }
        });
    });
    
    // ===== INTEGRAÇÃO COM VIACEP =====
    
    const cepInputsViaCep = document.querySelectorAll('input[name="cep"]');
    cepInputsViaCep.forEach(input => {
        input.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            
            if (cep.length === 8) {
                // Mostrar loading
                this.classList.add('loading');
                
                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            // Preencher campos automaticamente
                            const logradouroInput = this.closest('form').querySelector('input[name="logradouro"]');
                            const bairroInput = this.closest('form').querySelector('input[name="bairro"]');
                            const cidadeInput = this.closest('form').querySelector('input[name="cidade"]');
                            const ufInput = this.closest('form').querySelector('input[name="uf"]');
                            
                            if (logradouroInput) logradouroInput.value = data.logradouro;
                            if (bairroInput) bairroInput.value = data.bairro;
                            if (cidadeInput) cidadeInput.value = data.localidade;
                            if (ufInput) ufInput.value = data.uf;
                            
                            // Marcar como válido
                            this.classList.add('is-valid');
                        } else {
                            this.classList.add('is-invalid');
                            alert('CEP não encontrado.');
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao buscar CEP:', error);
                        this.classList.add('is-invalid');
                        alert('Erro ao buscar CEP. Tente novamente.');
                    })
                    .finally(() => {
                        this.classList.remove('loading');
                    });
            }
        });
    });
    
    // ===== VALIDAÇÃO DE FORMULÁRIOS =====
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            let emptyFields = [];
            
            requiredFields.forEach(field => {
                const fieldValue = field.value.trim();
                const fieldName = field.name || field.id || 'Campo sem nome';
                
                if (!fieldValue) {
                    isValid = false;
                    emptyFields.push(fieldName);
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert(`Por favor, preencha todos os campos obrigatórios.\n\nCampos vazios:\n${emptyFields.join('\n')}`);
            }
        });
    });
    
    // ===== ESTADOS DE CARREGAMENTO =====
    
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.id === 'btn-criar-conta') {
                const btnText = this.querySelector('#btn-text');
                const btnLoading = this.querySelector('#btn-loading');
                
                if (btnText && btnLoading) {
                    btnText.classList.add('d-none');
                    btnLoading.classList.remove('d-none');
                    this.disabled = true;
                    this.classList.add('btn-loading');
                }
            }
        });
    });
});
