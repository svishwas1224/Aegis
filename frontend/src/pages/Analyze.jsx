import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import API_BASE_URL from '../config';
import { ShieldCheck, ShieldAlert, Info, Search, RefreshCw, ArrowLeft, Activity, Target, Zap, LayoutGrid } from 'lucide-react';
import './Analyze.css';

const Analyze = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [input, setInput] = useState('');
    const [inputType, setInputType] = useState('url');
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [isRealTimeAnalyzing, setIsRealTimeAnalyzing] = useState(false);
    const [result, setResult] = useState(null);
    const debounceTimer = useRef(null);
    const realTimeAbortController = useRef(null);

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const mode = params.get('mode');
        const url = params.get('url');
        if (mode === 'text') setInputType('text');
        else if (mode === 'url') setInputType('url');
        if (url) {
            setInput(url);
        }
    }, [location]);

    const realTimeAnalyze = useCallback(async (value) => {
        if (!value || !value.trim()) {
            setIsRealTimeAnalyzing(false);
            return;
        }

        // Cancel previous request if it exists
        if (realTimeAbortController.current) {
            realTimeAbortController.current.abort();
        }

        setIsRealTimeAnalyzing(true);
        const abortController = new AbortController();
        realTimeAbortController.current = abortController;

        try {
            const cleanInput = value.trim();
            const endpoint = inputType === 'url' ? '/analyze' : '/analyze-text';
            const payload = inputType === 'url' ? { url: cleanInput } : { text: cleanInput };

            const res = await axios.post(`${API_BASE_URL}${endpoint}?t=${Date.now()}`, payload, {
                signal: abortController.signal,
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
            });

            setResult(res.data);
        } catch (err) {
            if (!axios.isCancel(err)) {
                // Real-time analysis failed; preserve current state.
            }
        } finally {
            setIsRealTimeAnalyzing(false);
        }
    }, [inputType]);

    const handleInputChange = (e) => {
        const newInput = e.target.value;
        setInput(newInput);

        // Cancel any pending real-time analysis timer
        if (debounceTimer.current) {
            clearTimeout(debounceTimer.current);
        }

        // Only do real-time analysis for text inputs.
        // URL scans should run only when the user explicitly clicks the button.
        if (inputType === 'text' && newInput.trim().length > 3) {
            debounceTimer.current = setTimeout(() => {
                realTimeAnalyze(newInput);
            }, 500); // 500ms debounce
        }
    };

    const handleAnalyze = async () => {
        if (!input || !input.trim()) return;
        setIsAnalyzing(true);
        setResult(null);

        const cleanInput = input.trim();
        const abortController = new AbortController();

        try {
            const endpoint = inputType === 'url' ? '/analyze' : '/analyze-text';
            const payload = inputType === 'url' ? { url: cleanInput } : { text: cleanInput };

            const res = await axios.post(`${API_BASE_URL}${endpoint}?t=${Date.now()}`, payload, {
                signal: abortController.signal,
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
            });

            // "Cinematic" delay for improved UX
            setTimeout(() => {
                setResult(res.data);
                setIsAnalyzing(false);
            }, 1800);
        } catch (err) {
            if (axios.isCancel(err)) return;
            setIsAnalyzing(false);
            setResult({ success: false, error: "Connection interrupted. Please check your secure link." });
        }
    };

    const trySample = () => {
        const samples = {
            url: "https://amazon-security-alert.net/login",
            text: "Final Warning! Your account will be permanently deactivated in 5 minutes unless you verify your identity now. Click here to prevent immediate loss of data!"
        };
        setInput(samples[inputType]);
    };

    const getStatusInfo = (status) => {
        if (status === 'SAFE') return { label: 'Safe', color: '#00ff9d', desc: 'This content appears safe and trustworthy.', recommend: 'You can proceed normally.' };
        if (status === 'SUSPICIOUS') return { label: 'Suspicious', color: '#ffcc00', desc: 'Some elements may be misleading or manipulative.', recommend: 'Proceed with caution.' };
        return { label: 'High Risk', color: '#ff4d4d', desc: 'This content contains strong deceptive patterns.', recommend: 'Avoid interacting with this content.' };
    };

    // Only findings that are actual problems — filter out informational/positive ones and bot traps
    const normalizeFindingText = (finding) => {
        if (!finding) return '';
        if (typeof finding === 'string') return finding;
        return finding.type || finding.category || finding.explanation || JSON.stringify(finding);
    };

    const getProblemFindings = (findings = []) => {
        const infoPatterns = [
            /^site responded with http 2/i,
            /^valid ssl/i,
            /^page title:/i,
            /^page title matches/i,
            /^site has standard trust markers/i,
            /^domain is the official/i,
            /^domain matched/i,
            /^network check/i,
            /^site uses redirects/i,
            /^live verification passed/i,
            /^domain is a verified/i,
        ];
        const botTrapPatterns = [
            /honeypot/i,
            /infinite loop/i,
            /bot trap/i,
        ];
        // Keep findings that are either not in infoPatterns or botTrapPatterns, or are clearly dark patterns
        const filtered = findings.filter(f => {
            const text = normalizeFindingText(f);
            const isInfo = infoPatterns.some(p => p.test(text));
            const isBotTrap = botTrapPatterns.some(p => p.test(text));
            const isDarkPattern = /urgency|scarcity|social proof|misdirection|forced action|cookie wall|subscription trap|false free trial|confirm shaming|hidden cost|bait and switch|trick question|pre selected|disguised ad|hard to cancel|privacy zuckering|sneaking|obstruction|general dark pattern/i.test(text);
            return (!isInfo && !isBotTrap) || isDarkPattern;
        });

        return filtered;
    };

    return (
        <div className={`analyze-portal-wrapper ${isAnalyzing ? 'is-scanning' : ''}`}>
            {/* Advanced Background Nexus */}
            <div className="background-nexus">
                <div className="nexus-base-gradient"></div>
                <div className="nexus-grid"></div>
                <div className="nexus-noise"></div>
                <div className="nexus-blobs">
                    <div className="blob blob-cyan"></div>
                    <div className="blob blob-purple"></div>
                    <div className="blob blob-teal"></div>
                </div>
            </div>

            <nav className="analyze-nav fade-in">
                <div className="nav-left">
                    <Link to="/dashboard" className="nav-logo">
                        <div className="logo-box">D</div>
                        <div className="logo-text">
                            <span className="logo-main">Dark Pattern Detection</span>
                            <span className="logo-sub">SECURE CONSOLE</span>
                        </div>
                    </Link>
                </div>
                <div className="nav-right">
                    <button className="nav-action-btn" onClick={() => navigate('/dashboard')}>
                        <LayoutGrid size={16} /> DASHBOARD
                    </button>
                </div>
            </nav>

            <main className="analyze-main">
                {!result && !isAnalyzing && (
                    <div className="analyze-hero fade-in">
                        <div className="hero-badge">
                            <Zap size={14} className="flash-icon" /> PATTERN DETECTION ENGINE
                        </div>
                        <h1>Dark Pattern Detection Console</h1>
                        <p>Advanced pattern analysis for deceptive design and manipulative content</p>
                    </div>
                )}

                {!result && (
                    <div className="glass-card analyzer-card stagger-1">
                        <div className="card-tabs">
                            <button 
                                className={`tab-btn ${inputType === 'url' ? 'active' : ''}`}
                                onClick={() => setInputType('url')}
                                disabled={isAnalyzing}
                            >
                                <Target size={18} /> URL Analysis
                            </button>
                            <button 
                                className={`tab-btn ${inputType === 'text' ? 'active' : ''}`}
                                onClick={() => setInputType('text')}
                                disabled={isAnalyzing}
                            >
                                <Activity size={18} /> Text Audit
                            </button>
                        </div>

                        <div className="analyzer-input-box">
                            <div className="input-header">
                                <h4>Input to Analyze</h4>
                                {isRealTimeAnalyzing && (
                                    <div className="real-time-indicator">
                                        <RefreshCw className="spin-icon" size={14} />
                                        <span>Analyzing in real-time...</span>
                                    </div>
                                )}
                            </div>
                            <textarea 
                                placeholder={inputType === 'url' ? "Enter website URL to scan..." : "Paste suspicious content or promotional text here..."}
                                value={input}
                                onChange={handleInputChange}
                                disabled={isAnalyzing}
                                className="styled-textarea"
                            />
                            
                            <div className="card-actions">
                                <div className="action-left">
                                    <button className="btn-secondary" onClick={() => setInput('')} disabled={isAnalyzing}>Clear</button>
                                    <button className="btn-secondary" onClick={trySample} disabled={isAnalyzing}>Try Sample</button>
                                </div>
                                <button 
                                    className={`btn-primary ${isAnalyzing ? 'loading' : ''}`} 
                                    onClick={handleAnalyze} 
                                    disabled={isAnalyzing || !input.trim()}
                                >
                                    {isAnalyzing ? <RefreshCw className="spin-icon" /> : <Search size={20} />}
                                    {isAnalyzing ? "Analyzing Patterns..." : "Launch Deep Analysis"}
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {isAnalyzing && (
                    <div className="scanning-ui fade-in">
                        <div className="neural-rings">
                            <div className="ring"></div>
                            <div className="ring delay-1"></div>
                            <div className="ring delay-2"></div>
                        </div>
                        <h3>Security Pipeline Active</h3>
                        <p>Scanning for manipulation markers...</p>
                    </div>
                )}

                {result && !isAnalyzing && (
                    <div className="result-view fade-in">
                        {/* Show warning banner if any dark patterns are found, even on safe sites */}
                        {getProblemFindings(result.findings).length > 0 && (
                            <div className="dark-pattern-warning">
                                <ShieldAlert size={24} />
                                <div className="warning-content">
                                    <h3>⚠️ Dark Patterns Detected!</h3>
                                    <p>This site uses {getProblemFindings(result.findings).length} manipulative design pattern(s) that may influence your decisions without your knowledge.</p>
                                </div>
                            </div>
                        )}

                        <div className="result-grid">
                            <div className="glass-card result-summary-card">
                                <div className="summary-header">
                                    <div className="status-indicator">
                                        <div className="status-label">SECURITY STATUS</div>
                                        <h2 style={{ color: getStatusInfo(result.status).color }}>
                                            {getStatusInfo(result.status).label}
                                        </h2>
                                    </div>
                                    <div className="trust-gauge">
                                        <svg viewBox="0 0 100 100" className="gauge-svg">
                                            <circle className="gauge-bg" cx="50" cy="50" r="45" />
                                            <circle
                                                className="gauge-fill"
                                                cx="50" cy="50" r="45"
                                                style={{
                                                    strokeDasharray: `${result.trust_score * 2.82} 282`,
                                                    stroke: getStatusInfo(result.status).color
                                                }}
                                            />
                                        </svg>
                                        <div className="gauge-text">
                                            <span className="gauge-val">{result.trust_score}%</span>
                                            <label>TRUST</label>
                                        </div>
                                    </div>
                                </div>
                                <p className="status-message">{result.message}</p>
                            </div>

                            <div className="glass-card explanation-card">
                                <h3>Verdict</h3>
                                <p className="insight-text">
                                    {result.status === 'SAFE'
                                        ? "This site passed live verification. It has a valid SSL certificate, responds correctly, and shows no signs of impersonation or fraud."
                                        : result.status === 'SUSPICIOUS'
                                        ? "This site could not be fully verified. It may be new, misconfigured, or potentially deceptive. Avoid entering personal information."
                                        : "This site failed verification checks. It may be a phishing page, typosquat, or known malicious domain. Do not interact with it."}
                                </p>
                                <div className="recommendation-pill" style={{ background: `${getStatusInfo(result.status).color}15`, color: getStatusInfo(result.status).color }}>
                                    {getStatusInfo(result.status).recommend}
                                </div>
                            </div>
                        </div>

                        {/* Show findings section when there are any problems */}
                        {getProblemFindings(result.findings).length > 0 && (
                            <div className="patterns-section">
                                <h3 className="section-title">Dark Patterns Identified</h3>
                                <div className="patterns-grid">
                                    {getProblemFindings(result.findings).map((f, i) => {
                                        const text = normalizeFindingText(f);
                                        const isHighSeverity = f && f.severity === 'HIGH';
                                        return (
                                            <div key={i} className={`glass-card pattern-element-card ${isHighSeverity ? 'high-severity' : ''}`}>
                                                <div className="pattern-header">
                                                    <ShieldAlert size={18} className={isHighSeverity ? 'text-danger' : 'text-warning'} />
                                                    <h4>{text}</h4>
                                                </div>
                                                {f && f.explanation && (
                                                    <p className="pattern-explanation">{f.explanation}</p>
                                                )}
                                                {f && f.evidence && (
                                                    <div className="evidence-box">
                                                        <label>EVIDENCE</label>
                                                        <code>{typeof f.evidence === 'string' ? f.evidence : JSON.stringify(f.evidence)}</code>
                                                    </div>
                                                )}
                                                {f && f.remediation && (
                                                    <div className="remediation-box">
                                                        <label>SUGGESTION</label>
                                                        <p>{f.remediation}</p>
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        <div className="result-nav-actions">
                            <button className="btn-secondary-large" onClick={() => setResult(null)}>
                                <RefreshCw size={18} /> Scan Another
                            </button>
                            <button className="btn-secondary-large" onClick={() => navigate('/dashboard?view=history')}>
                                <Activity size={18} /> View History
                            </button>
                            <button className="btn-primary-large" onClick={() => navigate('/dashboard')}>
                                <ArrowLeft size={18} /> Back to Dashboard
                            </button>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default Analyze;
