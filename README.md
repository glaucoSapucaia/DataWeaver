# DataWeaver
DataWeaver automatiza a extração de dados de PDFs hospedados na web. O sistema busca documentos, extrai tabelas, trata os dados, gera CSVs e os armazena em um banco de dados. Com API e frontend intuitivo, facilita consultas e visualização, tornando o processamento de dados mais rápido e eficiente.  

Testes realizados com dados da **Agência Nacional de Saúde Suplementar**.
- [O Rol de Procedimentos e Eventos em Saúde](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos)

## Documentação
Código e diagramas

- [Scraper Module](/docs/scraper/SCRAPER.md)
- [Data Module](/docs/data/DATA.md)


## 🛠️ Tecnologias Utilizadas
- Python + Type Hints (para código tipado e claro)
- Requests (HTTP client) + BeautifulSoup4 (HTML parsing)
- Pandas
- Tabula-py
- openjdk 11 — Para o uso de tabula-py.
- jpype1 — Para o uso de tabula-py.
- Mermaid (diagramas de arquitetura)
- Unittest + Pytest + cov (testes unitários)
- PEP 8 + Black (guia de estilo oficial do Python)
- Logging


**Design Patterns/SOLID:**
- Interface Segregation Principle (ISP) através de interfaces específicas.
- Dependency Injection para os componentes do pipeline.
- Factory Method (criação de serviços).
- Strategy (extração de links PDF).
- Decorator (compressão ZIP com validação/logging).
- Singleton (configurações).
- Facade: Simplifica interfaces complexas (ex: PDFProcessingService).


## ⚙️ Como Executar

**No Linux:**

Verifique se o openjdk 11 está instalado:

```bash
java --version
```

Caso não esteja instalado, ou exista outra versão no sistema, use:

Para instalação:

```bash
sudo apt install openjdk-11-jdk
```

Para selecionar a versão 11:

```bash
sudo update-alternatives --config java

Existem 2 escolhas para a alternativa java (disponibiliza /usr/bin/java).

  Selecção   Caminho                                      Prioridade Estado
------------------------------------------------------------
  0            /usr/lib/jvm/java-17-openjdk-amd64/bin/java   1711      modo automático
* 1            /usr/lib/jvm/java-11-openjdk-amd64/bin/java   1111      modo manual
  2            /usr/lib/jvm/java-17-openjdk-amd64/bin/java   1711      modo manual

Pressione <enter> para manter a escolha actual[*], ou digite o número da selecção:
```

**No Windows:**  
Instalar o Java Development Kit (JDK):  
- Baixe o JDK (versão mais recente)  
- Execute o instalador e siga as instruções.

Configuração:
- Pressione Win + R, digite sysdm.cpl e clique em OK.
- Vá para a aba "Avançado" e clique em "Variáveis de Ambiente".
- Em "Variáveis do sistema", clique em "Novo" e adicione:
- Nome da variável: ``JAVA_HOME``
- Valor da variável: Caminho da instalação do JDK (ex: C:\Program Files\Eclipse Adoptium\jdk-17.0.2.8-hotspot)
- Edite a variável Path (em "Variáveis do sistema") e adicione: ``%JAVA_HOME%\bin``

**1. Clone o repositório:**
```bash
git clone https://github.com/glaucoSapucaia/DataWeaver .
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Execute o serviço:**
```bash
python3 ./main.py
```
ou
```bash
python ./main.py
```

**4. Configure o .env**
```bash
# SCRAPER
PDF_ZIP_NAME="CHANGE-ME"
FILTER="CHANGE-ME"
URL="CHANGE-ME"

# DATA
CSV_ZIP_NAME="CHANGE-ME"
TARGET_FILE="CHANGE-ME"
```


## 📊 Diagramas

![ClassDiagram](/docs/DataWeaverPipelineClassDiagram.png)
![SequenceDiagram](/docs/DataWeaverPipelineSequenceDiagram.png)


**Desenvolvido com Python e boas práticas de design! 🚀**