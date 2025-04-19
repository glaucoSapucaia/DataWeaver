from .interfaces import (
    PDFScraperInterface,
    HttpClientInterface,
    PDFExtractionStrategy,
)
from dataweaver.settings import logger

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re


class RequestsPDFScraper(PDFScraperInterface):
    """
    Implementação do PDFScraper que utiliza um cliente HTTP e uma estratégia de extração.
    """

    def __init__(
        self, http_client: HttpClientInterface, extractor: PDFExtractionStrategy
    ) -> None:
        """
        Inicializa o scraper com um cliente HTTP e uma estratégia de extração.

        Parâmetros:
            http_client (HttpClientInterface): Cliente HTTP responsável pela requisição.
            extractor (PDFExtractorStrategy): Estratégia para extrair os links dos arquivos PDF.
        """
        self.http_client = http_client
        self.extractor = extractor

    def get_pdf_links(self, url: str) -> list[str]:
        """
        Obtém os links de arquivos PDF presentes na página indicada.

        Parâmetros:
            url (str): URL da página a ser analisada.

        Retorno:
            list[str]: Lista de URLs para arquivos PDF encontrados.
        """
        try:
            html = self.http_client.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            return self.extractor.extract(soup, url)
        except Exception as e:
            logger.error(f"Erro ao obter links PDF de '{url}': {e}")
            return []


class AnchorPDFExtractionStrategy(PDFExtractionStrategy):
    def __init__(self, keyword: str):
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        links = set()
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if ".pdf" in href.lower() and self.keyword in href.lower():
                links.add(urljoin(base_url, href))
        return links


class ParagraphPDFExtractionStrategy(PDFExtractionStrategy):
    def __init__(self, keyword: str):
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        links = set()
        for paragraph in soup.find_all("p"):
            matches = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', str(paragraph))
            for match in matches:
                if self.keyword in match.lower():
                    links.add(urljoin(base_url, match))
        return links


class PDFLinkExtractor:
    def __init__(self, strategies: list[PDFExtractionStrategy]):
        self.strategies = strategies

    def extract(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        pdf_links = set()
        for strategy in self.strategies:
            pdf_links.update(strategy.extract(soup, base_url))
        return list(pdf_links)


class RequestsHttpClient(HttpClientInterface):
    """
    Implementação do cliente HTTP utilizando a biblioteca `requests`.
    """

    def fetch_html(self, url: str) -> str:
        """
        Realiza uma requisição HTTP GET e retorna o conteúdo HTML da página.

        Parâmetros:
            url (str): URL da página a ser acessada.

        Retorno:
            str: HTML retornado pela página.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição HTTP para {url}: {e}")
            raise  # Propaga o erro para que o scraper lide com ele
