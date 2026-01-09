from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_api():
    # 1. Root
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Agentic IDP Platform API is running"}
    print("Root endpoint passed.")

    # 2. Upload
    # Create a dummy PDF file content
    dummy_pdf_content = b"%PDF-1.4 ... dummy content ..."
    test_filename = "api_test.pdf"
    
    # We need a valid PDF for pypdf usually, but our mock ingestion might fail if not valid.
    # Actually, pypdf will fail on dummy content. 
    # Let's use the 'create_test_pdf' helper logic or just use the one from previous test if exists.
    # Or simplified: The 'IngestionService' uses pypdf.
    # So we need a real PDF.
    
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Invoice #999. Amount: $1000.')
    pdf.output(test_filename)

    with open(test_filename, "rb") as f:
        files = {"file": (test_filename, f, "application/pdf")}
        response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    doc_id = data["document_id"]
    print(f"Upload passed. Doc ID: {doc_id}")

    # 3. Process
    process_response = client.post(f"/process/{doc_id}")
    assert process_response.status_code == 200
    p_data = process_response.json()
    print("Process Result:", p_data)
    
    assert p_data["doc_type"] == "invoice"
    assert p_data["extracted_data"]["amount"] == "1000"
    
    # 4. Query
    query_payload = {"query": "amount", "k": 1}
    query_response = client.post("/query", json=query_payload)
    assert query_response.status_code == 200
    print("Query Result:", query_response.json())
    
    # Clean up
    if os.path.exists(test_filename):
        os.remove(test_filename)
        
    print("API Test Passed!")

if __name__ == "__main__":
    test_api()
