import asyncio
from app.services.rag import RAGService
from app.models.document import DocumentChunk

def test_rag():
    service = RAGService()
    
    # Create dummy chunks
    chunks = [
        DocumentChunk(text="The Agentic IDP platform supports PDF uploads.", chunk_id=0, metadata={"source": "doc1"}),
        DocumentChunk(text="It uses FAISS for vector storage.", chunk_id=1, metadata={"source": "doc1"}),
        DocumentChunk(text="Machine Learning models are used for classification.", chunk_id=0, metadata={"source": "doc2"})
    ]
    
    print("Indexing chunks...")
    service.index_chunks(chunks, doc_id="doc1")
    
    print("Searching for 'vector storage'...")
    results = service.search("vector storage", k=1)
    
    print(f"Found {len(results)} results.")
    if results:
        print(f"Top result: {results[0].page_content}")
        assert "FAISS" in results[0].page_content
    else:
        print("No results found!")
        assert False

    print("RAG test passed!")

if __name__ == "__main__":
    test_rag()
