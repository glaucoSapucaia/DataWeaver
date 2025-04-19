import pytest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from dataweaver.settings import logger
from dataweaver.scraper.modules import (
    RequestsPDFScraper,
    AnchorPDFExtractionStrategy,
    ParagraphPDFExtractionStrategy,
    PDFLinkExtractor,
    RequestsHttpClient,
)


@pytest.fixture
def mock_html():
    return """
    <html>
        <body>
            <a href="doc1.pdf">PDF 1</a>
            <a href="http://example.com/doc2.pdf">PDF 2</a>
            <a href="other.doc">Not PDF</a>
            <p>
                <a href="doc3.pdf">PDF in paragraph</a>
            </p>
            <p>
                Text with href="doc4.pdf" embedded
            </p>
        </body>
    </html>
    """


@pytest.fixture
def mock_soup(mock_html):
    return BeautifulSoup(mock_html, "html.parser")


@pytest.fixture
def base_url():
    return "http://example.com"


class TestRequestsHttpClient:
    @patch("requests.get")
    def test_fetch_html_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html>content</html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = RequestsHttpClient()
        result = client.fetch_html("http://example.com")

        assert result == "<html>content</html>"
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("requests.get")
    @patch.object(logger, "error")
    def test_fetch_html_failure(self, mock_error, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        client = RequestsHttpClient()

        with pytest.raises(requests.exceptions.RequestException):
            client.fetch_html("http://example.com")

        mock_error.assert_called_once()


class TestAnchorPDFExtractionStrategy:
    def test_extract_with_keyword(self, mock_soup, base_url):
        strategy = AnchorPDFExtractionStrategy(keyword="doc")
        result = strategy.extract(mock_soup, base_url)

        expected = {
            urljoin(base_url, "doc1.pdf"),  # Link relativo será unido com base_url
            "http://example.com/doc2.pdf",  # Link absoluto permanece como está
            urljoin(
                base_url, "doc3.pdf"
            ),  # Link dentro de parágrafo mas ainda em tag <a>
        }
        assert result == expected

    def test_extract_with_specific_keyword(self, mock_soup, base_url):
        """Testa filtro por número específico no nome do arquivo"""
        strategy = AnchorPDFExtractionStrategy(keyword="doc2")
        result = strategy.extract(mock_soup, base_url)

        assert result == {"http://example.com/doc2.pdf"}

    def test_extract_without_keyword(self, mock_soup, base_url):
        """Testa comportamento quando keyword não é encontrada"""
        strategy = AnchorPDFExtractionStrategy(keyword="nonexistent")
        result = strategy.extract(mock_soup, base_url)
        assert result == set()


class TestParagraphPDFExtractionStrategy:
    def test_extract_with_keyword(self, mock_soup, base_url):
        strategy = ParagraphPDFExtractionStrategy(keyword="doc")
        result = strategy.extract(mock_soup, base_url)

        expected = {urljoin(base_url, "doc3.pdf"), urljoin(base_url, "doc4.pdf")}
        assert result == expected

    def test_extract_without_keyword(self, mock_soup, base_url):
        strategy = ParagraphPDFExtractionStrategy(keyword="nonexistent")
        result = strategy.extract(mock_soup, base_url)
        assert result == set()


class TestPDFLinkExtractor:
    def test_extract_combines_strategies(self, mock_soup, base_url):
        strategies = [
            AnchorPDFExtractionStrategy(keyword="doc"),
            ParagraphPDFExtractionStrategy(keyword="doc"),
        ]
        extractor = PDFLinkExtractor(strategies)
        result = extractor.extract(mock_soup, base_url)

        expected = [
            urljoin(base_url, "doc1.pdf"),
            urljoin(base_url, "http://example.com/doc2.pdf"),
            urljoin(base_url, "doc3.pdf"),
            urljoin(base_url, "doc4.pdf"),
        ]
        assert sorted(result) == sorted(expected)


class TestRequestsPDFScraper:
    @patch.object(logger, "error")
    def test_get_pdf_links_success(self, mock_error, mock_soup, base_url):
        mock_http = MagicMock()
        mock_http.fetch_html.return_value = str(mock_soup)

        mock_extractor = MagicMock()
        mock_extractor.extract.return_value = ["pdf1.pdf", "pdf2.pdf"]

        scraper = RequestsPDFScraper(mock_http, mock_extractor)
        result = scraper.get_pdf_links(base_url)

        assert result == ["pdf1.pdf", "pdf2.pdf"]
        mock_error.assert_not_called()

    @patch.object(logger, "error")
    def test_get_pdf_links_http_error(self, mock_error):
        mock_http = MagicMock()
        mock_http.fetch_html.side_effect = requests.exceptions.RequestException("Error")

        mock_extractor = MagicMock()

        scraper = RequestsPDFScraper(mock_http, mock_extractor)
        result = scraper.get_pdf_links("http://example.com")

        assert result == []
        mock_error.assert_called_once()

    @patch.object(logger, "error")
    def test_get_pdf_links_extraction_error(self, mock_error, base_url):
        mock_http = MagicMock()
        mock_http.fetch_html.return_value = "<html></html>"

        mock_extractor = MagicMock()
        mock_extractor.extract.side_effect = Exception("Extraction error")

        scraper = RequestsPDFScraper(mock_http, mock_extractor)
        result = scraper.get_pdf_links(base_url)

        assert result == []
        mock_error.assert_called_once()
