from dataweaver.settings import logger
from dataweaver.errors import LinkPDFExtractionError
from .interfaces import PDFScraperInterface, HttpClientInterface, PDFExtractionStrategy

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re


class RequestsPDFScraper(PDFScraperInterface):
    """Implementação concreta de PDFScraper usando requests e estratégia de extração.

    Padrão de Projeto:
        Strategy - delega a extração de links para PDFExtractionStrategy
        Composition - combina HttpClientInterface e PDFExtractionStrategy
    """

    def __init__(
        self, http_client: HttpClientInterface, extractor: "PDFExtractionStrategy"
    ) -> None:
        self.http_client = http_client
        self.extractor = extractor

    def get_pdf_links(self, url: str) -> list[str]:
        """Obtém links de PDFs de uma página web."""
        try:
            html = self.http_client.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            return self.extractor.extract(soup, url)
        except Exception as e:
            logger.error("Erro ao extrair PDFs")
            raise LinkPDFExtractionError(f"Erro ao processar a URL: {url}")


class AnchorPDFExtractionStrategy(PDFExtractionStrategy):
    """Estratégia para extrair links PDF de tags <a>.

    Padrão de Projeto:
        Strategy - implementa algoritmo específico de extração
    """

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Extrai links PDF de elementos <a href>.

        Args:
            soup: Objeto BeautifulSoup com o HTML parseado
            base_url: URL base para resolver links relativos

        Returns:
            Conjunto de URLs absolutos para PDFs encontrados
        """
        links = set()
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if ".pdf" in href.lower() and self.keyword in href.lower():
                links.add(urljoin(base_url, href))
        return links


class ParagraphPDFExtractionStrategy(PDFExtractionStrategy):
    """Estratégia para extrair links PDF embutidos em parágrafos."""

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Busca links PDF em textos de parágrafos usando regex.

        Args:
            soup: Objeto BeautifulSoup com o HTML
            base_url: URL base para links relativos

        Returns:
            Conjunto de URLs absolutos para PDFs encontrados
        """
        links = set()
        for paragraph in soup.find_all("p"):
            matches = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', str(paragraph))
            for match in matches:
                if self.keyword in match.lower():
                    links.add(urljoin(base_url, match))
        return links


class PDFLinkExtractor(PDFExtractionStrategy):
    """Agrega múltiplas estratégias de extração de links PDF.

    Padrão de Projeto:
        Composite - combina resultados de várias estratégias
    """

    def __init__(self, strategies: list["PDFExtractionStrategy"]) -> None:
        self.strategies = strategies

    def extract(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Executa todas as estratégias e consolida os resultados.

        Args:
            soup: HTML parseado
            base_url: URL base para normalização

        Returns:
            Lista única com todos os links encontrados (sem duplicatas)
        """
        pdf_links = set()
        for strategy in self.strategies:
            pdf_links.update(strategy.extract(soup, base_url))
        return list(pdf_links)


class RequestsHttpClient(HttpClientInterface):
    """Implementação de cliente HTTP usando a biblioteca requests.

    Padrão de Projeto:
        Adapter - adapta a interface do requests para HttpClientInterface
    """

    def fetch_html(self, url: str) -> str:
        """Obtém o conteúdo HTML de uma URL.

        Args:
            url: Endereço para requisição GET

        Returns:
            String com o conteúdo HTML

        Raises:
            requests.exceptions.RequestException: Em falhas de rede/timeout
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Falha na requisição para {url[:50]}...: {e}")
            raise
