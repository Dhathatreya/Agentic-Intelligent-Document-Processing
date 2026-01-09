from app.services.ml_baseline import DocumentClassifier
import sys
import os

# Add root to python path to run as script
sys.path.append(os.getcwd())

def main():
    texts = [
        "Invoice for services rendered. Total amount: $500. Due date: 2023-10-01.",
        "Contract agreement between Party A and Party B. Terms and conditions apply.",
        "Resume: John Doe. Experience: Software Engineer at Tech Corp.",
        "Monthly financial report. Revenue increased by 20%.",
        "Invoice #12345. Please remit payment to...",
        "Employment Agreement. This contract is made effective as of...",
        "Curriculum Vitae. Education: BS Computer Science.",
        "Quarterly earnings report. Net income was...",
        "Bill to: Jane Doe. Service Charge: $100.",
        "Non-Disclosure Agreement (NDA). The parties agree to..."
    ]
    labels = [
        "invoice",
        "contract",
        "resume",
        "report",
        "invoice",
        "contract",
        "resume",
        "report",
        "invoice",
        "contract"
    ]

    print("Starting training script...")
    clf = DocumentClassifier()
    clf.train(texts, labels)
    
    # Test prediction
    test_text = "Please find attached the invoice for the last month."
    prediction = clf.predict(test_text)
    print(f"Test Prediction for '{test_text}': {prediction}")

if __name__ == "__main__":
    main()
