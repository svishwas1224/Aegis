import React from 'react';

const TrustScore = ({ score, riskLevel, status }) => {
    const getScoreColor = (score) => {
        if (score >= 75) return '#4caf50';
        if (score >= 45) return '#ff9800';
        return '#f44336';
    };

    const getRiskIcon = (riskLevel) => {
        const icons = {
            'SAFE': '🛡️',
            'CAUTION': '⚠️',
            'DANGER': '🚨'
        };
        return icons[riskLevel] || '❓';
    };

    const getScoreRotation = () => {
        return (score * 1.8) - 90; // Convert score to rotation angle
    };

    return (
        <div className="trust-score-container">
            <div className="score-gauge">
                <div className="gauge-circle">
                    <div 
                        className="gauge-fill"
                        style={{
                            background: `conic-gradient(${getScoreColor(score)} 0deg ${score * 3.6}deg, #e0e0e0 ${score * 3.6}deg 360deg)`
                        }}
                    ></div>
                    <div className="gauge-center">
                        <div className="score-number">{score}</div>
                        <div className="score-label">Trust Score</div>
                    </div>
                </div>
            </div>
            
            <div className="risk-indicator">
                <div className="risk-icon">{getRiskIcon(riskLevel)}</div>
                <div className="risk-text">
                    <div className="risk-level">{riskLevel}</div>
                    <div className="risk-status">{status}</div>
                </div>
            </div>
        </div>
    );
};

export default TrustScore;
