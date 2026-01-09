from app.agents.state import AgentState
from app.services.ml_baseline import DocumentClassifier
from app.services.rag import RAGService
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize services (singleton-ish for this demo)
classifier = DocumentClassifier()
rag_service = RAGService()

def classifier_node(state: AgentState) -> Dict:
    print("--- Classifier Agent ---")
    doc_text = state.get("text", "")
    prediction = classifier.predict(doc_text)
    print(f"Classified as: {prediction}")
    return {"doc_type": prediction}

def extractor_node(state: AgentState) -> Dict:
    print("--- Extractor Agent ---")
    doc_type = state.get("doc_type")
    text = state.get("text", "")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import PromptTemplate
        import json
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)
        
        prompt_template = """Extract the following information from the document text below. Return ONLY a valid JSON object.
        
        Document Type: {doc_type}
        
        If Invoice: extract "amount" (number), "date", "vendor_name".
        If Contract: extract "parties" (list of names), "effective_date", "contract_value".
        If Other/Unknown: try to extract "summary", "dates", "entities".
        
        Document Text:
        {text}
        
        JSON Output:"""
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["doc_type", "text"])
        chain = prompt | llm
        
        response = chain.invoke({"doc_type": doc_type, "text": text[:2000]}) # Limit text context window
        
        # Clean response to ensure json
        content = response.content.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(content)
        
    except Exception as e:
        print(f"Extraction Error: {e}")
        # Fallback
        extracted = {"error": str(e)}

    return {"extracted_data": extracted}

def validator_node(state: AgentState) -> Dict:
    print("--- Validator Agent ---")
    data = state.get("extracted_data", {})
    if data:
        return {"validation_status": "valid"}
    else:
        return {"validation_status": "invalid", "errors": ["No data extracted"]}

def reasoning_node(state: AgentState) -> Dict:
    # Optional node if question is present, but for ingestion flow we might skip
    return {}
