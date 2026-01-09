import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';

function App() {
  const [docId, setDocId] = useState(null);
  const [extractionResult, setExtractionResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUpload = async (file) => {
    setIsProcessing(true);
    try {
      // 1. Upload
      const formData = new FormData();
      formData.append('file', file);

      const uploadRes = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData
      });
      const uploadData = await uploadRes.json();
      const id = uploadData.document_id;
      setDocId(id);

      // 2. Process
      const processRes = await fetch(`http://127.0.0.1:8000/process/${id}`, {
        method: 'POST'
      });
      const processData = await processRes.json();
      setExtractionResult(processData);

    } catch (err) {
      console.error(err);
      alert("Error processing document");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="app-container">
      <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <h1 className="title-gradient" style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>
          Agentic IDP
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem' }}>
          Intelligent Document Processing with Multi-Agent AI
        </p>
      </header>

      <UploadZone onUpload={handleUpload} isUploading={isProcessing} />

      {extractionResult && (
        <>
          <Dashboard
            data={extractionResult.extracted_data}
            docType={extractionResult.doc_type}
          />
          <ChatInterface />
        </>
      )}
    </div>
  );
}

export default App;
