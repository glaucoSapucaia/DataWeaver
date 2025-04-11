"""
Módulo responsável por realizar scraping de arquivos PDF a partir de uma página HTML.

Contém as classes:
- RequestsPDFScraper: usa um cliente HTTP para buscar o HTML e extrair links de PDF.
- PDFLinkExtractor: estratégia para extrair links de PDF com base em palavras-chave.
- RequestsHttpClient: implementação do cliente HTTP usando a biblioteca `requests`.
"""

from .interfaces import PDFScraperInterface, HttpClientInterface, PDFExtractorStrategyInterface
from urllib.parse import urljoin
from dataweaver.logger import logger
from bs4 import BeautifulSoup  # type: ignore
import requests                # type: ignore
import re

class RequestsPDFScraper(PDFScraperInterface):
    """
    Implementação do PDFScraper que utiliza um cliente HTTP e uma estratégia de extração.
    """

    def __init__(self, http_client: HttpClientInterface, extractor: PDFExtractorStrategyInterface) -> None:
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
            soup = BeautifulSoup(html, 'html.parser')
            return self.extractor.extract(soup, url)
        except Exception as e:
            logger.error(f"Erro ao obter links PDF de '{url}': {e}")
            return []

class PDFLinkExtractor(PDFExtractorStrategyInterface):
    """
    Estratégia para extrair links de arquivos PDF com base em uma palavra-chave.
    """

    def __init__(self, keyword: str):
        """
        Inicializa o extrator com a palavra-chave que será usada como filtro.

        Parâmetros:
            keyword (str): Palavra-chave que deve estar presente no nome do arquivo.
        """
        self.keyword = keyword.lower()

    def extract(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """
        Extrai todos os links de PDF de uma estrutura HTML.

        Parâmetros:
            soup (BeautifulSoup): Estrutura HTML da página.
            base_url (str): URL base para composição de links relativos.

        Retorno:
            list[str]: Lista de URLs para arquivos PDF encontrados.
        """
        try:
            pdf_links = set()
            pdf_links.update(self._extract_from_anchors(soup, base_url))
            pdf_links.update(self._extract_from_paragraphs(soup, base_url))
            return list(pdf_links)
        except Exception as e:
            logger.error(f"Erro ao extrair links PDF: {e}")
            return []

    def _extract_from_anchors(self, soup: BeautifulSoup, base_url: str) -> set[str]:
        """
        Extrai links de arquivos PDF presentes em elementos <a>.

        Parâmetros:
            soup (BeautifulSoup): Estrutura HTML.
            base_url (str): URL base para links relativos.

        Retorno:
            set[str]: Conjunto de links de arquivos PDF.
        """
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
        """
        Extrai links de arquivos PDF mencionados em parágrafos usando regex.

        Parâmetros:
            soup (BeautifulSoup): Estrutura HTML.
            base_url (str): URL base para links relativos.

        Retorno:
            set[str]: Conjunto de links de arquivos PDF encontrados em <p>.
        """
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
