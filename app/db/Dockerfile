# Usa a imagem oficial do PostgreSQL com Alpine (mais leve)
FROM postgres:13-alpine

# Define variáveis de ambiente (podem ser sobrescritas no docker-compose)
ENV POSTGRES_USER=dataweaver
ENV POSTGRES_PASSWORD=senha_segura
ENV POSTGRES_DB=dataweaver

# Copia scripts SQL para inicialização do banco
COPY ./db/init.sql /docker-entrypoint-initdb.d/

# Cria diretório para dados temporários
RUN mkdir -p /var/lib/postgresql/tmp

# Configurações adicionais
RUN chmod -R 750 /var/lib/postgresql/tmp

# Porta padrão do PostgreSQL
EXPOSE 5432

# Health check (opcional mas recomendado)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB

# Comando padrão (já vem na imagem base)
CMD ["postgres"]