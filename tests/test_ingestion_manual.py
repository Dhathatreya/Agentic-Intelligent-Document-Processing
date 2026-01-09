import os
import asyncio
from app.services.ingestion import IngestionService
from fpdf import FPDF
from fastapi import UploadFile

# Create a dummy PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Test Document', 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_test_pdf(filename):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body("This is a test document for the Agentic IDP Platform.\n" * 20)
    pdf.output(filename)
    return filename

async def test_ingestion():
    service = IngestionService()
    test_file = "test_doc.pdf"
    
    # 1. Create a real PDF file
    create_test_pdf(test_file)
    
    # 2. Simulate UploadFile
    # In a real API, FastAPI handles this. Here we just mock what we need or pass path if we modify service.
    # Actually, service.save_upload takes UploadFile. Let's create a minimal mock/adaptor or just test process_document directly 
    # since save_upload is mostly FastAPI boilerplate.
    
    print(f"Testing extraction on {test_file}...")
    
    # We will test process_document directly assuming the file is already 'saved'
    doc_id = "test-id-123"
    processed = service.process_document(test_file, test_file, doc_id)
    
    print("Metadata:", processed.metadata)
    print("Number of chunks:", len(processed.chunks))
    print("First chunk text:", processed.chunks[0].text[:50] + "...")
    
    assert processed.metadata.filename == test_file
    assert len(processed.chunks) > 0
    assert "Agentic IDP" in processed.raw_text
    
    print("Ingestion test passed!")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    asyncio.run(test_ingestion())
