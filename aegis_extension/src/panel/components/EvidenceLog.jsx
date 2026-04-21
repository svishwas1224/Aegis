import React, { useState } from 'react';

const EvidenceLog = ({ findings }) => {
    const [expandedItems, setExpandedItems] = useState(new Set());
    const [filter, setFilter] = useState('all');
    const [severityFilter, setSeverityFilter] = useState('all');

    const toggleExpanded = (index) => {
        const newExpanded = new Set(expandedItems);
        if (newExpanded.has(index)) {
            newExpanded.delete(index);
        } else {
            newExpanded.add(index);
        }
        setExpandedItems(newExpanded);
    };

    const getEngineIcon = (engine) => {
        const icons = {
            'NLP': '📝',
            'VISUAL': '👁️',
            'BEHAVIORAL': '🔍'
        };
        return icons[engine] || '📋';
    };

    const getSeverityColor = (severity) => {
        const colors = {
            'HIGH': '#f44336',
            'MEDIUM': '#ff9800',
            'LOW': '#4caf50'
        };
        return colors[severity] || '#9e9e9e';
    };

    const filteredFindings = findings.filter(finding => {
        if (filter !== 'all' && finding.engine !== filter) return false;
        if (severityFilter !== 'all' && finding.severity !== severityFilter) return false;
        return true;
    });

    const getFindingsByType = () => {
        const grouped = {};
        filteredFindings.forEach(finding => {
            const type = finding.type;
            if (!grouped[type]) {
                grouped[type] = [];
            }
            grouped[type].push(finding);
        });
        return grouped;
    };

    const groupedFindings = getFindingsByType();

    return (
        <div className="evidence-log">
            <div className="evidence-header">
                <h3>Evidence Log</h3>
                <div className="evidence-filters">
                    <select 
                        value={filter} 
                        onChange={(e) => setFilter(e.target.value)}
                        className="filter-select"
                    >
                        <option value="all">All Engines</option>
                        <option value="NLP">NLP Engine</option>
                        <option value="VISUAL">Visual Engine</option>
                        <option value="BEHAVIORAL">Behavioral Engine</option>
                    </select>
                    
                    <select 
                        value={severityFilter} 
                        onChange={(e) => setSeverityFilter(e.target.value)}
                        className="filter-select"
                    >
                        <option value="all">All Severities</option>
                        <option value="HIGH">High Severity</option>
                        <option value="MEDIUM">Medium Severity</option>
                        <option value="LOW">Low Severity</option>
                    </select>
                </div>
            </div>

            <div className="evidence-stats">
                <div className="stat-item">
                    <span className="stat-number">{filteredFindings.length}</span>
                    <span className="stat-label">Total Findings</span>
                </div>
                <div className="stat-item">
                    <span className="stat-number">{Object.keys(groupedFindings).length}</span>
                    <span className="stat-label">Pattern Types</span>
                </div>
            </div>

            <div className="evidence-content">
                {Object.entries(groupedFindings).map(([type, typeFindings]) => (
                    <div key={type} className="pattern-group">
                        <div className="pattern-group-header">
                            <h4>{type.replace('_', ' ').toUpperCase()}</h4>
                            <span className="pattern-count">{typeFindings.length}</span>
                        </div>
                        
                        {typeFindings.map((finding, index) => {
                            const globalIndex = findings.indexOf(finding);
                            const isExpanded = expandedItems.has(globalIndex);
                            
                            return (
                                <div key={globalIndex} className="evidence-item">
                                    <div 
                                        className="evidence-item-header"
                                        onClick={() => toggleExpanded(globalIndex)}
                                    >
                                        <div className="evidence-meta">
                                            <span className="engine-icon">
                                                {getEngineIcon(finding.engine)}
                                            </span>
                                            <span className="finding-type">{finding.type}</span>
                                            <span 
                                                className="severity-badge"
                                                style={{ backgroundColor: getSeverityColor(finding.severity) }}
                                            >
                                                {finding.severity}
                                            </span>
                                        </div>
                                        <button className="expand-btn">
                                            {isExpanded ? '▼' : '▶'}
                                        </button>
                                    </div>
                                    
                                    {isExpanded && (
                                        <div className="evidence-details">
                                            <div className="evidence-source">
                                                <strong>Source:</strong> {finding.source_text || 'N/A'}
                                            </div>
                                            
                                            <div className="evidence-explanation">
                                                <strong>Explanation:</strong> {finding.explanation}
                                            </div>
                                            
                                            <div className="evidence-remediation">
                                                <strong>Remediation:</strong> {finding.remediation}
                                            </div>
                                            
                                            {finding.evidence && (
                                                <div className="evidence-technical">
                                                    <strong>Technical Details:</strong>
                                                    <pre>{JSON.stringify(finding.evidence, null, 2)}</pre>
                                                </div>
                                            )}
                                            
                                            {finding.bbox && (
                                                <div className="evidence-bbox">
                                                    <strong>Location:</strong> 
                                                    X: {finding.bbox[0]}, Y: {finding.bbox[1]}, 
                                                    W: {finding.bbox[2]}, H: {finding.bbox[3]}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                ))}
                
                {filteredFindings.length === 0 && (
                    <div className="no-evidence">
                        <p>No findings match the current filters.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EvidenceLog;
