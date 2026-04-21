import React, { useState } from 'react';

const Remediation = ({ findings }) => {
    const [selectedFindings, setSelectedFindings] = useState(new Set());
    const [ghostWriterMode, setGhostWriterMode] = useState(false);

    const toggleFindingSelection = (index) => {
        const newSelected = new Set(selectedFindings);
        if (newSelected.has(index)) {
            newSelected.delete(index);
        } else {
            newSelected.add(index);
        }
        setSelectedFindings(newSelected);
    };

    const toggleGhostWriter = () => {
        const newState = !ghostWriterMode;
        setGhostWriterMode(newState);
        
        chrome.runtime.sendMessage({
            type: 'TOGGLE_GHOST_WRITER',
            enabled: newState
        });
    };

    const getPrioritizedRemediations = () => {
        // Group findings by severity and type
        const prioritized = {
            high: [],
            medium: [],
            low: []
        };

        findings.forEach((finding, index) => {
            const item = { ...finding, index };
            if (finding.severity === 'HIGH') {
                prioritized.high.push(item);
            } else if (finding.severity === 'MEDIUM') {
                prioritized.medium.push(item);
            } else {
                prioritized.low.push(item);
            }
        });

        return prioritized;
    };

    const getRemediationStats = () => {
        const stats = {
            total: findings.length,
            fixable: 0,
            automated: 0,
            manual: 0
        };

        findings.forEach(finding => {
            if (finding.remediation && finding.remediation !== 'N/A') {
                stats.fixable++;
                if (finding.engine === 'NLP') {
                    stats.automated++;
                } else {
                    stats.manual++;
                }
            }
        });

        return stats;
    };

    const prioritized = getPrioritizedRemediations();
    const stats = getRemediationStats();

    return (
        <div className="remediation-panel">
            <div className="remediation-header">
                <h3>Remediation Center</h3>
                <button 
                    onClick={toggleGhostWriter}
                    className={`btn ${ghostWriterMode ? 'btn-success' : 'btn-secondary'}`}
                >
                    {ghostWriterMode ? '🛡️ Ghost-Writer Active' : '👻 Enable Ghost-Writer'}
                </button>
            </div>

            <div className="remediation-stats">
                <div className="stat-cards">
                    <div className="stat-card">
                        <div className="stat-number">{stats.total}</div>
                        <div className="stat-label">Total Issues</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.fixable}</div>
                        <div className="stat-label">Fixable</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.automated}</div>
                        <div className="stat-label">Auto-Fixable</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-number">{stats.manual}</div>
                        <div className="stat-label">Manual Fix</div>
                    </div>
                </div>
            </div>

            {ghostWriterMode && (
                <div className="ghost-writer-status">
                    <div className="status-indicator active"></div>
                    <span>Ghost-Writer is actively fixing patterns on this page</span>
                </div>
            )}

            <div className="remediation-content">
                {/* High Priority Issues */}
                {prioritized.high.length > 0 && (
                    <div className="priority-section high-priority">
                        <h4>🚨 High Priority - Fix Immediately</h4>
                        {prioritized.high.map((finding) => (
                            <RemediationItem
                                key={finding.index}
                                finding={finding}
                                isSelected={selectedFindings.has(finding.index)}
                                onToggle={() => toggleFindingSelection(finding.index)}
                                ghostWriterMode={ghostWriterMode}
                            />
                        ))}
                    </div>
                )}

                {/* Medium Priority Issues */}
                {prioritized.medium.length > 0 && (
                    <div className="priority-section medium-priority">
                        <h4>⚠️ Medium Priority - Recommended Fixes</h4>
                        {prioritized.medium.map((finding) => (
                            <RemediationItem
                                key={finding.index}
                                finding={finding}
                                isSelected={selectedFindings.has(finding.index)}
                                onToggle={() => toggleFindingSelection(finding.index)}
                                ghostWriterMode={ghostWriterMode}
                            />
                        ))}
                    </div>
                )}

                {/* Low Priority Issues */}
                {prioritized.low.length > 0 && (
                    <div className="priority-section low-priority">
                        <h4>💡 Low Priority - Optional Improvements</h4>
                        {prioritized.low.map((finding) => (
                            <RemediationItem
                                key={finding.index}
                                finding={finding}
                                isSelected={selectedFindings.has(finding.index)}
                                onToggle={() => toggleFindingSelection(finding.index)}
                                ghostWriterMode={ghostWriterMode}
                            />
                        ))}
                    </div>
                )}

                {findings.length === 0 && (
                    <div className="no-issues">
                        <div className="success-icon">🎉</div>
                        <h4>No Issues Found!</h4>
                        <p>This page appears to follow ethical design practices.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

const RemediationItem = ({ finding, isSelected, onToggle, ghostWriterMode }) => {
    const getEngineIcon = (engine) => {
        const icons = {
            'NLP': '📝',
            'VISUAL': '👁️',
            'BEHAVIORAL': '🔍'
        };
        return icons[engine] || '📋';
    };

    const isAutomaticallyFixable = finding.engine === 'NLP' && finding.remediation;

    return (
        <div className={`remediation-item ${isSelected ? 'selected' : ''}`}>
            <div className="remediation-item-header">
                <div className="remediation-meta">
                    <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={onToggle}
                        className="remediation-checkbox"
                    />
                    <span className="engine-icon">{getEngineIcon(finding.engine)}</span>
                    <span className="finding-type">{finding.type}</span>
                    <span className={`severity-badge ${finding.severity.toLowerCase()}`}>
                        {finding.severity}
                    </span>
                    {isAutomaticallyFixable && (
                        <span className="auto-fix-badge">🤖 Auto-Fixable</span>
                    )}
                </div>
            </div>

            <div className="remediation-details">
                <div className="original-text">
                    <strong>Original:</strong> {finding.source_text}
                </div>
                
                {finding.remediation && (
                    <div className="remediation-text">
                        <strong>Fixed:</strong> {finding.remediation}
                    </div>
                )}
                
                <div className="remediation-explanation">
                    <strong>Why:</strong> {finding.explanation}
                </div>
            </div>

            <div className="remediation-actions">
                {isAutomaticallyFixable && (
                    <div className="fix-status">
                        {ghostWriterMode ? (
                            <span className="fixed-indicator">✅ Automatically fixed</span>
                        ) : (
                            <span className="pending-fix">Enable Ghost-Writer to auto-fix</span>
                        )}
                    </div>
                )}
                
                {!isAutomaticallyFixable && (
                    <div className="manual-instructions">
                        <span>🔧 Manual fix required</span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Remediation;
