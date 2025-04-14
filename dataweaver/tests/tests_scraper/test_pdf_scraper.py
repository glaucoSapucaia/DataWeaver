"""
Módulo de testes para classes de scraping de PDFs no sistema.

Testa o funcionamento da extração de links de PDF em páginas HTML usando a classe `PDFLinkExtractor`,
o comportamento do `RequestsPDFScraper` em diferentes situações e o funcionamento do cliente HTTP `RequestsHttpClient`.

O módulo cobre:
- Casos funcionais
- Tratamento de exceções
- Requisições HTTP simuladas
"""

import pytest                  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import requests                # type: ignore

from dataweaver.scraper.modules.pdf_scraper import RequestsPDFScraper, PDFLinkExtractor, RequestsHttpClient
from unittest.mock import Mock, patch


# =========================
# FIXTURES
# =========================

@pytest.fixture
def html_with_links():
    """Retorna um HTML de exemplo contendo dois links para arquivos PDF."""

    return '''
        <html>
            <body>
                <a href="relatorio_2024.pdf">Relatório</a>
                <p>Veja o <a href='dados_internos_2024.pdf'>PDF</a></p>
                <p>href="boletim_extra.pdf"</p>
            </body>
        </html>
    '''

@pytest.fixture
def html_without_links():
    """Retorna um HTML de exemplo que não contém links para PDFs."""

    return "<html><body><p>Sem PDFs aqui</p></body></html>"


# =========================
# TESTES FUNCIONAIS
# =========================

def test_extractor_finds_pdfs_from_anchors_and_paragraphs(html_with_links):
    """Verifica se o extrator retorna os links esperados a partir de âncoras e parágrafos."""

    soup = BeautifulSoup(html_with_links, "html.parser")
    extractor = PDFLinkExtractor(keyword="2024")
    links = extractor.extract(soup, "https://exemplo.com")

    assert isinstance(links, list)
    assert len(links) == 2
    assert "relatorio_2024.pdf" in links[0] or links[1]
    assert all(link.endswith(".pdf") for link in links)

def test_scraper_returns_links(html_with_links):
    """Verifica se o scraper retorna os links de PDF extraídos corretamente."""

    mock_http = Mock()
    mock_http.fetch_html.return_value = html_with_links
    extractor = PDFLinkExtractor(keyword="2024")
    scraper = RequestsPDFScraper(http_client=mock_http, extractor=extractor)

    links = scraper.get_pdf_links("https://teste.com")

    assert isinstance(links, list)
    assert len(links) == 2

def test_scraper_returns_empty_on_extraction_failure():
    """Garante que o scraper retorna lista vazia e registra log em caso de falha de extração."""

    mock_http = Mock()
    mock_http.fetch_html.return_value = "<html></html>"
    broken_extractor = Mock()
    broken_extractor.extract.side_effect = Exception("Erro ao extrair")
    
    scraper = RequestsPDFScraper(http_client=mock_http, extractor=broken_extractor)

    with patch("dataweaver.scraper.modules.pdf_scraper.logger.error") as mock_log:
        links = scraper.get_pdf_links("https://exemplo.com")
        assert links == []
        mock_log.assert_called()


# =========================
# TESTES DE EXCEÇÕES INTERNAS
# =========================

def test_anchor_extraction_exception_logged(html_with_links):
    """Testa se exceções em _extract_from_anchors são registradas e não interrompem a execução."""

    extractor = PDFLinkExtractor(keyword="2024")
    soup = BeautifulSoup(html_with_links, "html.parser")

    with patch("bs4.BeautifulSoup.find_all", side_effect=Exception("Erro")):
        with patch("dataweaver.scraper.modules.pdf_scraper.logger.warning") as mock_warning:
            links = extractor._extract_from_anchors(soup, "https://base.url")
            assert links == set()
            mock_warning.assert_called()

def test_paragraph_extraction_exception_logged(html_with_links):
    """Testa se exceções em _extract_from_paragraphs são registradas corretamente."""

    extractor = PDFLinkExtractor(keyword="2024")
    soup = BeautifulSoup(html_with_links, "html.parser")

    with patch("bs4.BeautifulSoup.find_all", side_effect=Exception("Erro")):
        with patch("dataweaver.scraper.modules.pdf_scraper.logger.warning") as mock_warning:
            links = extractor._extract_from_paragraphs(soup, "https://base.url")
            assert links == set()
            mock_warning.assert_called()

def test_extract_handles_exception_from_anchors():
    """Verifica se erros em _extract_from_anchors são tratados no método extract."""

    extractor = PDFLinkExtractor("relatorio")
    soup = BeautifulSoup("<html></html>", "html.parser")
    
    with patch.object(PDFLinkExtractor, '_extract_from_anchors', side_effect=Exception("Erro em anchors")), \
        patch("dataweaver.scraper.modules.pdf_scraper.logger.error") as mock_logger:
        
        result = extractor.extract(soup, "http://exemplo.com")
        assert result == []
        assert mock_logger.called
        assert "Erro ao extrair links PDF" in mock_logger.call_args[0][0]

def test_extract_handles_exception_from_paragraphs():
    """Verifica se erros em _extract_from_paragraphs são tratados no método extract."""

    extractor = PDFLinkExtractor("relatorio")
    soup = BeautifulSoup("<html><a href='relatorio.pdf'></a></html>", "html.parser")

    with patch.object(PDFLinkExtractor, '_extract_from_paragraphs', side_effect=Exception("Erro em paragrafos")), \
        patch("dataweaver.scraper.modules.pdf_scraper.logger.error") as mock_logger:
        
        result = extractor.extract(soup, "http://exemplo.com")
        assert result == []
        assert mock_logger.called
        assert "Erro ao extrair links PDF" in mock_logger.call_args[0][0]

def test_extract_handles_generic_exception():
    """Garante que exceções genéricas durante a extração também são tratadas."""

    extractor = PDFLinkExtractor("relatorio")
    soup = BeautifulSoup("<html></html>", "html.parser")

    with patch.object(PDFLinkExtractor, '_extract_from_anchors', side_effect=Exception("Erro artificial")), \
        patch("dataweaver.scraper.modules.pdf_scraper.logger.error") as mock_logger:

        result = extractor.extract(soup, "http://exemplo.com")
        assert result == []
        assert mock_logger.called
        assert "Erro ao extrair links PDF" in mock_logger.call_args[0][0]


# =========================
# TESTES DE CLIENTE HTTP
# =========================

def test_http_client_fetches_html_success():
    """Testa se o cliente HTTP retorna o HTML corretamente em caso de sucesso."""

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = RequestsHttpClient()
        html = client.fetch_html("https://site.com")

        assert isinstance(html, str)
        assert html.startswith("<html>")

def test_http_client_raises_on_failure():
    """Garante que o cliente HTTP levanta exceção e registra erro em falhas de requisição."""
    
    with patch("requests.get", side_effect=requests.exceptions.RequestException("Erro")):
        client = RequestsHttpClient()
        with patch("dataweaver.scraper.modules.pdf_scraper.logger.error") as mock_logger:
            with pytest.raises(Exception):
                client.fetch_html("https://erro.com")
            assert mock_logger.called
