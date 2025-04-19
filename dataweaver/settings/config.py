from dataweaver.utils import *

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DirectoryConfig:
    """Configuração de diretórios da aplicação (Princípio da Responsabilidade Única)"""

    root: Path  # Diretório raiz do projeto
    pdfs: Path  # Pasta para armazenar PDFs
    modules: Path  # Pasta dos módulos do scraper
    tests: Path  # Pasta de testes
    data: Path  # Pasta de dados processados
    logs: Path  # Pasta de arquivos de log

    @classmethod
    def create(cls) -> "DirectoryConfig":
        """Método factory para criação da configuração de diretórios"""
        root = Path(__file__).resolve().parent.parent.parent
        return cls(
            root=root,
            pdfs=root / "dataweaver" / "scraper" / "pdfs",
            modules=root / "dataweaver" / "scraper" / "modules",
            tests=root / "dataweaver" / "scraper" / "tests",
            data=root / "data" / "files",
            logs=root / "dataweaver" / "logs",
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
            zip_name=get_env_variable("ZIP_NAME", "pdfs_compactados.zip"),
            filter=get_env_variable("FILTER", "ANEXO"),
            url=get_env_variable(
                "URL",
                "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
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
        self.logging = LoggingConfig.create(self.dirs.logs)  # Configuração de logs
        self.scraper = ScraperConfig.create()  # Configuração do scraper
        # Caminho completo para o arquivo ZIP dos PDFs
        self.pdf_zip_file = self.dirs.root / "scraper" / "pdfs" / "pdfs_compactados.zip"


config = AppConfig()
