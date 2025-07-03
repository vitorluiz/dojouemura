# Usar a imagem oficial do Node.js como base
FROM node:20-alpine

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar apenas os arquivos de configuração de dependência
COPY package.json package-lock.json* ./

# Instalar as dependências do projeto
# Usar npm ci para instalações limpas e consistentes
RUN npm ci --force --legacy-peer-deps

# Copiar o restante do código da aplicação
COPY . . 

# Expor a porta que o React usa
EXPOSE 3000

# Comando para iniciar a aplicação em modo de desenvolvimento
# Usar o comando completo do npm para iniciar o script
CMD ["npm", "run", "start"]
