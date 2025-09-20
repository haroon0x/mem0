
from typing import Optional

from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helpers.json_serializable import register_deserializable


@register_deserializable
class UnstructuredChunker(BaseChunker):
    """Chunker for unstructured data."""

    def __init__(self, config: Optional[ChunkerConfig] = None):
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        # We don't need a text splitter for unstructured data
        super().__init__(None)

    def chunks(self, loader, config: ChunkerConfig):
        """Return chunks from a loader."""
        data_result = loader.load_data(self.config.url)
        doc_id = data_result["doc_id"]
        data = data_result["data"]

        all_chunks = []
        for data_item in data:
            content = data_item["content"]
            metadata = data_item["meta_data"]
            metadata["doc_id"] = doc_id

            if metadata.get("data_type") == "table":
                # For tables, we don't need to split the content
                all_chunks.append({
                    "content": content,
                    "meta_data": metadata,
                })
            else:
                # For other data types, we can use the default chunking
                # In the future, we can add more sophisticated chunking for images
                # For now, we just treat them as text
                all_chunks.append({
                    "content": content,
                    "meta_data": metadata,
                })

        return all_chunks
