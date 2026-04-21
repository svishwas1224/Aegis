import React, { useState, useEffect, useRef } from 'react';

const Heatmap = ({ findings }) => {
    const canvasRef = useRef(null);
    const [heatmapMode, setHeatmapMode] = useState('severity');
    const [showOverlay, setShowOverlay] = useState(false);

    useEffect(() => {
        if (showOverlay && canvasRef.current) {
            drawHeatmap();
        }
    }, [showOverlay, heatmapMode, findings]);

    const drawHeatmap = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const width = canvas.width = window.innerWidth;
        const height = canvas.height = window.innerHeight;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Create heatmap data
        findings.forEach(finding => {
            if (finding.bbox) {
                const [x, y, w, h] = finding.bbox;
                const intensity = getIntensity(finding);
                
                // Draw heat rectangle
                ctx.fillStyle = getHeatColor(intensity);
                ctx.globalAlpha = 0.6;
                ctx.fillRect(x, y, w, h);
                
                // Add gradient effect
                const gradient = ctx.createRadialGradient(
                    x + w/2, y + h/2, 0,
                    x + w/2, y + h/2, Math.max(w, h)
                );
                gradient.addColorStop(0, getHeatColor(intensity));
                gradient.addColorStop(1, 'transparent');
                ctx.fillStyle = gradient;
                ctx.globalAlpha = 0.4;
                ctx.fillRect(x - w/2, y - h/2, w * 2, h * 2);
            }
        });

        ctx.globalAlpha = 1;
    };

    const getIntensity = (finding) => {
        if (heatmapMode === 'severity') {
            const severityMap = { 'HIGH': 1.0, 'MEDIUM': 0.6, 'LOW': 0.3 };
            return severityMap[finding.severity] || 0.3;
        } else if (heatmapMode === 'type') {
            // Different intensities for different pattern types
            const typeMap = {
                'confirm_shaming': 1.0,
                'urgency': 0.8,
                'scarcity': 0.7,
                'misdirection': 0.9,
                'forced_action': 0.8,
                'low_contrast': 0.6,
                'small_touch_target': 0.5,
                'hidden_element': 0.9
            };
            return typeMap[finding.type] || 0.4;
        }
        return 0.5;
    };

    const getHeatColor = (intensity) => {
        // Red to yellow gradient
        const r = 255;
        const g = Math.floor(255 * (1 - intensity));
        const b = 0;
        return `rgb(${r}, ${g}, ${b})`;
    };

    const toggleOverlay = () => {
        setShowOverlay(!showOverlay);
        if (!showOverlay) {
            // Send message to content script to show heatmap
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'SHOW_HEATMAP',
                    mode: heatmapMode
                });
            });
        } else {
            // Hide heatmap
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'HIDE_HEATMAP'
                });
            });
        }
    };

    const getHeatmapStats = () => {
        const stats = {
            total: findings.length,
            bySeverity: { HIGH: 0, MEDIUM: 0, LOW: 0 },
            byType: {},
            byEngine: { NLP: 0, VISUAL: 0, BEHAVIORAL: 0 },
            coverage: 0
        };

        findings.forEach(finding => {
            // Count by severity
            stats.bySeverity[finding.severity]++;

            // Count by type
            if (!stats.byType[finding.type]) {
                stats.byType[finding.type] = 0;
            }
            stats.byType[finding.type]++;

            // Count by engine
            stats.byEngine[finding.engine]++;

            // Calculate coverage (simplified)
            if (finding.bbox) {
                const [x, y, w, h] = finding.bbox;
                stats.coverage += (w * h) / (window.innerWidth * window.innerHeight);
            }
        });

        stats.coverage = Math.min(100, stats.coverage * 100); // Cap at 100%
        return stats;
    };

    const stats = getHeatmapStats();

    return (
        <div className="heatmap-panel">
            <div className="heatmap-header">
                <h3>Dark Pattern Heatmap</h3>
                <div className="heatmap-controls">
                    <select 
                        value={heatmapMode} 
                        onChange={(e) => setHeatmapMode(e.target.value)}
                        className="mode-select"
                    >
                        <option value="severity">By Severity</option>
                        <option value="type">By Pattern Type</option>
                    </select>
                    
                    <button 
                        onClick={toggleOverlay}
                        className={`btn ${showOverlay ? 'btn-danger' : 'btn-secondary'}`}
                    >
                        {showOverlay ? '🔥 Hide Heatmap' : '🗺️ Show Heatmap'}
                    </button>
                </div>
            </div>

            <div className="heatmap-stats">
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-number">{stats.total}</div>
                        <div className="stat-label">Hotspots</div>
                    </div>
                    
                    <div className="stat-card">
                        <div className="stat-number">{stats.coverage.toFixed(1)}%</div>
                        <div className="stat-label">Page Coverage</div>
                    </div>
                    
                    <div className="stat-card">
                        <div className="stat-number">{stats.bySeverity.HIGH}</div>
                        <div className="stat-label">Critical Zones</div>
                    </div>
                </div>
            </div>

            <div className="heatmap-legend">
                <h4>Intensity Legend</h4>
                <div className="legend-items">
                    <div className="legend-item">
                        <div className="legend-color high-intensity"></div>
                        <span>Critical (High Severity)</span>
                    </div>
                    <div className="legend-item">
                        <div className="legend-color medium-intensity"></div>
                        <span>Warning (Medium Severity)</span>
                    </div>
                    <div className="legend-item">
                        <div className="legend-color low-intensity"></div>
                        <span>Caution (Low Severity)</span>
                    </div>
                </div>
            </div>

            <div className="heatmap-distribution">
                <div className="distribution-section">
                    <h4>By Severity</h4>
                    <div className="severity-bars">
                        <div className="bar-item">
                            <span>High</span>
                            <div className="bar-container">
                                <div 
                                    className="bar high-bar"
                                    style={{ width: `${(stats.bySeverity.HIGH / stats.total) * 100}%` }}
                                ></div>
                            </div>
                            <span>{stats.bySeverity.HIGH}</span>
                        </div>
                        <div className="bar-item">
                            <span>Medium</span>
                            <div className="bar-container">
                                <div 
                                    className="bar medium-bar"
                                    style={{ width: `${(stats.bySeverity.MEDIUM / stats.total) * 100}%` }}
                                ></div>
                            </div>
                            <span>{stats.bySeverity.MEDIUM}</span>
                        </div>
                        <div className="bar-item">
                            <span>Low</span>
                            <div className="bar-container">
                                <div 
                                    className="bar low-bar"
                                    style={{ width: `${(stats.bySeverity.LOW / stats.total) * 100}%` }}
                                ></div>
                            </div>
                            <span>{stats.bySeverity.LOW}</span>
                        </div>
                    </div>
                </div>

                <div className="distribution-section">
                    <h4>By Engine</h4>
                    <div className="engine-distribution">
                        <div className="engine-stat">
                            <span>📝 NLP</span>
                            <span>{stats.byEngine.NLP}</span>
                        </div>
                        <div className="engine-stat">
                            <span>👁️ Visual</span>
                            <span>{stats.byEngine.VISUAL}</span>
                        </div>
                        <div className="engine-stat">
                            <span>🔍 Behavioral</span>
                            <span>{stats.byEngine.BEHAVIORAL}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="heatmap-instructions">
                <h4>How to Use the Heatmap</h4>
                <ul>
                    <li>Click "Show Heatmap" to overlay intensity map on the page</li>
                    <li>Red areas indicate high-severity dark patterns</li>
                    <li>Yellow areas show medium-severity issues</li>
                    <li>Green areas indicate low-severity patterns</li>
                    <li>Switch between "By Severity" and "By Pattern Type" views</li>
                    <li>Use this to identify problematic areas at a glance</li>
                </ul>
            </div>

            {showOverlay && (
                <div className="heatmap-active-indicator">
                    <div className="pulse-dot"></div>
                    <span>Heatmap overlay is active on the page</span>
                </div>
            )}
        </div>
    );
};

export default Heatmap;
