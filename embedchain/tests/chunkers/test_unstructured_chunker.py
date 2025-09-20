
import pytest
from unittest.mock import MagicMock, patch

from embedchain.config import ChunkerConfig
from embedchain.chunkers.unstructured_chunker import UnstructuredChunker
from embedchain.loaders.pdf_file import PdfFileLoader


@pytest.fixture
def loader():
    return PdfFileLoader()


def test_unstructured_chunker(mocker):
    mocker.patch(
        "embedchain.chunkers.unstructured_chunker.UnstructuredChunker.set_data_type",
    )
    chunker = UnstructuredChunker(config=ChunkerConfig())

    # Mock the loader
    loader = MagicMock()
    loader.load_data.return_value = {
        "doc_id": "123",
        "data": [
            {"content": "This is a test table", "meta_data": {"type": "table"}},
            {"content": "This is a test image", "meta_data": {"type": "image"}},
            {"content": "This is a test text", "meta_data": {"type": "text"}},
        ],
    }

    # Test the chunker
    result = chunker.chunks(loader, ChunkerConfig())
    assert len(result) == 3
    assert result[0]["content"] == "This is a test table"
    assert result[0]["meta_data"]["type"] == "table"
    assert result[1]["content"] == "This is a test image"
    assert result[1]["meta_data"]["type"] == "image"
    assert result[2]["content"] == "This is a test text"
    assert result[2]["meta_data"]["type"] == "text"
