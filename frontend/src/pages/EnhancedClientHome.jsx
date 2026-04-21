import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import API_BASE_URL from '../config';
import Cookies from 'js-cookie';
import { 
    Shield, 
    Search, 
    History, 
    User, 
    LogOut, 
    Zap, 
    AlertTriangle, 
    CheckCircle2, 
    Globe, 
    FileText,
    TrendingUp,
    ShieldCheck,
    Activity,
    Clock,
    Award,
    BarChart3,
    Settings,
    Bell,
    HelpCircle,
    ChevronRight,
    Star,
    Target,
    Lock,
    Eye,
    Download,
    Share2,
    Filter,
    Calendar,
    TrendingDown
} from 'lucide-react';
import './EnhancedClientHome.css';

const EnhancedClientHome = () => {
    const [user, setUser] = useState(Cookies.get('user') || 'User');
    const [history, setHistory] = useState([]);
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
    const [selectedTimeRange, setSelectedTimeRange] = useState('week');
    const [notifications, setNotifications] = useState([]);
    const [showNotifications, setShowNotifications] = useState(false);
    const [showUserMenu, setShowUserMenu] = useState(false);

    useEffect(() => {
        document.title = 'Aegis Pro - Security Dashboard';
        fetchData();
        
        // Simulate real-time updates
        const interval = setInterval(() => {
            fetchStats();
        }, 30000); // Update every 30 seconds

        return () => clearInterval(interval);
    }, []);

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

        } catch (err) {
            console.error("Session verification failed", err);
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
        } catch (err) {
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
                        <h2>Initializing Aegis Pro</h2>
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
                                <span className="brand-name">Aegis</span>
                                <span className="brand-tagline">Pro</span>
                            </div>
                        </Link>
                    </div>
                    
                    <nav className="header-nav">
                        <Link to="/" className="nav-link active">Dashboard</Link>
                        <Link to="/analyze" className="nav-link">Scan</Link>
                        <Link to="/dashboard" className="nav-link">History</Link>
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
                                className="user-menu-btn"
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
                        <div className="welcome-badge">
                            <Zap size={16} />
                            <span>AI-Powered Protection Active</span>
                        </div>
                        <h1>Welcome back, <span className="user-highlight">{user}</span></h1>
                        <p className="welcome-subtitle">
                            Your digital security dashboard with real-time threat detection and analysis
                        </p>
                        
                        <div className="welcome-actions">
                            <Link to="/analyze" className="primary-btn">
                                <Target size={20} />
                                Start New Scan
                            </Link>
                            <button className="secondary-btn">
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

                    <div className="stats-grid">
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
                                <Link to="/dashboard" className="view-all">
                                    View all
                                </Link>
                            </div>
                            <div className="activity-list">
                                {stats.recentActivity.map((activity, index) => (
                                    <div key={index} className="activity-item">
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
                                ))}
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
                                    <div key={index} className="pattern-item">
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
                                                style={{ width: `${(pattern.count / stats.totalScans) * 100}%` }}
                                            ></div>
                                        </div>
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

                        <Link to="/dashboard" className="action-card">
                            <div className="action-icon">
                                <History size={32} />
                            </div>
                            <h3>View History</h3>
                            <p>Access your scan history</p>
                        </Link>

                        <button className="action-card">
                            <div className="action-icon">
                                <Share2 size={32} />
                            </div>
                            <h3>Share Results</h3>
                            <p>Export and share findings</p>
                        </button>

                        <button className="action-card">
                            <div className="action-icon">
                                <Settings size={32} />
                            </div>
                            <h3>Settings</h3>
                            <p>Customize your experience</p>
                        </button>
                    </div>
                </section>
            </main>
        </div>
    );
};

export default EnhancedClientHome;
