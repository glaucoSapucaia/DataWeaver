from dataweaver.utils import ensure_directory_exists, get_env_variable

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DirectoryConfig:
    """Configuração de diretórios da aplicação (Princípio da Responsabilidade Única)"""

    # PROJECT
    root: Path  # Diretório raiz do projeto
    tests: Path  # Pasta de testes
    logs: Path  # Pasta de arquivos de log

    # SCRAPER
    pdfs: Path  # Pasta para armazenar PDFs
    modules_scraper: Path  # Pasta dos módulos do scraper

    # DATA
    csv: Path  # Pasta de dados CSV
    modules_data: Path  # Pasta dos módulos do data

    @classmethod
    def create(cls) -> "DirectoryConfig":
        """Método factory para criação da configuração de diretórios"""
        root = Path(__file__).resolve().parent.parent.parent
        return cls(
            # PROJECT
            root=root,
            tests=root / "dataweaver" / "scraper" / "tests",
            logs=root / "dataweaver" / "logs",
            # SCRAPER
            pdfs=root / "dataweaver" / "scraper" / "pdfs",
            modules_scraper=root / "dataweaver" / "scraper" / "modules",
            # DATA
            csv=root / "dataweaver" / "data" / "csv",
            modules_data=root / "dataweaver" / "data" / "modules",
        )


@dataclass
class LoggingConfig:
    """Configuração dos arquivos de log (Separação de Responsabilidades)"""

    log_dir: Path  # Diretório base para logs
    app_log: Path  # Arquivo de log principal
    error_log: Path  # Arquivo de log de erros
    warning_log: Path  # Arquivo de log de avisos

    @classmethod
    def create(cls, log_dir: Path) -> "LoggingConfig":
        """Método factory para criação da configuração de logs"""
        return cls(
            log_dir=log_dir,
            app_log=log_dir / "app.log",
            error_log=log_dir / "error.log",
            warning_log=log_dir / "warning.log",
        )


@dataclass
class ScraperConfig:
    """Configuração específica para o scraper"""

    zip_name: str  # Nome do arquivo ZIP para compactação
    filter: str  # Filtro para busca de documentos
    url: str  # URL base para scraping

    @classmethod
    def create(cls) -> "ScraperConfig":
        """Método factory para criação da configuração do scraper"""
        return cls(
            zip_name=get_env_variable("PDF_ZIP_NAME", "pdfs_compactados.zip"),
            filter=get_env_variable("FILTER", "ANEXO"),
            url=get_env_variable(
                "URL",
                "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
            ),
        )


@dataclass
class DataConfig:
    """Configuração específica para o data"""

    zip_name: str  # Nome do arquivo ZIP para compactação
    target_file: str  # Nome do arqvuios pdf para extração de tabelas

    @classmethod
    def create(cls) -> "DataConfig":
        """Método factory para criação da configuração do data"""
        return cls(
            zip_name=get_env_variable("CSV_ZIP_NAME", "csv_compactados.zip"),
            target_file=get_env_variable(
                "TARGET_FILE", "copy3_of_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
            ),
        )


class AppConfig:
    """Classe principal de configuração (Padrão Facade)"""

    _instance = None  # Variável de classe para o padrão Singleton

    def __new__(cls) -> "AppConfig":
        """Implementação do padrão Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Inicializa todas as configurações da aplicação"""
        self.dirs = DirectoryConfig.create()  # Configuração de diretórios
        ensure_directory_exists(self.dirs.pdfs)  # Cria diretórios necessários
        ensure_directory_exists(self.dirs.csv)  # Cria diretórios necessários
        ensure_directory_exists(self.dirs.logs)
        self.logging = LoggingConfig.create(self.dirs.logs)  # Configuração de logs
        self.scraper = ScraperConfig.create()  # Configuração do scraper
        self.data = DataConfig.create()  # Configuração do data
        # Caminho completo para o arquivo ZIP dos PDFs e CSVs
        self.pdf_zip_file = self.dirs.root / "scraper" / "pdfs" / "pdfs_compactados.zip"
        self.csv_zip_file = self.dirs.root / "data" / "csv" / "csv_compactados.zip"


config = AppConfig()
