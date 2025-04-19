from dataweaver.settings import logger
from dataweaver.scraper.modules import (
    RequestsPDFScraper,
    AnchorPDFExtractionStrategy,
    ParagraphPDFExtractionStrategy,
    PDFLinkExtractor,
    RequestsHttpClient,
)

import pytest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


@pytest.fixture
def mock_html():
    """Retorna HTML de exemplo contendo vários tipos de links para testes."""
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
    """Retorna um objeto BeautifulSoup parseado a partir do HTML mockado."""
    return BeautifulSoup(mock_html, "html.parser")


@pytest.fixture
def base_url():
    """URL base para testes de resolução de links relativos."""
    return "http://example.com"


class TestRequestsHttpClient:
    """Testes para a classe RequestsHttpClient."""

    @patch("requests.get")
    def test_fetch_html_success(self, mock_get):
        """Testa requisição HTTP bem-sucedida.

        Verifica:
            - Retorna o conteúdo HTML correto
            - Faz a requisição com timeout de 10s
            - Verifica status da resposta
        """
        mock_response = MagicMock()
        mock_response.text = "<html>content</html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = RequestsHttpClient()
        result = client.fetch_html("http://example.com")

        assert result == "<html>content</html>"
        mock_get.assert_called_once_with("http://example.com", timeout=10)
        mock_response.raise_for_status.assert_called_once()

    @patch("requests.get")
    @patch.object(logger, "error")
    def test_fetch_html_failure(self, mock_error, mock_get):
        """Testa falha na requisição HTTP.

        Verifica:
            - Propaga a exceção corretamente
            - Loga o erro apropriadamente
        """
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        client = RequestsHttpClient()

        with pytest.raises(requests.exceptions.RequestException):
            client.fetch_html("http://example.com")

        mock_error.assert_called_once_with(
            "Falha na requisição para http://example.com: Error"
        )


class TestAnchorPDFExtractionStrategy:
    """Testes para a estratégia de extração de links em tags <a>."""

    def test_extract_with_keyword(self, mock_soup, base_url):
        """Testa extração com palavra-chave genérica.

        Verifica:
            - Encontra links PDF em tags <a>
            - Resolve links relativos corretamente
            - Mantém links absolutos
            - Filtra por palavra-chave
            - Ignora arquivos não-PDF
        """
        strategy = AnchorPDFExtractionStrategy(keyword="doc")
        result = strategy.extract(mock_soup, base_url)

        expected = {
            urljoin(base_url, "doc1.pdf"),
            "http://example.com/doc2.pdf",
            urljoin(base_url, "doc3.pdf"),
        }
        assert result == expected

    def test_extract_with_specific_keyword(self, mock_soup, base_url):
        """Testa filtro por palavra-chave específica.

        Verifica:
            - Filtra corretamente por termo específico
            - Retorna apenas links que contêm a palavra-chave
        """
        strategy = AnchorPDFExtractionStrategy(keyword="doc2")
        result = strategy.extract(mock_soup, base_url)

        assert result == {"http://example.com/doc2.pdf"}

    def test_extract_without_keyword(self, mock_soup, base_url):
        """Testa comportamento quando palavra-chave não é encontrada.

        Verifica:
            - Retorna conjunto vazio quando nenhum link corresponde
        """
        strategy = AnchorPDFExtractionStrategy(keyword="nonexistent")
        result = strategy.extract(mock_soup, base_url)
        assert result == set()


class TestParagraphPDFExtractionStrategy:
    """Testes para a estratégia de extração de links em parágrafos."""

    def test_extract_with_keyword(self, mock_soup, base_url):
        """Testa extração de links embutidos em texto.

        Verifica:
            - Encontra links PDF em texto usando regex
            - Resolve links relativos corretamente
            - Filtra por palavra-chave
        """
        strategy = ParagraphPDFExtractionStrategy(keyword="doc")
        result = strategy.extract(mock_soup, base_url)

        expected = {urljoin(base_url, "doc3.pdf"), urljoin(base_url, "doc4.pdf")}
        assert result == expected

    def test_extract_without_keyword(self, mock_soup, base_url):
        """Testa comportamento quando palavra-chave não é encontrada.

        Verifica:
            - Retorna conjunto vazio quando nenhum link corresponde
        """
        strategy = ParagraphPDFExtractionStrategy(keyword="nonexistent")
        result = strategy.extract(mock_soup, base_url)
        assert result == set()


class TestPDFLinkExtractor:
    """Testes para o combinador de estratégias de extração."""

    def test_extract_combines_strategies(self, mock_soup, base_url):
        """Testa combinação de múltiplas estratégias.

        Verifica:
            - Combina resultados de todas as estratégias
            - Remove duplicatas
            - Mantém todos os links encontrados
        """
        strategies = [
            AnchorPDFExtractionStrategy(keyword="doc"),
            ParagraphPDFExtractionStrategy(keyword="doc"),
        ]
        extractor = PDFLinkExtractor(strategies)
        result = extractor.extract(mock_soup, base_url)

        expected = [
            urljoin(base_url, "doc1.pdf"),
            "http://example.com/doc2.pdf",
            urljoin(base_url, "doc3.pdf"),
            urljoin(base_url, "doc4.pdf"),
        ]
        assert sorted(result) == sorted(expected)


class TestRequestsPDFScraper:
    """Testes para a classe principal de scraping de PDFs."""

    @patch.object(logger, "error")
    def test_get_pdf_links_success(self, mock_error, mock_soup, base_url):
        """Testa fluxo completo bem-sucedido.

        Verifica:
            - Obtém HTML via HTTP
            - Extrai links usando o extrator
            - Retorna lista de links
            - Não loga erros
        """
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
        """Testa falha na requisição HTTP.

        Verifica:
            - Retorna lista vazia em caso de erro
            - Loga o erro apropriadamente
        """
        mock_http = MagicMock()
        mock_http.fetch_html.side_effect = requests.exceptions.RequestException("Error")

        mock_extractor = MagicMock()

        scraper = RequestsPDFScraper(mock_http, mock_extractor)
        result = scraper.get_pdf_links("http://example.com")

        assert result == []
        mock_error.assert_called_once_with(
            "Erro ao obter links PDF de 'http://example.com': Error"
        )

    @patch.object(logger, "error")
    def test_get_pdf_links_extraction_error(self, mock_error, base_url):
        """Testa falha na extração de links.

        Verifica:
            - Retorna lista vazia em caso de erro
            - Loga o erro apropriadamente
        """
        mock_http = MagicMock()
        mock_http.fetch_html.return_value = "<html></html>"

        mock_extractor = MagicMock()
        mock_extractor.extract.side_effect = Exception("Extraction error")

        scraper = RequestsPDFScraper(mock_http, mock_extractor)
        result = scraper.get_pdf_links(base_url)

        assert result == []
        mock_error.assert_called_once_with(
            "Erro ao obter links PDF de 'http://example.com': Extraction error"
        )
