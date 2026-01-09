from app.agents.workflow import WorkflowOrchestrator

def test_workflow():
    print("Initializing workflow...")
    orchestrator = WorkflowOrchestrator()
    
    # Test 1: Invoice
    text_invoice = "Invoice #001. Please pay amount: $500 by tomorrow."
    result = orchestrator.run(text_invoice, "doc_1")
    
    print("\n--- Result 1 (Invoice) ---")
    print("Classified Type:", result["doc_type"])
    print("Extracted:", result["extracted_data"])
    print("Validation:", result["validation_status"])
    
    assert result["doc_type"] == "invoice"
    assert result["extracted_data"]["amount"] == "500"
    assert result["validation_status"] == "valid"

    # Test 2: Contract
    text_contract = "Contract agreement between Party A and Party B."
    result2 = orchestrator.run(text_contract, "doc_2")
    
    print("\n--- Result 2 (Contract) ---")
    print("Classified Type:", result2["doc_type"])
    
    assert result2["doc_type"] == "contract"

    print("\nWorkflow Test Passed!")

if __name__ == "__main__":
    test_workflow()
