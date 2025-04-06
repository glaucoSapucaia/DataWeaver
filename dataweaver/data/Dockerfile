# Usa uma imagem base com Python
FROM python:3.10-slim

# Instala Java (requisito para o tabula-py)
RUN apt-get update && \
    apt-get install -y openjdk-11-jre curl && \
    apt-get clean

# Define a variável de ambiente para o Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Instala as bibliotecas Python necessárias
RUN pip install --no-cache-dir pandas tabula-py

# Cria um diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto (se houver)
COPY . /app

# Comando padrão ao rodar o container
CMD ["python"]