import React, { useCallback } from 'react';

export default function UploadZone({ onUpload, isUploading }) {
    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            onUpload(file);
        }
    };

    return (
        <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
            <input
                type="file"
                id="fileInput"
                accept=".pdf"
                onChange={handleFileChange}
                style={{ display: 'none' }}
                disabled={isUploading}
            />
            <label htmlFor="fileInput" style={{ cursor: 'pointer', display: 'block' }}>
                <div style={{
                    border: '2px dashed var(--border-color)',
                    borderRadius: '12px',
                    padding: '3rem',
                    transition: 'border-color 0.2s'
                }}>
                    <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>📄</span>
                    <h3 style={{ margin: '0 0 0.5rem 0' }}>Upload your Document</h3>
                    <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                        {isUploading ? 'Uploading & Processing...' : 'Click to select a PDF file'}
                    </p>
                </div>
            </label>
        </div>
    );
}
