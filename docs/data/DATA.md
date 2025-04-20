# DataWeaver - Módulo de Processamento de Dados

📌 Data é um módulo Python projetado para extrair, processar e salvar tabelas de arquivos PDF em formato CSV, com suporte para compactação dos arquivos gerados.


## Módulos Principais
**1. PDF Extractor (pdf_extractor.py)**
- Utiliza a biblioteca tabula para extrair tabelas de arquivos PDF.
- Suporte para extração de múltiplas tabelas e páginas específicas.
- Implementa a interface PDFExtractorInterface.

**2. Data Processor (data_processor.py)**
- Processa e concatena múltiplos DataFrames em um único DataFrame.
- Implementa a interface DataProcessorInterface.
- Tratamento de erros com TableProcessingError.

**3. CSV Saver (csv_saver.py)**
- Salva DataFrames em arquivos CSV.
- Configuração de encoding, cabeçalho e índice.
- Implementa a interface CSVSaverInterface.

**4. Table Extractor (table_extractor.py)**  
Coordena o fluxo completo de processamento:
- Extração de tabelas do PDF.
- Processamento dos dados.
- Salvamento em CSV.
- Compactação do arquivo.
- Utiliza o padrão Decorator para compressão com validação e logging.


## 📦 Estrutura do Projeto

```
dataweaver/
├── data/
│   ├── modules/
│   │   ├── interfaces/          # Interfaces para os módulos
│   │   ├── csv_saver.py         # Salvamento de DataFrames em CSV
│   │   ├── data_processor.py    # Processamento de dados
│   │   ├── pdf_extractor.py     # Extração de tabelas de PDFs
│   │   └── table_extractor.py   # Pipeline completo de processamento
```


## 📊 Diagramas

![ClassDiagram](/docs/data/Diagrams/DataWeaverDataClassDiagram.png)
![SequenceDiagram](/docs/data/Diagrams/DataWeaverDataSequenceDiagram.png)
