from typing import TypedDict, List, Dict, Optional
from app.models.document import ProcessedDocument

class AgentState(TypedDict):
    document_id: str
    text: str
    doc_type: Optional[str]
    extracted_data: Optional[Dict]
    validation_status: Optional[str] # "valid", "invalid"
    rag_response: Optional[str]
    errors: Optional[List[str]]
