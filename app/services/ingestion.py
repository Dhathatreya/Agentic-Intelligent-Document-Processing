import os
import uuid
from typing import List
from fastapi import UploadFile
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.document import ProcessedDocument, DocumentMetadata, DocumentChunk

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class IngestionService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    async def save_upload(self, file: UploadFile) -> str:
        """Saves the uploaded file to disk and returns the path."""
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
            
        return filepath, file_id

    def extract_text(self, filepath: str) -> str:
        """Extracts text from a PDF file."""
        text = ""
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF {filepath}: {e}")
            # Fallback or OCR could go here
        return text

    def process_document(self, filepath: str, filename: str, file_id: str) -> ProcessedDocument:
        """Full processing pipeline: Extract -> Chunk -> Model."""
        raw_text = self.extract_text(filepath)
        
        chunks = self.text_splitter.create_documents([raw_text])
        
        doc_chunks = []
        for i, chunk in enumerate(chunks):
            doc_chunks.append(DocumentChunk(
                text=chunk.page_content,
                chunk_id=i,
                metadata={"source": filename, "chunk_index": i}
            ))

        page_count = 0
        try:
             # Re-open to get page count safely if needed, or track during extraction
             reader = PdfReader(filepath)
             page_count = len(reader.pages)
        except:
            pass

        return ProcessedDocument(
            document_id=file_id,
            metadata=DocumentMetadata(
                filename=filename,
                content_type="application/pdf",
                file_size=os.path.getsize(filepath),
                page_count=page_count
            ),
            chunks=doc_chunks,
            raw_text=raw_text
        )
