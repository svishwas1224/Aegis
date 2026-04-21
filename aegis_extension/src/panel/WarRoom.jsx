import React, { useState, useEffect } from 'react';
import TrustScore from './components/TrustScore';
import XRayOverlay from './components/XRayOverlay';
import EvidenceLog from './components/EvidenceLog';
import Heatmap from './components/Heatmap';
import Remediation from './components/Remediation';
import History from './components/History';
import '../styles/panel.css';

const WarRoom = () => {
    const [analysis, setAnalysis] = useState(null);
    const [ghostWriterEnabled, setGhostWriterEnabled] = useState(false);
    const [activeTab, setActiveTab] = useState('overview');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Request current analysis from background script
        chrome.runtime.sendMessage({ type: 'GET_CURRENT_ANALYSIS' }, (response) => {
            if (response && response.analysis) {
                setAnalysis(response.analysis);
            }
        });

        // Listen for analysis updates
        const messageListener = (message) => {
            if (message.type === 'ANALYSIS_COMPLETE') {
                setAnalysis(message.analysis);
                setLoading(false);
                setError(null);
            } else if (message.type === 'ANALYSIS_ERROR') {
                setError(message.error);
                setLoading(false);
            }
        };

        chrome.runtime.onMessage.addListener(messageListener);
        return () => chrome.runtime.onMessage.removeListener(messageListener);
    }, []);

    const toggleGhostWriter = () => {
        const newState = !ghostWriterEnabled;
        setGhostWriterEnabled(newState);
        
        chrome.runtime.sendMessage({
            type: 'TOGGLE_GHOST_WRITER',
            enabled: newState
        }, (response) => {
            if (response && response.success) {
                setGhostWriterEnabled(response.enabled);
            }
        });
    };

    const rerunAnalysis = async () => {
        setLoading(true);
        setError(null);
        
        chrome.runtime.sendMessage({ type: 'ANALYZE_PAGE' }, (response) => {
            if (!response || !response.success) {
                setError('Failed to start analysis');
                setLoading(false);
            }
        });
    };

    const getRiskLevelColor = (riskLevel) => {
        const colors = {
            'SAFE': '#4caf50',
            'CAUTION': '#ff9800',
            'DANGER': '#f44336'
        };
        return colors[riskLevel] || '#9e9e9e';
    };

    if (!analysis) {
        return (
            <div className="war-room loading">
                <div className="loading-spinner"></div>
                <p>Initializing Aegis Pro...</p>
                <button onClick={rerunAnalysis} className="btn btn-primary">
                    Analyze Current Page
                </button>
            </div>
        );
    }

    return (
        <div className="war-room">
            {/* Header */}
            <div className="war-room-header">
                <div className="header-left">
                    <h1>Aegis Pro War Room</h1>
                    <div className="url-display">
                        <small>{analysis.url}</small>
                    </div>
                </div>
                <div className="header-right">
                    <button 
                        onClick={toggleGhostWriter}
                        className={`btn ${ghostWriterEnabled ? 'btn-success' : 'btn-secondary'}`}
                    >
                        {ghostWriterEnabled ? '🛡️ Ghost-Writer ON' : '👻 Ghost-Writer OFF'}
                    </button>
                    <button onClick={rerunAnalysis} className="btn btn-primary">
                        🔄 Re-analyze
                    </button>
                </div>
            </div>

            {/* Trust Score Display */}
            <div className="trust-score-section">
                <TrustScore 
                    score={analysis.trust_score} 
                    riskLevel={analysis.risk_level}
                    status={analysis.status}
                />
                <div className="summary-text">
                    <p>{analysis.summary}</p>
                </div>
            </div>

            {/* Tab Navigation */}
            <div className="tab-navigation">
                {['overview', 'evidence', 'remediation', 'heatmap', 'history'].map(tab => (
                    <button
                        key={tab}
                        className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab)}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                ))}
            </div>

            {/* Tab Content */}
            <div className="tab-content">
                {activeTab === 'overview' && (
                    <div className="overview-tab">
                        <div className="overview-grid">
                            <div className="overview-card">
                                <h3>Engines Used</h3>
                                <div className="engines-list">
                                    {analysis.engines_used.map(engine => (
                                        <span key={engine} className="engine-badge">
                                            {engine}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            
                            <div className="overview-card">
                                <h3>Patterns Found</h3>
                                <div className="patterns-count">
                                    <span className="count-number">{analysis.patterns_found}</span>
                                    <span className="count-label">Total Issues</span>
                                </div>
                            </div>
                            
                            <div className="overview-card">
                                <h3>Engine Scores</h3>
                                <div className="engine-scores">
                                    {Object.entries(analysis.engine_scores || {}).map(([engine, score]) => (
                                        <div key={engine} className="engine-score">
                                            <span>{engine}:</span>
                                            <span style={{ color: getRiskLevelColor(score >= 75 ? 'SAFE' : score >= 45 ? 'CAUTION' : 'DANGER') }}>
                                                {score}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        
                        <XRayOverlay findings={analysis.findings} />
                    </div>
                )}

                {activeTab === 'evidence' && (
                    <EvidenceLog findings={analysis.findings} />
                )}

                {activeTab === 'remediation' && (
                    <Remediation findings={analysis.findings} />
                )}

                {activeTab === 'heatmap' && (
                    <Heatmap findings={analysis.findings} />
                )}

                {activeTab === 'history' && (
                    <History />
                )}
            </div>

            {/* Loading Overlay */}
            {loading && (
                <div className="loading-overlay">
                    <div className="loading-spinner"></div>
                    <p>Analyzing page...</p>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className="error-display">
                    <p>❌ {error}</p>
                    <button onClick={rerunAnalysis} className="btn btn-primary">
                        Try Again
                    </button>
                </div>
            )}
        </div>
    );
};

export default WarRoom;
