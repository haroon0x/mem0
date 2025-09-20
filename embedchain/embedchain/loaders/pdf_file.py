import hashlib
import logging
from typing import Any, Optional

from unstructured.partition.pdf import partition_pdf

from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import clean_string

logger = logging.getLogger(__name__)


@register_deserializable
class PdfFileLoader(BaseLoader):
    def __init__(self, config: Optional[dict[str, Any]] = None):
        super().__init__()
        config = config or {}
        self.mode = config.get("mode", "paged")  # Default to 'paged'

    def load_data(self, url):
        """Load data from a PDF file."""
        try:
            elements = partition_pdf(
                url,
                strategy="auto",
                infer_table_structure=True,
                extract_images_in_pdf=True,
            )
            data = []
            all_content = []

            for element in elements:
                metadata = {"url": url, "data_type": "text"}  # Default data_type
                content = ""

                if "unstructured.documents.elements.Table" in str(type(element)):
                    metadata["data_type"] = "table"
                    content = str(element.metadata.text_as_html)
                elif "unstructured.documents.elements.Image" in str(type(element)):
                    metadata["data_type"] = "image"
                    content = str(element.text)
                else:
                    content = clean_string(str(element))

                if content:
                    data.append({"content": content, "meta_data": metadata})
                    all_content.append(content)

            if not data:
                raise ValueError("No data found")

            doc_id = hashlib.sha256((url + "".join(all_content)).encode()).hexdigest()
            return {"doc_id": doc_id, "data": data}

        except Exception as e:
            logger.error(f"Error processing PDF file {url}: {e}")
            raise
