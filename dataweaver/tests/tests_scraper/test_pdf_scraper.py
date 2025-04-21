from dataweaver.scraper.modules import (
    RequestsHttpClient,
    AnchorPDFExtractionStrategy,
    ParagraphPDFExtractionStrategy,
    PDFLinkExtractor,
    RequestsPDFScraper,
)

from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Testes para RequestsHttpClient
def test_http_client_success():
    """Testa requisição bem-sucedida"""
    mock_response = MagicMock()
    mock_response.text = "<html>content</html>"
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        client = RequestsHttpClient()
        result = client.fetch_html("http://example.com")

        assert result == "<html>content</html>"
        mock_get.assert_called_once_with("http://example.com", timeout=10)


# Testes para AnchorPDFExtractionStrategy
def test_anchor_strategy_finds_pdf_links():
    """Testa extração de links PDF em tags <a>"""
    html = """
    <html>
        <a href="doc1.pdf">PDF 1</a>
        <a href="http://other.com/doc2.pdf">PDF 2</a>
        <a href="invalid.doc">Not PDF</a>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    strategy = AnchorPDFExtractionStrategy(keyword="doc")

    links = strategy.extract(soup, "http://example.com/")

    assert urljoin("http://example.com/", "doc1.pdf") in links
    assert "http://other.com/doc2.pdf" in links
    assert len(links) == 2


def test_anchor_strategy_filters_by_keyword():
    """Testa filtro por palavra-chave"""
    html = """
    <html>
        <a href="important.pdf">Important</a>
        <a href="other.pdf">Other</a>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    strategy = AnchorPDFExtractionStrategy(keyword="important")

    links = strategy.extract(soup, "http://example.com/")

    assert urljoin("http://example.com/", "important.pdf") in links
    assert len(links) == 1


# Testes para ParagraphPDFExtractionStrategy
def test_paragraph_strategy_finds_embedded_links():
    """Testa extração de links em parágrafos"""
    html = """
    <html>
        <p>Download <a href="doc1.pdf">here</a></p>
        <p>Or visit <a href="http://site.com/doc2.pdf">this</a> page</p>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    strategy = ParagraphPDFExtractionStrategy(keyword="doc")

    links = strategy.extract(soup, "http://example.com/")

    assert urljoin("http://example.com/", "doc1.pdf") in links
    assert "http://site.com/doc2.pdf" in links
    assert len(links) == 2


def test_paragraph_strategy_uses_regex():
    """Testa regex para encontrar links PDF"""
    html = '<p>Download <a href="special.pdf">special file</a></p>'
    soup = BeautifulSoup(html, "html.parser")
    strategy = ParagraphPDFExtractionStrategy(keyword="special")

    links = strategy.extract(soup, "http://example.com/")

    assert urljoin("http://example.com/", "special.pdf") in links


# Testes para PDFLinkExtractor
def test_link_extractor_combines_strategies():
    """Testa combinação de múltiplas estratégias"""
    mock_strategy1 = Mock()
    mock_strategy1.extract.return_value = {"link1.pdf", "link2.pdf"}

    mock_strategy2 = Mock()
    mock_strategy2.extract.return_value = {"link2.pdf", "link3.pdf"}

    extractor = PDFLinkExtractor([mock_strategy1, mock_strategy2])
    soup = BeautifulSoup("<html></html>", "html.parser")

    links = extractor.extract(soup, "http://example.com")

    assert len(links) == 3  # União sem duplicatas
    mock_strategy1.extract.assert_called_once()
    mock_strategy2.extract.assert_called_once()


# Testes para RequestsPDFScraper
def test_pdf_scraper_success_flow():
    """Testa fluxo completo do scraper"""
    mock_client = Mock()
    mock_client.fetch_html.return_value = "<html></html>"

    mock_extractor = Mock()
    mock_extractor.extract.return_value = ["link1.pdf", "link2.pdf"]

    scraper = RequestsPDFScraper(mock_client, mock_extractor)
    links = scraper.get_pdf_links("http://example.com")

    assert links == ["link1.pdf", "link2.pdf"]
    mock_client.fetch_html.assert_called_once_with("http://example.com")
    mock_extractor.extract.assert_called_once()


def test_pdf_scraper_uses_strategy_correctly():
    """Testa integração entre scraper e estratégia"""
    test_html = """
    <html>
        <a href="test.pdf">Test</a>
    </html>
    """
    mock_client = Mock()
    mock_client.fetch_html.return_value = test_html

    # Usando estratégia real para teste de integração
    strategy = AnchorPDFExtractionStrategy(keyword="test")
    scraper = RequestsPDFScraper(mock_client, strategy)

    links = scraper.get_pdf_links("http://example.com")

    assert len(links) == 1
    assert urljoin("http://example.com/", "test.pdf") in links
