import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
    Activity, Users, Shield, Zap, Search, ArrowUpRight, 
    Download, RefreshCcw, LayoutDashboard, Database, 
    Bell, Settings, LogOut, ChevronRight, UserCheck, ShieldAlert,
    ArrowLeft, User, TrendingUp, TrendingDown, BarChart3,
    PieChart, Calendar, Filter, MoreVertical, Eye, Edit,
    Trash2, Mail, Phone, MapPin, Clock, CheckCircle, XCircle,
    AlertTriangle, Globe, Lock, Unlock, Ban, UserPlus,
    FileText, Archive, Cpu, HardDrive, Wifi, Server,
    Monitor, Smartphone, Tablet, Laptop, Terminal, ShieldCheck
} from 'lucide-react';
import { 
    LineChart, Line, XAxis, YAxis, CartesianGrid, 
    Tooltip, ResponsiveContainer, AreaChart, Area,
    BarChart, Bar, PieChart as RechartsPieChart, Pie, Cell,
    Legend
} from 'recharts';
import axios from 'axios';
import Swal from 'sweetalert2';
import './EnhancedAdminDashboard.css';

const API_BASE_URL = "/api";

const EnhancedAdminDashboard = () => {
    const [stats, setStats] = useState({ 
        total_users: 0, total_scans: 0, total_safe: 0, total_threats: 0, 
        hourly_stats: [], weekly_stats: [], monthly_stats: [],
        system_health: 'healthy', uptime: '99.9%', response_time: '245ms'
    });
    const [chartRange, setChartRange] = useState('W');
    const [users, setUsers] = useState([]);
    const [scans, setScans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');
    const [adminName] = useState('Admin');
    const [searchQuery, setSearchQuery] = useState('');
    const [showNotifications, setShowNotifications] = useState(false);
    const [showUserMenu, setShowUserMenu] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [notifications, setNotifications] = useState([
        { id: 1, type: 'warning', message: 'High traffic detected on scan API', time: '2 min ago' },
        { id: 2, type: 'info', message: 'System backup completed successfully', time: '15 min ago' },
        { id: 3, type: 'success', message: 'New user registration milestone reached', time: '1 hour ago' }
    ]);

    useEffect(() => {
        document.title = 'Dark Pattern Detection Admin Dashboard';
        fetchDashboardData();
        
        const interval = setInterval(fetchDashboardData, 30000); // Update every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchDashboardData = async () => {
        try {
            const [statsRes, usersRes, scansRes] = await Promise.all([
                axios.get(`${API_BASE_URL}/admin/stats`),
                axios.get(`${API_BASE_URL}/admin/users`),
                axios.get(`${API_BASE_URL}/admin/scans`)
            ]);
            
            setStats(statsRes.data);
            setUsers(usersRes.data);
            setScans(scansRes.data);
        } catch {
            // Dashboard data could not be loaded. The page will update when the next fetch completes.
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await axios.get(`${API_BASE_URL}/admin/logout`);
            window.location.href = '/admin/login';
        } catch {
            window.location.href = '/admin/login';
        }
    };

    const getChartData = () => {
        switch (chartRange) {
            case 'D':
                return stats.hourly_stats || [];
            case 'W':
                return stats.weekly_stats || [];
            case 'M':
                return stats.monthly_stats || [];
            default:
                return stats.weekly_stats || [];
        }
    };

    const getSystemHealthColor = (status) => {
        switch (status) {
            case 'healthy': return '#10b981';
            case 'warning': return '#f59e0b';
            case 'critical': return '#ef4444';
            default: return '#6b7280';
        }
    };

    const getRiskDistribution = () => {
        const safe = stats.total_safe || 0;
        const threats = stats.total_threats || 0;
        const total = safe + threats;
        
        if (total === 0) return [
            { name: 'Safe', value: 1, color: '#10b981' },
            { name: 'Threats', value: 0, color: '#ef4444' }
        ];
        
        return [
            { name: 'Safe', value: safe, color: '#10b981' },
            { name: 'Threats', value: threats, color: '#ef4444' }
        ];
    };

    if (loading) {
        return (
            <div className="enhanced-admin-loading">
                <div className="loading-container">
                    <div className="loading-animation">
                        <Shield className="loading-icon" size={48} />
                        <div className="loading-rings">
                            <div className="ring"></div>
                            <div className="ring"></div>
                            <div className="ring"></div>
                        </div>
                    </div>
                    <h2>Initializing Admin Dashboard</h2>
                    <p>Loading system metrics and user data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="enhanced-admin-dashboard">
            {/* Enhanced Header */}
            <header className="admin-header">
                <div className="header-container">
                    <div className="header-left">
                        <Link to="/admin" className="admin-brand">
                            <div className="brand-logo">
                                <Shield size={32} />
                                <div className="brand-pulse"></div>
                            </div>
                            <div className="brand-text">
                                <span className="brand-name">Dark Pattern Detection</span>
                                <span className="brand-role">Admin</span>
                            </div>
                        </Link>
                    </div>

                    <nav className="admin-nav">
                        <button 
                            className={`nav-btn ${activeTab === 'overview' ? 'active' : ''}`}
                            onClick={() => setActiveTab('overview')}
                        >
                            <LayoutDashboard size={18} />
                            Overview
                        </button>
                        <button 
                            className={`nav-btn ${activeTab === 'users' ? 'active' : ''}`}
                            onClick={() => setActiveTab('users')}
                        >
                            <Users size={18} />
                            Users
                        </button>
                        <button 
                            className={`nav-btn ${activeTab === 'scans' ? 'active' : ''}`}
                            onClick={() => setActiveTab('scans')}
                        >
                            <Search size={18} />
                            Scans
                        </button>
                        <button 
                            className={`nav-btn ${activeTab === 'projects' ? 'active' : ''}`}
                            onClick={() => setActiveTab('projects')}
                        >
                            <FileText size={18} />
                            Projects
                        </button>
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
                                        <h4>System Notifications</h4>
                                        <button onClick={() => setNotifications([])}>
                                            Clear all
                                        </button>
                                    </div>
                                    <div className="notification-list">
                                        {notifications.map(notif => (
                                            <div key={notif.id} className={`notification-item ${notif.type}`}>
                                                <div className="notification-icon">
                                                    {notif.type === 'warning' ? <AlertTriangle size={16} /> : 
                                                     notif.type === 'success' ? <CheckCircle size={16} /> : 
                                                     <Activity size={16} />}
                                                </div>
                                                <div className="notification-content">
                                                    <p>{notif.message}</p>
                                                    <span className="notification-time">{notif.time}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Settings */}
                        <button 
                            className="settings-btn"
                            onClick={() => setShowSettings(!showSettings)}
                        >
                            <Settings size={20} />
                        </button>

                        {/* User Menu */}
                        <div className="user-menu-wrapper">
                            <button 
                                className="user-menu-btn"
                                onClick={() => setShowUserMenu(!showUserMenu)}
                            >
                                <div className="user-avatar">
                                    <User size={20} />
                                </div>
                                <span className="user-name">{adminName}</span>
                                <ChevronRight size={16} className="chevron" />
                            </button>
                            
                            {showUserMenu && (
                                <div className="user-dropdown">
                                    <Link to="/admin/profile" className="dropdown-item">
                                        <User size={16} />
                                        Profile
                                    </Link>
                                    <Link to="/admin/settings" className="dropdown-item">
                                        <Settings size={16} />
                                        Settings
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

            <main className="admin-main">
                {activeTab === 'overview' && (
                    <div className="overview-content">
                        {/* System Health Banner */}
                        <div className="health-banner">
                            <div className="health-indicator">
                                <div className="health-dot" style={{ backgroundColor: getSystemHealthColor(stats.system_health) }}></div>
                                <span className="health-text">System {stats.system_health}</span>
                            </div>
                            <div className="health-stats">
                                <div className="health-stat">
                                    <Clock size={16} />
                                    <span>Uptime: {stats.uptime}</span>
                                </div>
                                <div className="health-stat">
                                    <Activity size={16} />
                                    <span>Response: {stats.response_time}</span>
                                </div>
                            </div>
                        </div>

                        {/* Key Metrics */}
                        <div className="metrics-grid">
                            <div className="metric-card primary">
                                <div className="metric-header">
                                    <div className="metric-icon">
                                        <Users size={24} />
                                    </div>
                                    <div className="metric-trend">
                                        <TrendingUp size={16} />
                                        <span>+12%</span>
                                    </div>
                                </div>
                                <div className="metric-content">
                                    <h3>{stats.total_users}</h3>
                                    <p>Total Users</p>
                                </div>
                            </div>

                            <div className="metric-card success">
                                <div className="metric-header">
                                    <div className="metric-icon">
                                        <Search size={24} />
                                    </div>
                                    <div className="metric-trend">
                                        <TrendingUp size={16} />
                                        <span>+8%</span>
                                    </div>
                                </div>
                                <div className="metric-content">
                                    <h3>{stats.total_scans}</h3>
                                    <p>Total Scans</p>
                                </div>
                            </div>

                            <div className="metric-card info">
                                <div className="metric-header">
                                    <div className="metric-icon">
                                        <ShieldCheck size={24} />
                                    </div>
                                    <div className="metric-trend">
                                        <TrendingUp size={16} />
                                        <span>+5%</span>
                                    </div>
                                </div>
                                <div className="metric-content">
                                    <h3>{stats.total_safe}</h3>
                                    <p>Safe Sites</p>
                                </div>
                            </div>

                            <div className="metric-card danger">
                                <div className="metric-header">
                                    <div className="metric-icon">
                                        <ShieldAlert size={24} />
                                    </div>
                                    <div className="metric-trend">
                                        <TrendingDown size={16} />
                                        <span>-3%</span>
                                    </div>
                                </div>
                                <div className="metric-content">
                                    <h3>{stats.total_threats}</h3>
                                    <p>Threats Detected</p>
                                </div>
                            </div>
                        </div>

                        {/* Charts Section */}
                        <div className="charts-section">
                            <div className="chart-container">
                                <div className="chart-header">
                                    <h3>Activity Trends</h3>
                                    <div className="chart-controls">
                                        <button 
                                            className={`chart-btn ${chartRange === 'D' ? 'active' : ''}`}
                                            onClick={() => setChartRange('D')}
                                        >
                                            Day
                                        </button>
                                        <button 
                                            className={`chart-btn ${chartRange === 'W' ? 'active' : ''}`}
                                            onClick={() => setChartRange('W')}
                                        >
                                            Week
                                        </button>
                                        <button 
                                            className={`chart-btn ${chartRange === 'M' ? 'active' : ''}`}
                                            onClick={() => setChartRange('M')}
                                        >
                                            Month
                                        </button>
                                    </div>
                                </div>
                                <div className="chart-content">
                                    <ResponsiveContainer width="100%" height={300}>
                                        <AreaChart data={getChartData()}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                            <XAxis dataKey="name" stroke="#9ca3af" />
                                            <YAxis stroke="#9ca3af" />
                                            <Tooltip 
                                                contentStyle={{ 
                                                    backgroundColor: '#1f2937', 
                                                    border: '1px solid #374151',
                                                    borderRadius: '8px'
                                                }}
                                            />
                                            <Area 
                                                type="monotone" 
                                                dataKey="scans" 
                                                stroke="#3b82f6" 
                                                fill="#3b82f6" 
                                                fillOpacity={0.3}
                                            />
                                            <Area 
                                                type="monotone" 
                                                dataKey="users" 
                                                stroke="#8b5cf6" 
                                                fill="#8b5cf6" 
                                                fillOpacity={0.3}
                                            />
                                        </AreaChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            <div className="chart-container">
                                <div className="chart-header">
                                    <h3>Risk Distribution</h3>
                                    <button className="chart-btn">
                                        <Download size={16} />
                                        Export
                                    </button>
                                </div>
                                <div className="chart-content">
                                    <ResponsiveContainer width="100%" height={300}>
                                        <RechartsPieChart>
                                            <Pie
                                                data={getRiskDistribution()}
                                                cx="50%"
                                                cy="50%"
                                                innerRadius={60}
                                                outerRadius={100}
                                                paddingAngle={5}
                                                dataKey="value"
                                            >
                                                {getRiskDistribution().map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                            <Legend />
                                        </RechartsPieChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'users' && (
                    <div className="users-content">
                        <div className="content-header">
                            <h2>User Management</h2>
                            <div className="header-actions">
                                <div className="search-box">
                                    <Search size={20} />
                                    <input
                                        type="text"
                                        placeholder="Search users..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                    />
                                </div>
                                <button className="primary-btn">
                                    <UserPlus size={16} />
                                    Add User
                                </button>
                            </div>
                        </div>

                        <div className="users-table">
                            <div className="table-header">
                                <div className="table-cell">User</div>
                                <div className="table-cell">Email</div>
                                <div className="table-cell">Status</div>
                                <div className="table-cell">Scans</div>
                                <div className="table-cell">Last Active</div>
                                <div className="table-cell">Actions</div>
                            </div>
                            <div className="table-body">
                                {users.filter(user => 
                                    user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                    user.email.toLowerCase().includes(searchQuery.toLowerCase())
                                ).map(user => (
                                    <div key={user.id} className="table-row">
                                        <div className="table-cell">
                                            <div className="user-info">
                                                <div className="user-avatar">
                                                    {user.username.charAt(0).toUpperCase()}
                                                </div>
                                                <span>{user.username}</span>
                                            </div>
                                        </div>
                                        <div className="table-cell">{user.email}</div>
                                        <div className="table-cell">
                                            <span className={`status-badge ${user.status}`}>
                                                {user.status}
                                            </span>
                                        </div>
                                        <div className="table-cell">{user.scan_count || 0}</div>
                                        <div className="table-cell">
                                            {user.last_active ? new Date(user.last_active).toLocaleDateString() : 'Never'}
                                        </div>
                                        <div className="table-cell">
                                            <div className="action-buttons">
                                                <button className="action-btn view">
                                                    <Eye size={16} />
                                                </button>
                                                <button className="action-btn edit">
                                                    <Edit size={16} />
                                                </button>
                                                <button className="action-btn delete">
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'scans' && (
                    <div className="scans-content">
                        <div className="content-header">
                            <h2>Scan History</h2>
                            <div className="header-actions">
                                <div className="search-box">
                                    <Search size={20} />
                                    <input
                                        type="text"
                                        placeholder="Search scans..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                    />
                                </div>
                                <button className="secondary-btn">
                                    <Download size={16} />
                                    Export
                                </button>
                            </div>
                        </div>

                        <div className="scans-table">
                            <div className="table-header">
                                <div className="table-cell">URL</div>
                                <div className="table-cell">User</div>
                                <div className="table-cell">Trust Score</div>
                                <div className="table-cell">Status</div>
                                <div className="table-cell">Date</div>
                                <div className="table-cell">Actions</div>
                            </div>
                            <div className="table-body">
                                {scans.filter(scan => 
                                    scan.url.toLowerCase().includes(searchQuery.toLowerCase())
                                ).map(scan => (
                                    <div key={scan.id} className="table-row">
                                        <div className="table-cell">
                                            <div className="url-info">
                                                <Globe size={16} />
                                                <span>{scan.url}</span>
                                            </div>
                                        </div>
                                        <div className="table-cell">{scan.username}</div>
                                        <div className="table-cell">
                                            <div className="trust-score">
                                                <div className="score-bar">
                                                    <div 
                                                        className="score-fill"
                                                        style={{ width: `${scan.trust_score}%` }}
                                                    ></div>
                                                </div>
                                                <span>{scan.trust_score}%</span>
                                            </div>
                                        </div>
                                        <div className="table-cell">
                                            <span className={`status-badge ${scan.safety_status}`}>
                                                {scan.safety_status}
                                            </span>
                                        </div>
                                        <div className="table-cell">
                                            {new Date(scan.timestamp).toLocaleDateString()}
                                        </div>
                                        <div className="table-cell">
                                            <div className="action-buttons">
                                                <button className="action-btn view">
                                                    <Eye size={16} />
                                                </button>
                                                <button className="action-btn">
                                                    <Download size={16} />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'projects' && (
                    <div className="analytics-content">
                        <div className="content-header">
                            <h2>Project Overview</h2>
                            <div className="header-actions">
                                <div className="date-range">
                                    <Calendar size={16} />
                                    <span>Last 30 Days</span>
                                </div>
                                <button className="primary-btn">
                                    <Download size={16} />
                                    Export Snapshot
                                </button>
                            </div>
                        </div>

                        <div className="analytics-grid">
                            <div className="analytics-card">
                                <h3>Project Activity</h3>
                                <ResponsiveContainer width="100%" height={250}>
                                    <BarChart data={stats.weekly_stats}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="name" stroke="#9ca3af" />
                                        <YAxis stroke="#9ca3af" />
                                        <Tooltip />
                                        <Bar dataKey="scans" fill="#3b82f6" />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>

                            <div className="analytics-card">
                                <h3>Project Health</h3>
                                <div className="performance-metrics">
                                    <div className="metric">
                                        <div className="metric-label">Total Jobs</div>
                                        <div className="metric-value">{stats.total_scans}</div>
                                        <div className="metric-bar">
                                            <div className="metric-fill" style={{ width: `${Math.min(100, stats.total_scans || 0) % 100}%` }}></div>
                                        </div>
                                    </div>
                                    <div className="metric">
                                        <div className="metric-label">Contributors</div>
                                        <div className="metric-value">{stats.total_users}</div>
                                        <div className="metric-bar">
                                            <div className="metric-fill" style={{ width: `${Math.min(100, stats.total_users || 0) % 100}%` }}></div>
                                        </div>
                                    </div>
                                    <div className="metric">
                                        <div className="metric-label">Successful Runs</div>
                                        <div className="metric-value">{stats.total_safe}</div>
                                        <div className="metric-bar">
                                            <div className="metric-fill" style={{ width: `${Math.min(100, stats.total_safe || 0) % 100}%` }}></div>
                                        </div>
                                    </div>
                                    <div className="metric">
                                        <div className="metric-label">Failed Runs</div>
                                        <div className="metric-value">{stats.total_threats}</div>
                                        <div className="metric-bar">
                                            <div className="metric-fill" style={{ width: `${Math.min(100, stats.total_threats || 0) % 100}%` }}></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default EnhancedAdminDashboard;
