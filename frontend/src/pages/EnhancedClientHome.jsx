import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import API_BASE_URL from '../config';
import Cookies from 'js-cookie';
import { 
    Shield, 
    Search, 
    History, 
    User, 
    LogOut, 
    AlertTriangle, 
    CheckCircle2, 
    Globe, 
    TrendingUp,
    ShieldCheck,
    Activity,
    Settings,
    Bell,
    HelpCircle,
    ChevronRight,
    Target,
    Download,
    Share2,
    Filter,
    TrendingDown
} from 'lucide-react';
import './EnhancedClientHome.css';

const EnhancedClientHome = () => {
    const [user, setUser] = useState(Cookies.get('user') || 'Guest');
    const [history, setHistory] = useState([]);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [stats, setStats] = useState({
        totalScans: 0,
        threatsDetected: 0,
        trustScore: 0,
        riskLevel: 'Calculating...',
        weeklyScans: 0,
        monthlyScans: 0,
        avgScanTime: 0,
        topPatterns: [],
        recentActivity: []
    });
    const [isLoading, setIsLoading] = useState(true);
    const [isStatsLoading, setIsStatsLoading] = useState(false);
    const [selectedTimeRange, setSelectedTimeRange] = useState('week');
    const [filteredHistory, setFilteredHistory] = useState([]);
    const [selectedScan, setSelectedScan] = useState(null);
    const [expandedPatterns, setExpandedPatterns] = useState(new Set());
    const location = useLocation();
    const [notifications, setNotifications] = useState([]);
    const [showNotifications, setShowNotifications] = useState(false);
    const [showUserMenu, setShowUserMenu] = useState(false);

    useEffect(() => {
        document.title = 'Dark Pattern Detection - Security Dashboard';
        fetchData();
    }, []);

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const view = params.get('view');
        setActiveTab(view === 'history' ? 'history' : 'dashboard');
    }, [location.search]);

    // Filter history based on time range
    useEffect(() => {
        console.log("Time range updated:", selectedTimeRange);
        setIsStatsLoading(true);
        
        // Simulate a small delay for loading effect
        setTimeout(() => {
            const now = new Date();
            let filterDate;
        
        switch(selectedTimeRange) {
            case 'day':
                filterDate = new Date(now.getTime() - 24 * 60 * 60 * 1000);
                break;
            case 'week':
                filterDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                break;
            case 'month':
                filterDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                break;
            default:
                filterDate = new Date(0); // All time
        }
        
        const filtered = history.filter(item => new Date(item.timestamp) > filterDate);
        console.log("Filtered history:", filtered);
        setFilteredHistory(filtered);
        
        // Recalculate stats for filtered history
        if (filtered.length > 0) {
            const threats = filtered.filter(item => 
                item.safety_status && item.safety_status.toLowerCase() === 'unsafe'
            ).length;
            
            const avgTrust = Math.round(filtered.reduce((acc, curr) => acc + (curr.trust_score || 0), 0) / filtered.length);
            
            const patternCounts = {};
            filtered.forEach(item => {
                if (item.findings) {
                    item.findings.forEach(finding => {
                        patternCounts[finding.type] = (patternCounts[finding.type] || 0) + 1;
                    });
                }
            });
            
            const topPatterns = Object.entries(patternCounts)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 5)
                .map(([pattern, count]) => ({ pattern, count }));
                
            const recentActivity = filtered.slice(0, 5).map(item => ({
                url: item.url,
                timestamp: item.timestamp,
                trustScore: item.trust_score,
                status: item.safety_status
            }));
                
            setStats(prev => ({
                ...prev,
                totalScans: filtered.length,
                threatsDetected: threats,
                trustScore: avgTrust,
                topPatterns,
                recentActivity
            }));
            console.log("Updated stats:", { totalScans: filtered.length, threats, avgTrust, topPatterns, recentActivity });
        }
        
        setIsStatsLoading(false);
        }, 300);
    }, [history, selectedTimeRange]);

    const togglePatternExpansion = (patternIndex) => {
        console.log("Toggling pattern expansion:", patternIndex);
        const newExpanded = new Set(expandedPatterns);
        if (newExpanded.has(patternIndex)) {
            newExpanded.delete(patternIndex);
        } else {
            newExpanded.add(patternIndex);
        }
        console.log("New expanded patterns:", newExpanded);
        setExpandedPatterns(newExpanded);
    };

    const handleSelectScan = (scan) => {
        console.log("Selecting scan:", scan);
        setSelectedScan(selectedScan?._id === scan._id ? null : scan);
    };

    const exportReport = () => {
        console.log("Exporting report...");
        const reportData = {
            user,
            timestamp: new Date().toISOString(),
            stats,
            history: filteredHistory
        };
        
        console.log("Report data:", reportData);
        
        const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `security-report-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        // Show success notification
        setNotifications(prev => [...prev, {
            type: 'success',
            message: 'Report exported successfully!',
            timestamp: new Date()
        }]);
        console.log("Report exported successfully!");
    };

    const shareResult = async (scan) => {
        console.log("Sharing scan result:", scan);
        const shareData = {
            title: `Dark Pattern Scan for ${scan.url}`,
            text: `Trust Score: ${scan.trust_score}% | Status: ${scan.safety_status}`,
            url: scan.url
        };
        
        console.log("Share data:", shareData);
        
        if (navigator.share) {
            try {
                await navigator.share(shareData);
                console.log("Share successful!");
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.log("Share failed, copying to clipboard...", err);
                    alert('Share failed, copying to clipboard instead...');
                    await navigator.clipboard.writeText(JSON.stringify(shareData));
                }
            }
        } else {
            await navigator.clipboard.writeText(JSON.stringify(shareData));
            alert('Scan data copied to clipboard!');
            console.log("Copied to clipboard!");
        }
    };

    const fetchData = async () => {
        try {
            const res = await axios.get(`${API_BASE_URL}/dashboard`);
            setUser(res.data.user);
            const hData = res.data.history || [];
            setHistory(hData);
            
            // Enhanced Stats Calculation
            const threats = hData.filter(item => 
                item.safety_status && item.safety_status.toLowerCase() === 'unsafe'
            ).length;
            
            const avgTrust = hData.length > 0 
                ? Math.round(hData.reduce((acc, curr) => acc + (curr.trust_score || 0), 0) / hData.length)
                : 100;

            let risk = 'Low';
            if (avgTrust < 50) risk = 'High';
            else if (avgTrust < 80) risk = 'Medium';

            // Calculate weekly and monthly scans
            const now = new Date();
            const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
            
            const weeklyScans = hData.filter(item => new Date(item.timestamp) > weekAgo).length;
            const monthlyScans = hData.filter(item => new Date(item.timestamp) > monthAgo).length;

            // Extract top patterns
            const patternCounts = {};
            hData.forEach(item => {
                if (item.findings) {
                    item.findings.forEach(finding => {
                        patternCounts[finding.type] = (patternCounts[finding.type] || 0) + 1;
                    });
                }
            });
            
            const topPatterns = Object.entries(patternCounts)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 5)
                .map(([pattern, count]) => ({ pattern, count }));

            // Recent activity
            const recentActivity = hData.slice(0, 5).map(item => ({
                url: item.url,
                timestamp: item.timestamp,
                trustScore: item.trust_score,
                status: item.safety_status
            }));

            setStats({
                totalScans: hData.length,
                threatsDetected: threats,
                trustScore: avgTrust,
                riskLevel: hData.length > 0 ? risk : 'Low',
                weeklyScans,
                monthlyScans,
                avgScanTime: 2.3, // Simulated
                topPatterns,
                recentActivity
            });

            // Generate notifications
            const notifications = [];
            if (threats > 0) {
                notifications.push({
                    type: 'warning',
                    message: `${threats} threats detected in recent scans`,
                    timestamp: new Date()
                });
            }
            if (weeklyScans > 10) {
                notifications.push({
                    type: 'success',
                    message: 'Great job! You\'ve been very active this week',
                    timestamp: new Date()
                });
            }
            setNotifications(notifications);

        } catch {
            Cookies.remove('user');
            window.location.href = '/login';
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await axios.get(`${API_BASE_URL}/logout`);
            Cookies.remove('user');
            window.location.href = '/login';
        } catch {
            Cookies.remove('user');
            window.location.href = '/login';
        }
    };

    const getRiskColor = (level) => {
        switch (level.toLowerCase()) {
            case 'high': return '#ef4444';
            case 'medium': return '#f59e0b';
            case 'low': return '#10b981';
            default: return '#6b7280';
        }
    };

    const getRiskIcon = (level) => {
        switch (level.toLowerCase()) {
            case 'high': return AlertTriangle;
            case 'medium': return Shield;
            case 'low': return CheckCircle2;
            default: return Activity;
        }
    };

    if (isLoading) {
        return (
            <div className="enhanced-loading">
                <div className="loading-container">
                    <div className="loading-shield">
                        <Shield className="loading-icon" size={48} />
                        <div className="loading-pulse"></div>
                    </div>
                    <div className="loading-text">
                        <h2>Initializing Dark Pattern Detection</h2>
                        <p>Securing your digital experience...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="enhanced-client-home">
            {/* Enhanced Header */}
            <header className="enhanced-header">
                <div className="header-container">
                    <div className="header-left">
                        <Link to="/" className="brand-logo">
                            <div className="logo-shield">
                                <Shield size={32} />
                                <div className="logo-pulse"></div>
                            </div>
                            <div className="brand-text">
                                <span className="brand-name">Dark Pattern Detection</span>
                                <span className="brand-tagline">Console</span>
                            </div>
                        </Link>
                    </div>
                    
                    <nav className="header-nav">
                        <Link to="/dashboard" className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}>Dashboard</Link>
                        <Link to="/analyze" className="nav-link">Scan</Link>
                        <Link to="/dashboard?view=history" className={`nav-link ${activeTab === 'history' ? 'active' : ''}`}>History</Link>
                    </nav>

                    <div className="header-right">
                        {/* Notifications */}
                        <div className="notification-wrapper">
                            <button 
                                className="notification-btn"
                                onClick={() => setShowNotifications(!showNotifications)}
                            >
                                <Bell size={20} />
                                {notifications.length > 0 && (
                                    <span className="notification-badge">{notifications.length}</span>
                                )}
                            </button>
                            
                            {showNotifications && (
                                <div className="notification-dropdown">
                                    <div className="notification-header">
                                        <h4>Notifications</h4>
                                        <button onClick={() => setNotifications([])}>
                                            Clear all
                                        </button>
                                    </div>
                                    <div className="notification-list">
                                        {notifications.map((notif, index) => (
                                            <div key={index} className={`notification-item ${notif.type}`}>
                                                <div className="notification-icon">
                                                    {notif.type === 'warning' ? <AlertTriangle size={16} /> : <CheckCircle2 size={16} />}
                                                </div>
                                                <div className="notification-content">
                                                    <p>{notif.message}</p>
                                                    <span className="notification-time">
                                                        {new Date(notif.timestamp).toLocaleTimeString()}
                                                    </span>
                                                </div>
                                            </div>
                                        ))}
                                        {notifications.length === 0 && (
                                            <div className="no-notifications">
                                                <p>No new notifications</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* User Menu */}
                        <div className="user-menu-wrapper">
                            <button 
                                type="button"
                                className={`user-menu-btn ${showUserMenu ? 'open' : ''}`}
                                onClick={() => setShowUserMenu(!showUserMenu)}
                            >
                                <div className="user-avatar">
                                    <User size={20} />
                                </div>
                                <span className="user-name">{user}</span>
                                <ChevronRight size={16} className="chevron" />
                            </button>
                            
                            {showUserMenu && (
                                <div className="user-dropdown">
                                    <Link to="/settings" className="dropdown-item">
                                        <Settings size={16} />
                                        Settings
                                    </Link>
                                    <Link to="/help" className="dropdown-item">
                                        <HelpCircle size={16} />
                                        Help & Support
                                    </Link>
                                    <button onClick={handleLogout} className="dropdown-item logout">
                                        <LogOut size={16} />
                                        Logout
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            <main className="enhanced-main">
                {/* Welcome Section */}
                <section className="welcome-section">
                    <div className="welcome-content">
                        <h1>Welcome back, <span className="user-highlight">{user}</span></h1>
                        <p className="welcome-subtitle">
                            Your digital security dashboard with real-time threat detection and analysis
                        </p>
                        
                        <div className="welcome-actions">
                            <Link to="/analyze" className="primary-btn">
                                <Target size={20} />
                                Start New Scan
                            </Link>
                            <button type="button" className="secondary-btn" onClick={exportReport}>
                                <Download size={20} />
                                Export Report
                            </button>
                        </div>
                    </div>
                    
                    <div className="welcome-visual">
                        <div className="security-ring">
                            <Shield className="center-icon" size={64} />
                            <div className="ring-animation"></div>
                        </div>
                    </div>
                </section>

                <section className="insight-banner">
                    <div className="banner-left">
                        <p className="banner-label">Security pulse</p>
                        <h2>
                            {stats.threatsDetected > 0 ? `${stats.threatsDetected} threats detected` : 'All systems are secure'}
                        </h2>
                        <p className="banner-copy">
                            Your average trust score is <strong>{stats.trustScore}%</strong> and current risk is <strong>{stats.riskLevel}</strong>. Keep scanning regularly to maintain protection.
                        </p>
                    </div>
                    <div className="banner-right">
                        <div className="banner-pill">
                            <span>Trust score</span>
                            <strong>{stats.trustScore}%</strong>
                        </div>
                        <div className="banner-pill status">
                            <span>Risk level</span>
                            <strong>{stats.riskLevel}</strong>
                        </div>
                    </div>
                </section>

                {activeTab === 'history' ? (
                    <section className="history-section">
                        <div className="card-header">
                            <h2>Scan History</h2>
                            <Link to="/dashboard" className="view-all">
                                Back to dashboard
                            </Link>
                        </div>
                        {filteredHistory.length > 0 ? (
                            <div className="history-table">
                                <div className="history-row history-row-head">
                                    <span>URL</span>
                                    <span>Status</span>
                                    <span>Trust</span>
                                    <span>Timestamp</span>
                                    <span>Actions</span>
                                </div>
                                {filteredHistory.map((item, index) => (
                                    <div key={item._id || index} className="history-item-wrapper">
                                        <div 
                                            className={`history-row ${selectedScan?._id === item._id ? 'expanded' : ''}`}
                                            onClick={() => {
                                                console.log("History row clicked:", item);
                                                handleSelectScan(item);
                                            }}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <span className="history-url">{item.url || 'N/A'}</span>
                                            <span>
                                                <span className={`status-pill ${item.safety_status ? item.safety_status.toLowerCase() : 'unknown'}`}>
                                                    {item.safety_status || 'Unknown'}
                                                </span>
                                            </span>
                                            <span>{item.trust_score != null ? `${item.trust_score}%` : '—'}</span>
                                            <span>{item.timestamp ? new Date(item.timestamp).toLocaleString() : 'N/A'}</span>
                                            <span>
                                                <button 
                                                    type="button"
                                                    onClick={(e) => { e.stopPropagation(); shareResult(item); }}
                                                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '4px 8px', color: '#60a5fa' }}
                                                >
                                                    <Share2 size={16} />
                                                </button>
                                            </span>
                                        </div>
                                        <div className={`scan-details ${selectedScan?._id === item._id ? 'visible' : ''}`} style={{
                                            background: '#1e293b',
                                            borderLeft: '4px solid #3b82f6',
                                            borderRadius: '0 8px 8px 0',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{ padding: '16px' }}>
                                                <h4 style={{ margin: '0 0 12px' }}>Scan Details</h4>
                                                <p style={{ margin: '8px 0' }}><strong>URL:</strong> {item.url}</p>
                                                <p style={{ margin: '8px 0' }}><strong>Trust Score:</strong> {item.trust_score}%</p>
                                                <p style={{ margin: '8px 0' }}><strong>Status:</strong> {item.safety_status}</p>
                                                {item.findings && item.findings.length > 0 && (
                                                    <div style={{ marginTop: '12px' }}>
                                                        <strong>Findings:</strong>
                                                        <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                                                            {item.findings.map((finding, fIndex) => (
                                                                <li key={fIndex} style={{ margin: '4px 0' }}>
                                                                    {finding.type || finding} - {finding.explanation || ''}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}
                                                <Link 
                                                    to={`/analyze?url=${encodeURIComponent(item.url)}`}
                                                    style={{
                                                        display: 'inline-block',
                                                        marginTop: '12px',
                                                        color: '#60a5fa',
                                                        textDecoration: 'none'
                                                    }}
                                                >
                                                    Re-scan this URL →
                                                </Link>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="no-activity">
                                <p>No scan history available yet.</p>
                                <p className="no-activity-subtitle">Start a new scan to populate your history and capture suspicious content immediately.</p>
                            </div>
                        )}
                    </section>
                ) : (
                    <>
                        {/* Stats Overview */}
                        <section className="stats-overview">
                            <div className="stats-header">
                                <h2>Security Overview</h2>
                                <div className="time-range-selector">
                                    <button 
                                        className={`range-btn ${selectedTimeRange === 'day' ? 'active' : ''}`}
                                        onClick={() => setSelectedTimeRange('day')}
                                    >
                                        Day
                                    </button>
                                    <button 
                                        className={`range-btn ${selectedTimeRange === 'week' ? 'active' : ''}`}
                                        onClick={() => setSelectedTimeRange('week')}
                                    >
                                        Week
                                    </button>
                                    <button 
                                        className={`range-btn ${selectedTimeRange === 'month' ? 'active' : ''}`}
                                        onClick={() => setSelectedTimeRange('month')}
                                    >
                                        Month
                                    </button>
                                </div>
                            </div>

                            <div className="stats-grid" style={{ position: 'relative' }}>
                                {isStatsLoading && (
                                    <div style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: 0,
                                        right: 0,
                                        bottom: 0,
                                        background: 'rgba(15,23,42,0.8)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        zIndex: 10,
                                        borderRadius: '16px'
                                    }}>
                                        <div style={{
                                            width: '30px',
                                            height: '30px',
                                            border: '3px solid rgba(59,130,246,0.2)',
                                            borderTopColor: '#3b82f6',
                                            borderRadius: '50%',
                                            animation: 'spin 0.8s linear infinite'
                                        }}></div>
                                    </div>
                                )}
                                <div className="stat-card primary">
                                    <div className="stat-header">
                                        <div className="stat-icon">
                                            <Search size={24} />
                                        </div>
                                        <div className="stat-trend">
                                            <TrendingUp size={16} />
                                            <span>+12%</span>
                                        </div>
                                    </div>
                                    <div className="stat-content">
                                        <h3>{stats.totalScans}</h3>
                                        <p>Total Scans</p>
                                    </div>
                                </div>

                                <div className="stat-card danger">
                                    <div className="stat-header">
                                        <div className="stat-icon">
                                            <AlertTriangle size={24} />
                                        </div>
                                        <div className="stat-trend">
                                            <TrendingDown size={16} />
                                            <span>-5%</span>
                                        </div>
                                    </div>
                                    <div className="stat-content">
                                        <h3>{stats.threatsDetected}</h3>
                                        <p>Threats Detected</p>
                                    </div>
                                </div>

                                <div className="stat-card success">
                                    <div className="stat-header">
                                        <div className="stat-icon">
                                            <ShieldCheck size={24} />
                                        </div>
                                        <div className="stat-trend">
                                            <TrendingUp size={16} />
                                            <span>+8%</span>
                                        </div>
                                    </div>
                                    <div className="stat-content">
                                        <h3>{stats.trustScore}%</h3>
                                        <p>Average Trust Score</p>
                                    </div>
                                </div>

                                <div className="stat-card warning">
                                    <div className="stat-header">
                                        <div className="stat-icon">
                                            {React.createElement(getRiskIcon(stats.riskLevel), { size: 24 })}
                                        </div>
                                        <div className="stat-trend">
                                            <Activity size={16} />
                                            <span>Stable</span>
                                        </div>
                                    </div>
                                    <div className="stat-content">
                                        <h3 style={{ color: getRiskColor(stats.riskLevel) }}>
                                            {stats.riskLevel}
                                        </h3>
                                        <p>Risk Level</p>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Activity & Patterns */}
                        <section className="activity-section">
                            <div className="activity-grid">
                                {/* Recent Activity */}
                                <div className="activity-card">
                                    <div className="card-header">
                                        <h3>Recent Activity</h3>
                                        <Link to="/dashboard?view=history" className="view-all">
                                            View all
                                        </Link>
                                    </div>
                                    <div className="activity-list">
                                        {stats.recentActivity.map((activity, index) => {
                                            const fullScan = history.find(h => h.url === activity.url && h.timestamp === activity.timestamp);
                                            return (
                                                <div 
                                                    key={index} 
                                                    className="activity-item"
                                                    onClick={() => fullScan && handleSelectScan(fullScan)}
                                                    style={{ cursor: 'pointer' }}
                                                >
                                                    <div className="activity-icon">
                                                        <Globe size={16} />
                                                    </div>
                                                    <div className="activity-details">
                                                        <p className="activity-url">{activity.url}</p>
                                                        <div className="activity-meta">
                                                            <span className="activity-score">
                                                                Trust: {activity.trustScore}%
                                                            </span>
                                                            <span className="activity-time">
                                                                {new Date(activity.timestamp).toLocaleTimeString()}
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div className={`activity-status ${activity.status}`}>
                                                        {activity.status}
                                                    </div>
                                                </div>
                                            );
                                        })}
                                        {stats.recentActivity.length === 0 && (
                                            <div className="no-activity">
                                                <p>No recent activity</p>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Top Patterns */}
                                <div className="patterns-card">
                                    <div className="card-header">
                                        <h3>Top Detected Patterns</h3>
                                        <Filter size={16} />
                                    </div>
                                    <div className="patterns-list">
                                        {stats.topPatterns.map((pattern, index) => (
                                            <div 
                                                key={index} 
                                                className="pattern-item"
                                                onClick={() => togglePatternExpansion(index)}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <div className="pattern-rank">
                                                    #{index + 1}
                                                </div>
                                                <div className="pattern-info">
                                                    <p className="pattern-name">{pattern.pattern}</p>
                                                    <p className="pattern-count">{pattern.count} detections</p>
                                                </div>
                                                <div className="pattern-bar">
                                                    <div 
                                                        className="pattern-fill"
                                                        style={{ 
                                                            width: `${(pattern.count / (stats.totalScans || 1)) * 100}%`,
                                                            transition: 'width 0.3s ease'
                                                        }}
                                                    ></div>
                                                </div>
                                                {expandedPatterns.has(index) && (
                                                    <div className={`pattern-expand ${expandedPatterns.has(index) ? 'visible' : ''}`} style={{
                                                        gridColumn: '1 / -1',
                                                        marginTop: '8px',
                                                        padding: '12px',
                                                        background: '#1e293b',
                                                        borderRadius: '8px',
                                                        fontSize: '0.9em'
                                                    }}>
                                                        <p style={{ margin: 0 }}>
                                                            This pattern was found in {pattern.count} of your scans. 
                                                            Scans with this pattern:
                                                        </p>
                                                        <ul style={{ margin: '8px 0 0', paddingLeft: '20px' }}>
                                                            {history
                                                                .filter(h => h.findings?.some(f => f.type === pattern.pattern))
                                                                .slice(0, 3)
                                                                .map((h, hi) => (
                                                                    <li key={hi}>
                                                                        <a href={`/analyze?url=${encodeURIComponent(h.url)}`} 
                                                                           style={{ color: '#60a5fa', textDecoration: 'none' }}>
                                                                            {h.url}
                                                                        </a>
                                                                    </li>
                                                                ))}
                                                        </ul>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                        {stats.topPatterns.length === 0 && (
                                            <div className="no-patterns">
                                                <p>No patterns detected yet</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Quick Actions */}
                        <section className="quick-actions">
                            <h2>Quick Actions</h2>
                            <div className="actions-grid">
                                <Link to="/analyze" className="action-card">
                                    <div className="action-icon">
                                        <Target size={32} />
                                    </div>
                                    <h3>Scan Website</h3>
                                    <p>Analyze any URL for dark patterns</p>
                                </Link>

                                <Link to="/dashboard?view=history" className="action-card">
                                    <div className="action-icon">
                                        <History size={32} />
                                    </div>
                                    <h3>View History</h3>
                                    <p>Access your scan history</p>
                                </Link>

                                <button type="button" className="action-card" onClick={exportReport}>
                                    <div className="action-icon">
                                        <Share2 size={32} />
                                    </div>
                                    <h3>Share Results</h3>
                                    <p>Export and share findings</p>
                                </button>

                                <Link to="/settings" className="action-card">
                                    <div className="action-icon">
                                        <Settings size={32} />
                                    </div>
                                    <h3>Settings</h3>
                                    <p>Customize your experience</p>
                                </Link>
                            </div>
                        </section>
                    </>
                )}
            </main>
        </div>
    );
};

export default EnhancedClientHome;
