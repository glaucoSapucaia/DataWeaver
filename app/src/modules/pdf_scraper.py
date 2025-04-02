from .interfaces import PDFScraperInterface
from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin
import requests
import re

class RequestsPDFScraper(PDFScraperInterface):
    """Implementação do PDFScraper usando a biblioteca requests."""
    
    def get_pdf_links(self, url: str, _filter: str) -> list:
        """
        Obtém os links dos arquivos PDF na página, verificando o nome do arquivo.
        
        Parâmetros:
            url (str): URL da página para extração.
            _filter (str): Palavra-chave para filtrar os PDFs.
        
        Retorna:
            list: Lista de URLs dos arquivos PDF encontrados.
        """
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        pdf_links = set()  # Usar um conjunto para evitar duplicatas

        # Captura links diretos em <a href="...">
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Verifica se o nome do arquivo .pdf contém o _filter
            if ".pdf" in href.lower() and _filter.lower() in href.lower():
                full_url = urljoin(url, href)
                pdf_links.add(full_url)

        # Captura PDFs mencionados em parágrafos <p> (usando regex)
        for paragraph in soup.find_all('p'):
            # Procura por links de PDFs no texto do parágrafo
            matches = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', str(paragraph))
            for match in matches:
                # Verifica se o nome do arquivo contém o _filter
                if _filter.lower() in match.lower():
                    full_url = urljoin(url, match)
                    pdf_links.add(full_url)

        return list(pdf_links)
