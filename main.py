from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.ingestion import IngestionService
import uvicorn
import os

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.services.rag import RAGService
from pydantic import BaseModel

ingestion_service = IngestionService()
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Agentic IDP API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        filepath, file_id = await ingestion_service.save_upload(file)
        return {"document_id": file_id, "filename": file.filename, "message": "Upload successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/{document_id}")
async def process_document(document_id: str):
    upload_dir = "data/uploads"
    files = os.listdir(upload_dir)
    target_file = next((f for f in files if f.startswith(document_id)), None)
    
    if not target_file:
        raise HTTPException(status_code=404, detail="Document not found")
    
    filepath = os.path.join(upload_dir, target_file)
    
    try:
        processed_doc = ingestion_service.process_document(filepath, target_file, document_id)
        
        # Index document chunks for RAG
        rag_service.index_chunks(processed_doc.chunks, document_id)
        
        return {
            "document_id": document_id,
            "doc_type": "PDF Document",
            "extracted_data": {
                "Filename": target_file,
                "File Size": f"{processed_doc.metadata.file_size} bytes",
                "Page Count": processed_doc.metadata.page_count,
                 "Chunk Count": len(processed_doc.chunks),
                "Content Preview": processed_doc.raw_text[:200] + "..." if processed_doc.raw_text else "No text extracted"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/query")
async def query_document(request: QueryRequest):
    try:
        docs = rag_service.search(request.query)
        answer = rag_service.generate_answer(request.query, docs)
        return {
            "answer": answer,
            "sources": [{"text": d.page_content, "metadata": d.metadata} for d in docs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
