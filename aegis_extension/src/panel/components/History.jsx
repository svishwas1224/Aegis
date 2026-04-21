import React, { useState, useEffect } from 'react';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            // Get history from backend
            const response = await fetch('http://localhost:5000/api/get-history', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                setHistory(data);
            }
        } catch (error) {
            console.error('Failed to load history:', error);
        } finally {
            setLoading(false);
        }
    };

    const clearHistory = async () => {
        if (confirm('Are you sure you want to clear all history?')) {
            try {
                const response = await fetch('http://localhost:5000/api/clear-history', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (response.ok) {
                    setHistory([]);
                }
            } catch (error) {
                console.error('Failed to clear history:', error);
            }
        }
    };

    const getFilteredHistory = () => {
        return history.filter(item => {
            if (filter !== 'all' && item.safety_status !== filter) {
                return false;
            }
            if (searchTerm && !item.url.toLowerCase().includes(searchTerm.toLowerCase())) {
                return false;
            }
            return true;
        });
    };

    const getHistoryStats = () => {
        const stats = {
            total: history.length,
            safe: 0,
            unsafe: 0,
            suspicious: 0,
            avgTrustScore: 0
        };

        history.forEach(item => {
            if (item.safety_status === 'Safe') stats.safe++;
            else if (item.safety_status === 'Unsafe') stats.unsafe++;
            else stats.suspicious++;

            stats.avgTrustScore += item.trust_score || 0;
        });

        if (history.length > 0) {
            stats.avgTrustScore = Math.round(stats.avgTrustScore / history.length);
        }

        return stats;
    };

    const formatDate = (timestamp) => {
        return new Date(timestamp).toLocaleString();
    };

    const getRiskLevelColor = (trustScore) => {
        if (trustScore >= 75) return '#4caf50';
        if (trustScore >= 45) return '#ff9800';
        return '#f44336';
    };

    const getRiskLevel = (trustScore) => {
        if (trustScore >= 75) return 'SAFE';
        if (trustScore >= 45) return 'CAUTION';
        return 'DANGER';
    };

    const filteredHistory = getFilteredHistory();
    const stats = getHistoryStats();

    if (loading) {
        return (
            <div className="history-loading">
                <div className="loading-spinner"></div>
                <p>Loading scan history...</p>
            </div>
        );
    }

    return (
        <div className="history-panel">
            <div className="history-header">
                <h3>Scan History</h3>
                <button 
                    onClick={clearHistory}
                    className="btn btn-danger"
                    disabled={history.length === 0}
                >
                    🗑️ Clear History
                </button>
            </div>

            <div className="history-stats">
                <div className="stat-cards">
                    <div className="stat-card">
                        <div className="stat-number">{stats.total}</div>
                        <div className="stat-label">Total Scans</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.safe}</div>
                        <div className="stat-label">Safe Sites</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.unsafe + stats.suspicious}</div>
                        <div className="stat-label">Risky Sites</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.avgTrustScore}</div>
                        <div className="stat-label">Avg Trust Score</div>
                    </div>
                </div>
            </div>

            <div className="history-filters">
                <input
                    type="text"
                    placeholder="Search URLs..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                />
                
                <select 
                    value={filter} 
                    onChange={(e) => setFilter(e.target.value)}
                    className="filter-select"
                >
                    <option value="all">All Sites</option>
                    <option value="Safe">Safe Only</option>
                    <option value="Unsafe">Unsafe Only</option>
                    <option value="Unknown">Unknown</option>
                </select>
            </div>

            <div className="history-list">
                {filteredHistory.length === 0 ? (
                    <div className="no-history">
                        <div className="empty-icon">📋</div>
                        <h4>No Scan History</h4>
                        <p>
                            {history.length === 0 
                                ? 'Start scanning websites to build your history.'
                                : 'No results match your current filters.'
                            }
                        </p>
                    </div>
                ) : (
                    filteredHistory.map((item, index) => (
                        <div key={item._id || index} className="history-item">
                            <div className="history-item-header">
                                <div className="url-info">
                                    <h4 className="url-title">
                                        {item.url.length > 50 
                                            ? item.url.substring(0, 50) + '...' 
                                            : item.url
                                        }
                                    </h4>
                                    <small className="scan-date">
                                        {formatDate(item.timestamp)}
                                    </small>
                                </div>
                                
                                <div className="trust-indicator">
                                    <div 
                                        className="trust-score-badge"
                                        style={{ backgroundColor: getRiskLevelColor(item.trust_score) }}
                                    >
                                        {item.trust_score}
                                    </div>
                                    <div className="risk-level">
                                        {getRiskLevel(item.trust_score)}
                                    </div>
                                </div>
                            </div>

                            <div className="history-item-details">
                                <div className="scan-info">
                                    <span className="info-item">
                                        <strong>Patterns Found:</strong> {item.total_patterns_found || 0}
                                    </span>
                                    <span className="info-item">
                                        <strong>Type:</strong> {item.type || 'url'}
                                    </span>
                                    <span className="info-item">
                                        <strong>Status:</strong> {item.safety_status}
                                    </span>
                                </div>

                                {item.conclusion && (
                                    <div className="scan-conclusion">
                                        <strong>Conclusion:</strong> {item.conclusion}
                                    </div>
                                )}

                                {item.findings && item.findings.length > 0 && (
                                    <div className="findings-preview">
                                        <strong>Top Findings:</strong>
                                        <ul>
                                            {item.findings.slice(0, 3).map((finding, i) => (
                                                <li key={i}>{finding}</li>
                                            ))}
                                            {item.findings.length > 3 && (
                                                <li className="more-findings">
                                                    +{item.findings.length - 3} more...
                                                </li>
                                            )}
                                        </ul>
                                    </div>
                                )}
                            </div>

                            <div className="history-actions">
                                <button 
                                    className="btn btn-secondary btn-sm"
                                    onClick={() => {
                                        // Navigate to the URL for re-analysis
                                        chrome.tabs.create({ url: item.url });
                                    }}
                                >
                                    🔍 Re-analyze
                                </button>
                                
                                <button 
                                    className="btn btn-secondary btn-sm"
                                    onClick={() => {
                                        // Copy URL to clipboard
                                        navigator.clipboard.writeText(item.url);
                                    }}
                                >
                                    📋 Copy URL
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default History;
