// src/services/empresaService.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

/**
 * Serviço para gerenciar as informações da empresa
 * Substitui o antigo dojoApi.js com dados reais do backend
 */
class EmpresaService {
  /**
   * Obtém as informações da empresa do backend
   * @returns {Promise<Object>} Dados da empresa
   */
  async obterInformacoes() {
    try {
      const response = await fetch(`${API_BASE_URL}/manager/info/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.message || 'Erro ao obter informações da empresa');
      }
    } catch (error) {
      console.error('Erro ao buscar informações da empresa:', error);
      
      // Fallback com dados padrão em caso de erro
      return {
        razao_social: "UEMURA CENTRO DE TREINAMENTO ESPORTIVO LTDA",
        nome_fantasia: "DOJÔ UEMURA",
        cnpj: "59.002.265/0001-71",
        logradouro: "Rod. Emanuel Pinheiro",
        numero: "S/N",
        complemento: "KM 60",
        cep: "78195-000",
        bairro: "Centro",
        municipio: "Chapada dos Guimarães",
        uf: "MT",
        email: "contato@dojouemura.com.br",
        telefone: "(65) 98111-1125"
      };
    }
  }

  /**
   * Atualiza as informações da empresa no backend
   * @param {Object} dados - Dados da empresa para atualizar
   * @returns {Promise<Object>} Dados atualizados da empresa
   */
  async atualizarInformacoes(dados) {
    try {
      const response = await fetch(`${API_BASE_URL}/manager/info/update/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados),
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.message || 'Erro ao atualizar informações da empresa');
      }
    } catch (error) {
      console.error('Erro ao atualizar informações da empresa:', error);
      throw error;
    }
  }

  /**
   * Formata o endereço completo da empresa
   * @param {Object} dados - Dados da empresa
   * @returns {string} Endereço formatado
   */
  formatarEndereco(dados) {
    const partes = [
      dados.logradouro,
      dados.numero,
      dados.complemento,
      dados.bairro,
      `${dados.municipio}/${dados.uf}`,
      `CEP: ${dados.cep}`
    ].filter(Boolean);
    
    return partes.join(', ');
  }

  /**
   * Formata o CNPJ
   * @param {string} cnpj - CNPJ sem formatação
   * @returns {string} CNPJ formatado
   */
  formatarCNPJ(cnpj) {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
  }

  /**
   * Formata o CEP
   * @param {string} cep - CEP sem formatação
   * @returns {string} CEP formatado
   */
  formatarCEP(cep) {
    return cep.replace(/^(\d{5})(\d{3})$/, '$1-$2');
  }
}

// Exporta uma instância única do serviço
const empresaService = new EmpresaService();
export default empresaService;

// Também exporta a função fetchDojoInfo para compatibilidade com o código existente
export const fetchDojoInfo = () => empresaService.obterInformacoes();

