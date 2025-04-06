from .interfaces import PDFScraperInterface, HttpClientInterface, PDFExtractorStrategy
from logger import logger
from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin
import requests
import re

class RequestsPDFScraper(PDFScraperInterface):
    """Implementação do PDFScraper usando um cliente HTTP injetável."""

    def __init__(self, http_client: HttpClientInterface, extractor: PDFExtractorStrategy) -> None:
        """
        Inicializa o scraper com um cliente HTTP.

        Parâmetros:
            http_client (HttpClientInterface): Cliente HTTP injetável.
        """
        self.http_client = http_client
        self.extractor = extractor

    def get_pdf_links(self, url: str) -> list[str]:
        """Obtém links de arquivos PDF na página, filtrando por palavra-chave."""
        try:
            html = self.http_client.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self.extractor.extract(soup, url)
        except Exception as e:
            logger.error(f"Erro ao obter links PDF de '{url}': {e}")
            return []

class PDFLinkExtractor(PDFExtractorStrategy):
    """Classe responsável por extrair links de PDFs da página."""
    
    def __init__(self, keyword: str):
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Extrai todos os links de PDFs de uma página HTML."""
        try:
            pdf_links = set()
            pdf_links.update(self._extract_from_anchors(soup, base_url))
            pdf_links.update(self._extract_from_paragraphs(soup, base_url))
            return list(pdf_links)
        except Exception as e:
            logger.error(f"Erro ao extrair links PDF: {e}")
            return []

    def _extract_from_anchors(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Extrai PDFs de links <a>."""
        links = set()
        try:
            for link in soup.find_all('a', href=True):
                href = link['href']
                if ".pdf" in href.lower() and self.keyword in href.lower():
                    links.add(urljoin(base_url, href))
        except Exception as e:
            logger.warning(f"Erro ao extrair de <a>: {e}")
        return links

    def _extract_from_paragraphs(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Extrai PDFs mencionados dentro de tags <p> usando regex."""
        links = set()
        try:
            for paragraph in soup.find_all('p'):
                matches = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', str(paragraph))
                for match in matches:
                    if self.keyword in match.lower():
                        links.add(urljoin(base_url, match))
        except Exception as e:
            logger.warning(f"Erro ao extrair de <p>: {e}")
        return links

class RequestsHttpClient(HttpClientInterface):
    """Implementação de HttpClientInterface usando requests."""

    def fetch_html(self, url: str) -> str:
        """Faz uma requisição HTTP GET e retorna o HTML da página."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição HTTP para {url}: {e}")
            raise  # Propaga o erro para que o scraper lide com ele
