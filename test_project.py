import pytest
from unittest.mock import MagicMock
from project import read_single_page, read_all_pages, read_custom_page

# Mock PDF reader for testing
@pytest.fixture
def mock_pdf_reader():
    pdf_reader = MagicMock()
    pdf_reader.pages = [MagicMock(), MagicMock(), MagicMock()]
    pdf_reader.pages[0].extract_text.return_value = "Page 1 text"
    pdf_reader.pages[1].extract_text.return_value = "Page 2 text"
    pdf_reader.pages[2].extract_text.return_value = "Page 3 text"
    return pdf_reader

def test_read_single_page_valid(mock_pdf_reader):
    page_number, text = read_single_page(mock_pdf_reader, 1)
    assert page_number == 1
    assert text == "Page 1 text"

def test_read_single_page_invalid(mock_pdf_reader):
    page_number, message = read_single_page(mock_pdf_reader, 4)
    assert page_number == 4
    assert message == "Page number is not in this PDF."

def test_read_all_pages(mock_pdf_reader):
    pages = read_all_pages(mock_pdf_reader)
    assert len(pages) == 3
    assert pages[0] == (1, "Page 1 text")
    assert pages[1] == (2, "Page 2 text")
    assert pages[2] == (3, "Page 3 text")

def test_read_custom_page_valid(mock_pdf_reader):
    pages = read_custom_page(mock_pdf_reader, 1, 2)
    assert len(pages) == 2
    assert pages[0] == (1, "Page 1 text")
    assert pages[1] == (2, "Page 2 text")

def test_read_custom_page_invalid_range(mock_pdf_reader):
    pages = read_custom_page(mock_pdf_reader, 2, 1)
    assert pages == [(2, "Start page cannot be greater than end page.")]

def test_read_custom_page_invalid_page(mock_pdf_reader):
    pages = read_custom_page(mock_pdf_reader, 1, 4)
    assert pages == [(1, "Start or end page is not in this PDF.")]
