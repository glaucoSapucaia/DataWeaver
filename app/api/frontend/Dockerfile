# Etapa 1: Construção da aplicação
FROM node:18 AS build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos package.json e package-lock.json
COPY package*.json ./

# Instalar as dependências
RUN npm install

# Copiar o restante dos arquivos do projeto
COPY . .

# Construir a aplicação Vue.js para produção
RUN npm run build

# Etapa 2: Servir a aplicação com Nginx
FROM nginx:alpine

# Copiar os arquivos de build para o diretório de configuração do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expor a porta 80 para acesso à aplicação
EXPOSE 80

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]