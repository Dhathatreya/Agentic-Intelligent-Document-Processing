from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import classifier_node, extractor_node, validator_node

class WorkflowOrchestrator:
    def __init__(self):
        self.workflow = StateGraph(AgentState)
        self._build_graph()
        self.app = self.workflow.compile()

    def _build_graph(self):
        # Add nodes
        self.workflow.add_node("classifier", classifier_node)
        self.workflow.add_node("extractor", extractor_node)
        self.workflow.add_node("validator", validator_node)

        # Add edges
        self.workflow.set_entry_point("classifier")
        self.workflow.add_edge("classifier", "extractor")
        self.workflow.add_edge("extractor", "validator")
        
        # Conditional edge or straight to end
        self.workflow.add_edge("validator", END)

    def run(self, text: str, doc_id: str):
        initial_state = AgentState(
            document_id=doc_id,
            text=text,
            doc_type=None,
            extracted_data=None,
            validation_status=None,
            rag_response=None,
            errors=[]
        )
        result = self.app.invoke(initial_state)
        return result
