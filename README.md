# Agentic Intelligent Document Processing (IDP) Platform

An advanced document processing platform that leverages **Multi-Agent AI** and **Retrieval-Augmented Generation (RAG)** to intelligently ingest, classify, extract, and validate information from documents. Built with **FastAPI**, **LangChain**, and **LangGraph**, this system orchestrates autonomous agents to handle complex document workflows.

## 🚀 Features

-   **Intelligent Ingestion**: Seamlessly upload and process PDF documents.
-   **RAG Pipeline**:
    -   **Embeddings**: Uses HuggingFace `sentence-transformers/all-MiniLM-L6-v2` for high-quality text embeddings.
    -   **Vector Search**: efficient similarity search using **FAISS** (Facebook AI Similarity Search).
    -   **Contextual Querying**: Retrieve relevant document chunks to answer user queries.
-   **Multi-Agent Workflow (LangGraph)**:
    -   **Classifier Agent**: Determines the document type.
    -   **Extractor Agent**: Pulls structured data based on the document type.
    -   **Validator Agent**: Ensures extracted data meets quality and format standards.
    -   **Orchestration**: A state-machine based workflow manages the lifecycle of document processing.
-   **Modern API**: High-performance REST API built with **FastAPI**.
-   **Interactive Frontend**: User-friendly interface built with **React** and **Vite** for easy document uploads and querying.

## 🛠️ Tech Stack

### Core Frameworks
-   **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast web framework for building APIs with Python.
-   **[LangChain](https://www.langchain.com/)**: Framework for developing applications powered by language models.
-   **[LangGraph](https://python.langchain.com/docs/langgraph)**: Library for building stateful, multi-agent applications with LLMs.

### Frontend
-   **[React](https://react.dev/)**: Library for building user interfaces.
-   **[Vite](https://vitejs.dev/)**: Next Generation Frontend Tooling.
-   **Vanilla CSS**: Custom styling for a responsive and modern UI.

### AI & Machine Learning
-   **[HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)**: Open-source embedding models for semantic search.
-   **[FAISS](https://github.com/facebookresearch/faiss)**: Efficient similarity search and clustering of dense vectors.
-   **[PyTorch](https://pytorch.org/)** / **Transformers**: Underlying libraries for model inference.

### Data Processing
-   **[PyPDF](https://pypi.org/project/pypdf/)**: PDF reading and manipulation.
-   **[Pandas](https://pandas.pydata.org/)** & **[NumPy](https://numpy.org/)**: Data analysis and manipulation.
-   **Pytesseract**: (Planned/Dependency) OCR capability for scanned documents.

### Infrastructure & Tools
-   **[Uvicorn](https://www.uvicorn.org/)**: ASGI web server implementation.
-   **Dotenv**: Environment variable management.

## 📂 Project Structure

```bash
├── app/
│   ├── agents/          # LangGraph agents (Nodes, State, Workflow)
│   ├── services/        # Business logic (Ingestion, RAG)
│   ├── models/          # Pydantic models for API and internal data
│   └── ...
├── frontend/            # React + Vite Frontend application
│   ├── src/             # Frontend source code
│   └── package.json     # Frontend dependencies
├── data/
│   ├── uploads/         # Stored uploaded documents
│   └── vector_store/    # FAISS index persistence
├── tests/               # Unit and integration tests
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## ⚡ Getting Started

### Prerequisites
-   Python 3.9+
-   Pip (Python package manager)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Frontend Dependencies**:
    ```bash
    cd frontend
    npm install
    cd ..
    ```

4.  **Configure Environment**:
    Create a `.env` file (if needed by specific agents/services):
    ```env
    # Example
    OPENAI_API_KEY=your_key_here
    ```

### Running the Application

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Running the Frontend

In a new terminal window:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### Documentation

Visit `http://127.0.0.1:8000/docs` to see the interactive Swagger UI and test the endpoints.

## 🔄 API Workflows

1.  **Upload Document**:
    -   `POST /upload`: Send a PDF file. Returns a `document_id`.
2.  **Process Document**:
    -   `POST /process/{document_id}`: Triggers the multi-agent workflow (Classify -> Extract -> Validate) and indexes the content for RAG.
3.  **Query System**:
    -   `POST /query`: Ask questions about the processed documents.

## 🧪 Testing

Run the test suite to verify functionality:

```bash
pytest
```
