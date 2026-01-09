import requests
import os

BASE_URL = "http://localhost:8000"
FILE_PATH = "demo_contract.pdf"

def main():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    print(f"Uploading {FILE_PATH}...")
    with open(FILE_PATH, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"Upload failed: {response.text}")
        return
    
    data = response.json()
    doc_id = data.get("document_id")
    print(f"Upload successful. Document ID: {doc_id}")
    
    print(f"Triggering processing for {doc_id}...")
    proc_response = requests.post(f"{BASE_URL}/process/{doc_id}")
    
    if proc_response.status_code == 200:
        result = proc_response.json()
        if result.get('extracted_data'):
            print("Processing successful!")
            print(f"Document ID: {result.get('document_id')}")
            print(f"Doc Type: {result.get('doc_type')}")
            print(f"Data: {result.get('extracted_data')}")
        else:
             print("Processing finished but data missing.")
    else:
        print(f"Processing failed: {proc_response.text}")

if __name__ == "__main__":
    main()
