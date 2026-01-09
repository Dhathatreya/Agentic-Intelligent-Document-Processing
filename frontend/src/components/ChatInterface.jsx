import React, { useState } from 'react';

export default function ChatInterface() {
    const [query, setQuery] = useState('');
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleAsk = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        const userQ = query;
        setQuery('');
        setHistory(prev => [...prev, { role: 'user', content: userQ }]);
        setLoading(true);

        try {
            const res = await fetch('http://127.0.0.1:8000/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userQ })
            });
            const data = await res.json();
            setHistory(prev => [...prev, { role: 'ai', content: data.answer }]);
        } catch (err) {
            setHistory(prev => [...prev, { role: 'ai', content: "Error: Could not fetch answer." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-panel" style={{ padding: '2rem', height: '500px', display: 'flex', flexDirection: 'column' }}>
            <h2 style={{ marginTop: 0 }}>Ask your Document</h2>

            <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', paddingRight: '0.5rem' }}>
                {history.length === 0 && (
                    <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>
                        Ask anything about your document...
                    </div>
                )}
                {history.map((msg, idx) => (
                    <div key={idx} style={{
                        marginBottom: '1rem',
                        textAlign: msg.role === 'user' ? 'right' : 'left'
                    }}>
                        <div style={{
                            display: 'inline-block',
                            maxWidth: '80%',
                            padding: '0.75rem 1rem',
                            borderRadius: '12px',
                            background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-secondary)',
                            color: 'var(--text-primary)',
                            borderBottomRightRadius: msg.role === 'user' ? '2px' : '12px',
                            borderBottomLeftRadius: msg.role === 'ai' ? '2px' : '12px'
                        }}>
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && <div style={{ color: 'var(--text-secondary)' }}>Thinking...</div>}
            </div>

            <form onSubmit={handleAsk} style={{ display: 'flex', gap: '0.5rem' }}>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Type your question..."
                    style={{
                        flex: 1,
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--border-color)',
                        padding: '0.75rem',
                        borderRadius: '8px',
                        color: 'white'
                    }}
                />
                <button type="submit" className="btn-primary" disabled={loading}>
                    Send
                </button>
            </form>
        </div>
    );
}
