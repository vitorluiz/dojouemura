// src/api/dojoApi.js

// Dados do Dojô que viriam de um backend no futuro
const dojoInfo = {
  cnpj: "59.002.265/0001-71",
  razaoSocial: "UEMURA CENTRO DE TREINAMENTO ESPORTIVO LTDA",
  nomeFantasia: "DOJÔ UEMURA",
  logradouro: "Rod. Emanuel Pinheiro",
  numero: "S/N",
  complemento: "KM 60",
  cep: "78195-000",
  bairro: "Centro",
  municipio: "Chapada dos Guimarães",
  uf: "MT",
  email: "contato@dojouemura.com.br",
  telefone: "(65) 98111-1125",
};

// Função que simula a busca desses dados
export const fetchDojoInfo = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(dojoInfo);
    }, 200); // Simula um pequeno atraso de rede
  });
};