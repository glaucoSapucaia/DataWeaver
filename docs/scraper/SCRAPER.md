# DataWeaver - Scraper de PDFs

📌 Código Python que demonstra padrões de projeto, boas práticas de arquitetura e geração de diagramas automatizados para um sistema de scraping e processamento de PDFs.


## Módulos Principais
**1. PDF Scraper (pdf_scraper.py)**
- Implementa estratégias de extração de links PDF (anchor e parágrafos) usando BeautifulSoup.
- Padrões: Strategy (PDFExtractionStrategy), Composite (PDFLinkExtractor).
- Classes:
    - RequestsPDFScraper: Coordena HTTP client e estratégias de extração.
    - AnchorPDFExtractionStrategy: Extrai links de tags ``<a>``.
    - ParagraphPDFExtractionStrategy: Busca PDFs em textos com regex.

**2. File Manager (file_manager.py)**
- Gerencia download e armazenamento de arquivos com separação de responsabilidades.
- Padrões: Facade (FileManager), Dependency Injection.
- Componentes:
    - FileDownloader: Baixa arquivos via requests.
    - FileSaver: Salva conteúdo no filesystem.

**3. PDF Processing Service (pdf_processor.py)**
- Orquestra o pipeline completo: extração → download → compressão.
- Padrões: Facade (PDFProcessingService), Decorator (compressão).
- Funcionalidades:
    - Validação e logging via decorators (ValidationZipCompressor, LoggingZipCompressor).

**4. Zip Compressor (zip_compressor.py)**  
- Compacta arquivos em ZIP com tratamento de erros.
- Padrões: Decorator (extensibilidade para validação/logging).
- Classes-chave:
    - ZipCompressor: Implementação base.
    - ZipCompressorDecorator: Classe base para decorators.

**5. Factories (factories.py)**  
- Fornece implementações concretas para todas as interfaces do sistema.
- Padrões: Abstract Factory (DefaultPDFServiceFactory), Composition.
- Componentes fabricados:
    - HTTP Client, Link Extractor, Scraper, File Manager.


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


## 📊 Diagramas

![ClassDiagram](/docs/scraper/diagrams/DataWeaverScraperClassDiagram.png)
![SequenceDiagram](/docs/scraper/diagrams/DataWeaverScraperSequenceDiagram.png)
