# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia apenas os arquivos essenciais para instalar as dependências
COPY requirements.txt .

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para dentro do contêiner
COPY . .

# Expõe a porta usada pelo FastAPI (geralmente 8000)
EXPOSE 8000

# Comando para iniciar o servidor FastAPI usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]