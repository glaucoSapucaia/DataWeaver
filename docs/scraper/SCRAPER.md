# DataWeaver - Scraper de PDFs

📌 Código Python que demonstra padrões de projeto, boas práticas de arquitetura e geração de diagramas automatizados para um sistema de scraping e processamento de PDFs.


## 🔍 Funcionalidades

- ✅ Scraping inteligente de links PDF com estratégias configuráveis (Anchor e Paragraph)
- ✅ Download e organização automática de arquivos em diretórios
- ✅ Compactação em ZIP com opções de logging e validação (via Decorator Pattern)
- ✅ Remoção segura de arquivos temporários após processamento
- ✅ Geração de diagramas (Mermaid) para documentação técnica (Sequência e Classes)
- ✅ Injeção de Dependência e Factory Pattern para flexibilidade


## 🛠️ Tecnologias Utilizadas

- Python + Type Hints (para código tipado e claro)
- Requests (HTTP client) + BeautifulSoup4 (HTML parsing)
- Mermaid (diagramas de arquitetura)
- Pytest (testes unitários)

**Design Patterns:**
- Factory Method (criação de serviços)
- Strategy (extração de links PDF)
- Decorator (compressão ZIP com validação/logging)
- Singleton (configurações)


## 📦 Estrutura do Projeto

```
dataweaver/  
└── scraper/  
    └── modules/  
        ├── factories.py           # Factory Pattern (DefaultPDFServiceFactory)  
        ├── file_manager.py        # Gerenciamento de arquivos (Download/Save)  
        ├── pdf_processor.py       # Serviço principal (PDFProcessingService)  
        ├── pdf_scraper.py         # Scraping + estratégias (Anchor/Paragraph)  
        ├── zip_compressor.py      # Compactação ZIP com Decorators  
        └── interfaces/            # Contratos (Interfaces)  
```


## ⚙️ Como Executar

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

**4. Configure o .env**
```bash
ZIP_NAME="CHANGE-ME"
FILTER="CHANGE-ME"
URL="CHANGE-ME"
```



## 📊 Diagramas

![ClassDiagram](/docs/scraper/diagrams/DataWeaverScraperClassDiagram.png)
![SequenceDiagram](/docs/scraper/diagrams/DataWeaverScraperSequenceDiagram.png)
