from pydantic import BaseModel
from typing import List, Optional

class DocumentMetadata(BaseModel):
    filename: str
    content_type: str
    file_size: int
    page_count: Optional[int] = 0

class DocumentChunk(BaseModel):
    text: str
    chunk_id: int
    metadata: dict

class ProcessedDocument(BaseModel):
    document_id: str
    metadata: DocumentMetadata
    chunks: List[DocumentChunk]
    raw_text: str
