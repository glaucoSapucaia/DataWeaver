# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de dependências (se houver)
COPY requirements.txt .  

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt  

# Copia os arquivos do script para dentro do contêiner
COPY . .

# Define o comando padrão para rodar o script
CMD ["python", "script.py"]