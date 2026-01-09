import os
import sys
import asyncio
from dotenv import load_dotenv

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ingestion import IngestionService
from app.services.rag import RAGService
from app.agents.workflow import WorkflowOrchestrator

# Load environment variables
load_dotenv()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <path_to_pdf>")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    print(f"Processing file: {filepath}...")
    
    # Initialize services
    ingestion = IngestionService()
    rag = RAGService()
    orchestrator = WorkflowOrchestrator()
    
    try:
        # 1. Ingest
        print("1. Ingesting document...")
        # specific logic to handle local path directly without upload
        filename = os.path.basename(filepath)
        doc_id = f"manual_{filename}"
        
        processed_doc = ingestion.process_document(filepath, filename, doc_id)
        print(f"   - Extracted {len(processed_doc.chunks)} chunks.")
        
        # 2. Index
        print("2. Indexing content...")
        rag.index_chunks(processed_doc.chunks, doc_id)
        
        # 3. Run Agent Workflow
        print("3. Running Agentic Workflow (Classification -> Extraction -> Validation)...")
        result = orchestrator.run(processed_doc.raw_text, doc_id)
        
        print("\n" + "="*50)
        print("PROCESSING COMPLETE")
        print("="*50)
        print(f"Document Type: {result.get('doc_type')}")
        print("Extracted Data:")
        import json
        print(json.dumps(result.get('extracted_data'), indent=2))
        print("="*50)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
