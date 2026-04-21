import React, { useState } from 'react';

const XRayOverlay = ({ findings }) => {
    const [overlayEnabled, setOverlayEnabled] = useState(false);

    const toggleOverlay = () => {
        setOverlayEnabled(!overlayEnabled);
        
        // Send message to content script to toggle highlights
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, {
                type: overlayEnabled ? 'REMOVE_HIGHLIGHTS' : 'HIGHLIGHT_PATTERNS'
            });
        });
    };

    const getPatternStats = () => {
        const stats = {
            total: findings.length,
            high: 0,
            medium: 0,
            low: 0,
            byEngine: {},
            byType: {}
        };

        findings.forEach(finding => {
            // Count by severity
            if (finding.severity === 'HIGH') stats.high++;
            else if (finding.severity === 'MEDIUM') stats.medium++;
            else if (finding.severity === 'LOW') stats.low++;

            // Count by engine
            if (!stats.byEngine[finding.engine]) {
                stats.byEngine[finding.engine] = 0;
            }
            stats.byEngine[finding.engine]++;

            // Count by type
            if (!stats.byType[finding.type]) {
                stats.byType[finding.type] = 0;
            }
            stats.byType[finding.type]++;
        });

        return stats;
    };

    const stats = getPatternStats();

    return (
        <div className="xray-overlay">
            <div className="xray-header">
                <h3>X-Ray Vision</h3>
                <button 
                    onClick={toggleOverlay}
                    className={`btn ${overlayEnabled ? 'btn-success' : 'btn-secondary'}`}
                >
                    {overlayEnabled ? '👁️ Overlay ON' : '👁️‍🗨️ Overlay OFF'}
                </button>
            </div>

            <div className="xray-stats">
                <div className="stat-grid">
                    <div className="stat-card">
                        <div className="stat-number">{stats.total}</div>
                        <div className="stat-label">Total Patterns</div>
                    </div>
                    
                    <div className="stat-card high-severity">
                        <div className="stat-number">{stats.high}</div>
                        <div className="stat-label">High Risk</div>
                    </div>
                    
                    <div className="stat-card medium-severity">
                        <div className="stat-number">{stats.medium}</div>
                        <div className="stat-label">Medium Risk</div>
                    </div>
                    
                    <div className="stat-card low-severity">
                        <div className="stat-number">{stats.low}</div>
                        <div className="stat-label">Low Risk</div>
                    </div>
                </div>
            </div>

            <div className="xray-breakdown">
                <div className="breakdown-section">
                    <h4>By Engine</h4>
                    <div className="engine-breakdown">
                        {Object.entries(stats.byEngine).map(([engine, count]) => (
                            <div key={engine} className="engine-stat">
                                <span className="engine-icon">
                                    {engine === 'NLP' ? '📝' : engine === 'VISUAL' ? '👁️' : '🔍'}
                                </span>
                                <span className="engine-name">{engine}</span>
                                <span className="engine-count">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="breakdown-section">
                    <h4>By Pattern Type</h4>
                    <div className="type-breakdown">
                        {Object.entries(stats.byType).map(([type, count]) => (
                            <div key={type} className="type-stat">
                                <span className="type-name">{type.replace('_', ' ')}</span>
                                <span className="type-count">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="xray-instructions">
                <h4>How to Use X-Ray Vision</h4>
                <ul>
                    <li>Click "Overlay ON" to highlight dark patterns on the page</li>
                    <li>High-risk patterns will be highlighted in red</li>
                    <li>Medium-risk patterns will be highlighted in yellow</li>
                    <li>Low-risk patterns will be highlighted in green</li>
                    <li>Hover over highlighted areas to see details</li>
                    <li>Use Ghost-Writer mode to automatically fix patterns</li>
                </ul>
            </div>

            {overlayEnabled && (
                <div className="xray-active-indicator">
                    <div className="pulse-dot"></div>
                    <span>X-Ray Vision is currently active</span>
                </div>
            )}
        </div>
    );
};

export default XRayOverlay;
