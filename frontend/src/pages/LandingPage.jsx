import React from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import { Globe, MessageSquare, Clock, ShieldCheck, Zap, BarChart2 } from 'lucide-react';
import './Landing.css';

const LandingPage = () => {
    const isLoggedIn = !!Cookies.get('session') || !!Cookies.get('user');

    return (
        <div className="landing-wrapper">
            <div className="bg-canvas">
                <div className="orb orb-1"></div>
                <div className="orb orb-2"></div>
            </div>

            <nav className="navbar">
                <Link to="/" className="brand" style={{ textDecoration: 'none' }}>
                    <div className="brand-mark">D</div>
                    <span className="brand-name">Pattern Detection</span>
                </Link>
                <div className="nav-links">
                    {isLoggedIn ? (
                        <>
                            <Link to="/dashboard" className="btn-auth btn-login">Dashboard</Link>
                            <Link to="/logout" className="btn-auth btn-signup">Logout</Link>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="btn-auth btn-login">Sign In</Link>
                            <Link to="/signup" className="btn-auth btn-signup">Join Now</Link>
                        </>
                    )}
                </div>
            </nav>

            <section className="hero">
                {isLoggedIn ? (
                    <div className="client-welcome-section fade-in">
                        <h1 className="hero-title">
                            Welcome back, <em>{Cookies.get('user') || 'User'}</em>
                        </h1>
                        <p className="hero-subtitle">
                            Your unified protection hub. Monitor history, verify links,
                            and analyze suspicious content with the Aegis detection engine.
                        </p>
                        <div className="hero-btns">
                            <Link to="/analyze" className="btn-auth btn-hero">Start Analysis</Link>
                            <Link to="/dashboard" className="btn-auth btn-login btn-outline-pill">View History</Link>
                        </div>

                        <div className="client-options-grid">
                            <div className="option-card">
                                <Globe size={28} className="option-icon" />
                                <h4>Domain Reputation</h4>
                                <p>Check if a domain is blacklisted or flagged by global security databases.</p>
                                <Link to="/analyze" className="option-link">Launch Scan</Link>
                            </div>
                            <div className="option-card">
                                <MessageSquare size={28} className="option-icon" />
                                <h4>NLP Pattern Check</h4>
                                <p>Our AI analyzes text for manipulative linguistic patterns used by scammers.</p>
                                <Link to="/analyze" className="option-link">Paste Text</Link>
                            </div>
                            <div className="option-card">
                                <Clock size={28} className="option-icon" />
                                <h4>Recent Archive</h4>
                                <p>Access your last security reports and verified safety statuses.</p>
                                <Link to="/dashboard" className="option-link">Open Logs</Link>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="guest-hero fade-in">
                        <h1 className="hero-title">
                            Detect Dark <em>Patterns</em><br />With Precision.
                        </h1>
                        <p className="hero-subtitle">
                            The most advanced AI-driven scanner for deceptive design.
                            Protect yourself from manipulative interfaces and data extraction.
                        </p>
                        <Link to="/login" className="btn-auth btn-hero">Start Security Scan</Link>

                        <div className="features-grid">
                            <div className="feature-card">
                                <ShieldCheck size={24} className="feature-icon" />
                                <h4>URL & Domain Analysis</h4>
                                <p>Cross-reference against 1M+ verified and blacklisted domains instantly.</p>
                            </div>
                            <div className="feature-card">
                                <Zap size={24} className="feature-icon" />
                                <h4>Real-time Detection</h4>
                                <p>AI-powered heuristics catch phishing, impersonation, and scam patterns.</p>
                            </div>
                            <div className="feature-card">
                                <BarChart2 size={24} className="feature-icon" />
                                <h4>Trust Score Engine</h4>
                                <p>Every scan produces a detailed trust score with evidence-backed findings.</p>
                            </div>
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
};

export default LandingPage;
