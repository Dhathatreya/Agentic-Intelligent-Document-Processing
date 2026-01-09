from app.services.rag import RAGService
import os

def test_rag_generation():
    rag = RAGService()
    # Mock some docs
    from langchain_core.documents import Document
    docs = [
        Document(page_content="The termination period is 30 days written notice.", metadata={"source": "test"})
    ]
    
    print("Testing Generation...")
    try:
        answer = rag.generate_answer("What is the termination period?", docs)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Caught Error: {e}")

if __name__ == "__main__":
    test_rag_generation()
