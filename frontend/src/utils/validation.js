// src/utils/validation.js

/**
 * Utilitários de validação para formulários
 */

/**
 * Valida CPF
 * @param {string} cpf - CPF para validar
 * @returns {boolean} - True se válido
 */
export const validarCPF = (cpf) => {
  // Remove caracteres não numéricos
  const cpfLimpo = cpf.replace(/\D/g, '');
  
  // Verifica se tem 11 dígitos
  if (cpfLimpo.length !== 11) return false;
  
  // Verifica se todos os dígitos são iguais
  if (/^(\d)\1{10}$/.test(cpfLimpo)) return false;
  
  // Validação do primeiro dígito verificador
  let soma = 0;
  for (let i = 0; i < 9; i++) {
    soma += parseInt(cpfLimpo.charAt(i)) * (10 - i);
  }
  let resto = 11 - (soma % 11);
  let digito1 = resto < 2 ? 0 : resto;
  
  if (parseInt(cpfLimpo.charAt(9)) !== digito1) return false;
  
  // Validação do segundo dígito verificador
  soma = 0;
  for (let i = 0; i < 10; i++) {
    soma += parseInt(cpfLimpo.charAt(i)) * (11 - i);
  }
  resto = 11 - (soma % 11);
  let digito2 = resto < 2 ? 0 : resto;
  
  return parseInt(cpfLimpo.charAt(10)) === digito2;
};

/**
 * Valida CNPJ
 * @param {string} cnpj - CNPJ para validar
 * @returns {boolean} - True se válido
 */
export const validarCNPJ = (cnpj) => {
  const cnpjLimpo = cnpj.replace(/\D/g, '');
  
  if (cnpjLimpo.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(cnpjLimpo)) return false;
  
  // Validação do primeiro dígito verificador
  let soma = 0;
  let peso = 2;
  for (let i = 11; i >= 0; i--) {
    soma += parseInt(cnpjLimpo.charAt(i)) * peso;
    peso = peso === 9 ? 2 : peso + 1;
  }
  let resto = soma % 11;
  let digito1 = resto < 2 ? 0 : 11 - resto;
  
  if (parseInt(cnpjLimpo.charAt(12)) !== digito1) return false;
  
  // Validação do segundo dígito verificador
  soma = 0;
  peso = 2;
  for (let i = 12; i >= 0; i--) {
    soma += parseInt(cnpjLimpo.charAt(i)) * peso;
    peso = peso === 9 ? 2 : peso + 1;
  }
  resto = soma % 11;
  let digito2 = resto < 2 ? 0 : 11 - resto;
  
  return parseInt(cnpjLimpo.charAt(13)) === digito2;
};

/**
 * Valida email
 * @param {string} email - Email para validar
 * @returns {boolean} - True se válido
 */
export const validarEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

/**
 * Valida telefone brasileiro
 * @param {string} telefone - Telefone para validar
 * @returns {boolean} - True se válido
 */
export const validarTelefone = (telefone) => {
  const telefoneLimpo = telefone.replace(/\D/g, '');
  // Aceita telefones com 10 ou 11 dígitos (com ou sem 9 no celular)
  return telefoneLimpo.length >= 10 && telefoneLimpo.length <= 11;
};

/**
 * Valida CEP
 * @param {string} cep - CEP para validar
 * @returns {boolean} - True se válido
 */
export const validarCEP = (cep) => {
  const cepLimpo = cep.replace(/\D/g, '');
  return cepLimpo.length === 8;
};

/**
 * Valida data de nascimento
 * @param {string} data - Data no formato YYYY-MM-DD
 * @returns {boolean} - True se válido
 */
export const validarDataNascimento = (data) => {
  if (!data) return false;
  
  const hoje = new Date();
  const nascimento = new Date(data);
  
  // Verifica se a data é válida
  if (isNaN(nascimento.getTime())) return false;
  
  // Verifica se não é uma data futura
  if (nascimento > hoje) return false;
  
  // Verifica se a pessoa tem pelo menos 3 anos e no máximo 120 anos
  const idade = hoje.getFullYear() - nascimento.getFullYear();
  return idade >= 3 && idade <= 120;
};

/**
 * Valida se um campo obrigatório está preenchido
 * @param {string} valor - Valor para validar
 * @returns {boolean} - True se válido
 */
export const validarCampoObrigatorio = (valor) => {
  return valor && valor.toString().trim().length > 0;
};

/**
 * Valida arquivo de imagem
 * @param {File} arquivo - Arquivo para validar
 * @returns {object} - {valido: boolean, erro: string}
 */
export const validarArquivoImagem = (arquivo) => {
  if (!arquivo) {
    return { valido: false, erro: 'Nenhum arquivo selecionado' };
  }
  
  // Verifica o tipo do arquivo
  const tiposPermitidos = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  if (!tiposPermitidos.includes(arquivo.type)) {
    return { valido: false, erro: 'Formato de arquivo não permitido. Use JPEG, PNG ou WebP.' };
  }
  
  // Verifica o tamanho (máximo 5MB)
  const tamanhoMaximo = 5 * 1024 * 1024; // 5MB em bytes
  if (arquivo.size > tamanhoMaximo) {
    return { valido: false, erro: 'Arquivo muito grande. Tamanho máximo: 5MB.' };
  }
  
  return { valido: true, erro: null };
};

/**
 * Formata CPF
 * @param {string} cpf - CPF para formatar
 * @returns {string} - CPF formatado
 */
export const formatarCPF = (cpf) => {
  const cpfLimpo = cpf.replace(/\D/g, '');
  return cpfLimpo.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

/**
 * Formata CNPJ
 * @param {string} cnpj - CNPJ para formatar
 * @returns {string} - CNPJ formatado
 */
export const formatarCNPJ = (cnpj) => {
  const cnpjLimpo = cnpj.replace(/\D/g, '');
  return cnpjLimpo.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};

/**
 * Formata telefone
 * @param {string} telefone - Telefone para formatar
 * @returns {string} - Telefone formatado
 */
export const formatarTelefone = (telefone) => {
  const telefoneLimpo = telefone.replace(/\D/g, '');
  if (telefoneLimpo.length === 11) {
    return telefoneLimpo.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  } else if (telefoneLimpo.length === 10) {
    return telefoneLimpo.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  }
  return telefone;
};

/**
 * Formata CEP
 * @param {string} cep - CEP para formatar
 * @returns {string} - CEP formatado
 */
export const formatarCEP = (cep) => {
  const cepLimpo = cep.replace(/\D/g, '');
  return cepLimpo.replace(/(\d{5})(\d{3})/, '$1-$2');
};

