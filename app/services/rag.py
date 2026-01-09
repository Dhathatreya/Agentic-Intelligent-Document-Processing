import os
from typing import List
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.models.document import DocumentChunk

VECTOR_STORE_PATH = "data/vector_store"
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

class RAGService:
    def __init__(self):
        print("Loading embeddings...")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = self.load_vector_store()

    def load_vector_store(self):
        if os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss")):
            try:
                print("Loading existing vector store...")
                return FAISS.load_local(VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                print(f"Error loading vector store: {e}")
                return self.create_new_store()
        else:
            return self.create_new_store()

    def create_new_store(self):
        print("Creating new vector store...")
        # Initialize with a dummy doc to create the structure if needed, or just return basic
        # FAISS needs at least one doc to init? Or we can use from_texts
        # We'll just init an empty one using from_texts with a dummy if needed
        # But commonly we just wait until first index.
        # Let's return None and handle lazy init or init with empty list if possible.
        # FAISS.from_documents([], embedding) might fail.
        # We will initialize it when first document is added if it doesn't exist.
        return None

    def index_chunks(self, chunks: List[DocumentChunk], doc_id: str):
        documents = [
            Document(page_content=chunk.text, metadata={**chunk.metadata, "doc_id": doc_id})
            for chunk in chunks
        ]
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"Indexed {len(documents)} chunks from {doc_id}")

    def search(self, query: str, k: int = 3) -> List[Document]:
        if self.vector_store is None:
            return []
        
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        if not context_docs:
            return "I couldn't find any relevant information in the documents."
            
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            import traceback
            # Using gemini-flash-latest
            llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.7)
            
            context_text = "\n\n".join([d.page_content for d in context_docs])
            prompt = f"""You are an intelligent assistant. Answer the question based ONLY on the following context. If the answer is not in the context, say "I don't know".

Context:
{context_text}

Question: {query}
Answer:"""
            
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error generating answer: {e}")
            traceback.print_exc()
            return "Sorry, I encountered an error while generating the answer."
