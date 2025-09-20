
import pytest
from unittest.mock import MagicMock, patch

from embedchain.loaders.pdf_file import PdfFileLoader


@pytest.fixture
def loader():
    return PdfFileLoader()


def test_load_data(loader, mocker):
    # Mock the partition_pdf function
    mock_partition_pdf = mocker.patch("embedchain.loaders.pdf_file.partition_pdf")

    # Mock the return value of partition_pdf
                        mock_partition_pdf.return_value = [
        MagicMock(
            __str__=lambda x: "unstructured.documents.elements.Table",
            metadata=MagicMock(text_as_html="<table><tr><td>This is a test table</td></tr></table>"),
            text="This is a test table",
        ),
        MagicMock(
            __str__=lambda x: "unstructured.documents.elements.Image",
            metadata=MagicMock(text_as_html=None),
            text="This is a test image",
        ),
        MagicMock(
            __str__=lambda x: "unstructured.documents.elements.Text",
            metadata=MagicMock(text_as_html=None),
            text="This is a test text",
        ),
    ]

    # Test the load_data method
    result = loader.load_data("dummy_url")

    # Assert the result
    assert len(result["data"]) == 3
    assert result["data"][0]["content"] == "<table><tr><td>This is a test table</td></tr></table>"
    assert result["data"][0]["meta_data"]["data_type"] == "table"
    assert result["data"][1]["content"] == "This is a test image"
    assert result["data"][1]["meta_data"]["data_type"] == "image"
    assert result["data"][2]["content"] == "This is a test text"
    assert result["data"][2]["meta_data"]["data_type"] == "text"
