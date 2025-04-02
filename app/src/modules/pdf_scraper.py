from .interfaces import PDFScraperInterface, HttpClientInterface, PDFExtractorStrategy
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
        html = self.http_client.fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        return self.extractor.extract(soup, url)

class PDFLinkExtractor(PDFExtractorStrategy):
    """Classe responsável por extrair links de PDFs da página."""
    
    def __init__(self, keyword: str):
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Extrai todos os links de PDFs de uma página HTML."""
        pdf_links = set()
        pdf_links.update(self._extract_from_anchors(soup, base_url))
        pdf_links.update(self._extract_from_paragraphs(soup, base_url))
        return list(pdf_links)

    def _extract_from_anchors(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Extrai PDFs de links <a>."""
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if ".pdf" in href.lower() and self.keyword in href.lower():
                links.add(urljoin(base_url, href))
        return links

    def _extract_from_paragraphs(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """Extrai PDFs mencionados dentro de tags <p> usando regex."""
        links = set()
        for paragraph in soup.find_all('p'):
            matches = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', str(paragraph))
            for match in matches:
                if self.keyword in match.lower():
                    links.add(urljoin(base_url, match))
        return links

class RequestsHttpClient(HttpClientInterface):
    """Implementação de HttpClientInterface usando requests."""

    def fetch_html(self, url: str) -> str:
        """Faz uma requisição HTTP GET e retorna o HTML da página."""
        response = requests.get(url)
        response.raise_for_status()
        return response.text
