import requests
import sys

BASE_URL = "http://localhost:8000"

def test_query():
    query = "What is the termination period?"
    print(f"Asking: '{query}'")
    
    try:
        response = requests.post(f"{BASE_URL}/query", json={"query": query})
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer')}")
            print(f"Sources: {len(data.get('sources', []))}")
            if data.get('sources'):
                 print("Source Snippets:")
                 # We can't see the text unless the API returns it.
                 # App.py source includes metadata but not text?
                 # main.py: return {"answer": answer, "sources": [d.metadata for d in docs]}
                 # So we only see metadata.
                 print(data.get('sources'))
        else:
            print(f"Query Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_query()
