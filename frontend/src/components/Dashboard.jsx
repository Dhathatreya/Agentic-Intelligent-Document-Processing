import React from 'react';

export default function Dashboard({ data, docType }) {
    if (!data) return null;

    return (
        <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ margin: 0 }}>Extraction Results</h2>
                <span style={{
                    background: 'var(--accent-secondary)',
                    padding: '0.25rem 0.75rem',
                    borderRadius: '99px',
                    fontSize: '0.875rem'
                }}>
                    {docType || 'Unknown Type'}
                </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                {Object.entries(data).map(([key, value]) => (
                    <div key={key} style={{
                        background: 'rgba(255,255,255,0.05)',
                        padding: '1rem',
                        borderRadius: '8px'
                    }}>
                        <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                            {key.replace(/_/g, ' ')}
                        </div>
                        <div style={{ fontSize: '1.125rem', fontWeight: 500 }}>
                            {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
