# Aegis Pro Documentation - Detailed Explanation

## 📋 Overview of Documentation Sections

This document provides detailed explanations of each section in the Aegis Pro project documentation to help stakeholders understand the system comprehensively.

---

## 1. Project Synopsis - Detailed Explanation

### **Purpose & Vision**
The Project Synopsis serves as the executive summary of Aegis Pro, answering the fundamental questions:
- **What is Aegis Pro?** - An advanced dark pattern detection system
- **Why does it exist?** - To protect users from manipulative design patterns
- **Who is it for?** - Multiple user groups with different needs

### **Key Components Explained**

#### **Mission Statement**
```
"To create a safer digital environment by automatically detecting 
and alerting users to manipulative design patterns that exploit 
psychological vulnerabilities."
```
**Significance**: This drives all technical decisions and feature development.

#### **Core Features Breakdown**
1. **Real-time Detection**: 
   - Analyzes web pages as users browse
   - Provides immediate alerts for dangerous patterns
   - Works in background without user intervention

2. **Multi-Engine Analysis**:
   - **NLP Engine**: Reads and understands text content
   - **Visual Engine**: Analyzes visual design elements
   - **Behavioral Engine**: Tracks user interaction patterns

3. **Chrome Extension**:
   - Browser-based protection for everyday users
   - Integrates seamlessly with browsing experience
   - Provides real-time warnings and insights

4. **Trust Scoring**:
   - Quantifies website trustworthiness (0-100 scale)
   - Helps users make informed decisions
   - Provides context for detected patterns

#### **Target User Groups**
- **End Users**: General public seeking protection from manipulation
- **Administrators**: System managers who need oversight capabilities
- **Developers**: Web developers checking compliance
- **Researchers**: Academic/industry professionals studying dark patterns

---

## 2. Software Requirements Specification (SRS) - Detailed Explanation

### **Purpose of SRS**
The SRS document serves as the contractual agreement between stakeholders and developers, defining exactly what the system must do.

### **Functional Requirements (FR) Explained**

#### **FR-1: Pattern Detection**
These requirements define the core detection capabilities:

**FR-1.1: Linguistic Dark Patterns**
- **What**: System must detect text-based manipulation
- **Examples**: "Only 2 left!" (scarcity), "Hurry! Offer ends soon!" (urgency)
- **Why**: Text is the most common manipulation vector

**FR-1.2: Visual Dark Patterns**
- **What**: System must detect visual manipulation techniques
- **Examples**: Hidden cancel buttons, low contrast text, misleading hierarchy
- **Why**: Visual design can hide important information

**FR-1.3: Behavioral Dark Patterns**
- **What**: System must detect interaction-based manipulation
- **Examples**: Forced actions, countdown timers that reset, fake notifications
- **Why**: Behavior manipulation exploits user psychology

**FR-1.4: Severity Scoring**
- **What**: System must rate pattern severity
- **Scale**: Low, Medium, High, Critical
- **Why**: Helps users prioritize which patterns to address

**FR-1.5: Remediation Suggestions**
- **What**: System must suggest fixes for detected patterns
- **Why**: Helps developers improve their designs

#### **FR-2: User Interface Requirements**
Define how users interact with the system:

**FR-2.1: Web Interface**
- **What**: Browser-based application for full functionality
- **Features**: Dashboard, history, settings, analysis tools

**FR-2.2: Chrome Extension Interface**
- **What**: Browser extension for real-time protection
- **Features**: Popup alerts, side panel, quick actions

**FR-2.3: Administrative Dashboard**
- **What**: Management interface for system administrators
- **Features**: User management, system monitoring, analytics

**FR-2.4: Responsive Design**
- **What**: Works on all device sizes
- **Importance**: Users access from phones, tablets, desktops

**FR-2.5: Real-time Notifications**
- **What**: Immediate alerts for detected patterns
- **Why**: Users need instant feedback for protection

#### **FR-3: Data Management Requirements**
Define how the system handles data:

**FR-3.1: User Accounts**
- **What**: Store user profiles and authentication
- **Features**: Login, registration, preferences, history

**FR-3.2: Scan History**
- **What**: Record all analysis results
- **Features**: Search, filter, export, analytics

**FR-3.3: Pattern Database**
- **What**: Maintain library of known dark patterns
- **Features**: Pattern definitions, detection rules, updates

**FR-3.4: Data Export**
- **What**: Allow users to export their data
- **Formats**: CSV, JSON, PDF reports

**FR-3.5: Data Retention**
- **What**: Automatically manage data lifecycle
- **Policies**: Delete old data, comply with regulations

#### **FR-4: Integration Requirements**
Define how the system connects with other services:

**FR-4.1: MongoDB Integration**
- **What**: Use MongoDB for data persistence
- **Why**: Flexible schema for complex data structures

**FR-4.2: Ollama AI Integration**
- **What**: Use AI for advanced pattern recognition
- **Why**: Machine learning improves detection accuracy

**FR-4.3: REST API**
- **What**: Provide RESTful API for all functionality
- **Why**: Standard interface for frontend and extensions

**FR-4.4: Chrome Extension API**
- **What**: Integrate with Chrome extension system
- **Why**: Browser-based protection requires native integration

**FR-4.5: External Authentication**
- **What**: Support third-party login (Google, GitHub)
- **Why**: Improves user experience and security

### **Non-Functional Requirements (NFR) Explained**

#### **NFR-1: Performance Requirements**
Define how well the system must perform:

**NFR-1.1: Analysis Speed**
- **Requirement**: < 2 seconds per page analysis
- **Why**: Users won't wait long for protection
- **Measurement**: Average analysis time across all engines

**NFR-1.2: Concurrency**
- **Requirement**: Support 1000+ simultaneous users
- **Why**: Must handle peak usage periods
- **Measurement**: Concurrent active sessions

**NFR-1.3: Uptime**
- **Requirement**: 99.9% availability
- **Why**: Protection must be reliable
- **Measurement**: Downtime per month < 43 minutes

**NFR-1.4: Caching**
- **Requirement**: Cache frequently accessed data
- **Why**: Improves response times
- **Implementation**: Redis for session and result caching

**NFR-1.5: Query Optimization**
- **Requirement**: Optimize database queries
- **Why**: Ensures scalability as data grows
- **Measurement**: Query response times < 100ms

#### **NFR-2: Security Requirements**
Define how the system protects itself and users:

**NFR-2.1: Authentication**
- **Requirement**: Secure user authentication system
- **Implementation**: bcrypt password hashing, JWT tokens
- **Why**: Protect user accounts and data

**NFR-2.2: Data Encryption**
- **Requirement**: Encrypt sensitive data at rest
- **Implementation**: AES-256 encryption for PII
- **Why**: Compliance with data protection regulations

**NFR-2.3: Injection Prevention**
- **Requirement**: Prevent SQL/NoSQL injection attacks
- **Implementation**: Parameterized queries, input validation
- **Why**: Common attack vector that must be blocked

**NFR-2.4: Rate Limiting**
- **Requirement**: Limit API request rates
- **Implementation**: Token bucket algorithm
- **Why**: Prevent abuse and DoS attacks

**NFR-2.5: Audit Logging**
- **Requirement**: Log all system actions
- **Implementation**: Comprehensive logging with timestamps
- **Why**: Security monitoring and compliance

#### **NFR-3: Usability Requirements**
Define how easy the system is to use:

**NFR-3.1: Intuitive Interface**
- **Requirement**: Easy-to-use interface design
- **Implementation**: User testing, feedback-driven design
- **Why**: Users need protection without technical knowledge

**NFR-3.2: WCAG Compliance**
- **Requirement**: Meet WCAG 2.1 AA accessibility standards
- **Implementation**: ARIA labels, keyboard navigation, color contrast
- **Why**: System must be accessible to all users

**NFR-3.3: Multi-language Support**
- **Requirement**: Support multiple languages
- **Implementation**: Internationalization framework
- **Why**: Global user base needs local language support

**NFR-3.4: Documentation**
- **Requirement**: Comprehensive user documentation
- **Implementation**: User guides, API docs, tutorials
- **Why**: Users need help understanding features

**NFR-3.5: Accessibility Features**
- **Requirement**: Screen reader support, keyboard navigation
- **Implementation**: Semantic HTML, ARIA landmarks
- **Why**: Ensure equal access for disabled users

#### **NFR-4: Reliability Requirements**
Define how dependable the system must be:

**NFR-4.1: Error Handling**
- **Requirement**: Graceful error handling throughout system
- **Implementation**: Try-catch blocks, user-friendly error messages
- **Why**: System should never crash unexpectedly

**NFR-4.2: Backup Mechanisms**
- **Requirement**: Automated backup systems
- **Implementation**: Daily database backups, offsite storage
- **Why**: Data loss prevention

**NFR-4.3: Graceful Degradation**
- **Requirement**: Function with reduced capabilities when components fail
- **Implementation**: Fallback mechanisms, offline mode
- **Why**: System should provide basic protection even during issues

**NFR-4.4: Health Monitoring**
- **Requirement**: Continuous system health monitoring
- **Implementation**: Health checks, alerting, metrics
- **Why**: Proactive issue detection and resolution

**NFR-4.5: Automated Recovery**
- **Requirement**: Self-healing capabilities
- **Implementation**: Service restart, circuit breakers
- **Why**: Minimize downtime and manual intervention

### **Technical Requirements (TR) Explained**

#### **TR-1: Technology Stack**
Defines the specific technologies used:

**TR-1.1: Backend Technology**
- **Python 3.14+**: Latest Python version with new features
- **Flask Framework**: Lightweight, flexible web framework
- **Why**: Python has excellent ML/AI libraries

**TR-1.2: Frontend Technology**
- **React 18+**: Modern UI framework with hooks
- **Vite Build System**: Fast development and building
- **Why**: React ecosystem and performance benefits

**TR-1.3: Database Technology**
- **MongoDB Atlas**: Cloud-hosted NoSQL database
- **Mongoose ODM**: Object modeling for Node.js/JavaScript
- **Why**: Flexible schema for complex pattern data

**TR-1.4: AI/ML Technology**
- **Ollama**: Local AI model serving
- **Transformer Models**: State-of-the-art NLP models
- **Why**: Advanced pattern recognition capabilities

**TR-1.5: Extension Technology**
- **Chrome Extension Manifest V3**: Latest extension standards
- **Service Workers**: Background processing
- **Why**: Native browser integration for protection

#### **TR-2: System Requirements**
Defines minimum hardware/software needs:

**TR-2.1: Hardware Requirements**
- **4GB RAM**: Minimum for smooth operation
- **2GHz Processor**: Sufficient for real-time analysis
- **Why**: Balance performance and accessibility

**TR-2.2: Storage Requirements**
- **10GB Space**: For application, data, and logs
- **Why**: Adequate space for operation and growth

**TR-2.3: Network Requirements**
- **Active Internet**: Required for AI and database access
- **Why**: Cloud-based services need connectivity

**TR-2.4: Browser Requirements**
- **Chrome 90+**: Latest Chrome browser version
- **Why**: Extension compatibility and security

**TR-2.5: Development Requirements**
- **Node.js 16+**: For frontend development
- **Python 3.14+**: For backend development
- **Why**: Modern development tooling support

---

## 3. Entity Relationship (ER) Diagram - Detailed Explanation

### **Purpose of ER Diagram**
The ER diagram visualizes the database structure and relationships between different data entities in the system.

### **Database Schema Explained**

#### **Users Table**
**Purpose**: Stores all user account information
```python
{
    "_id": ObjectId,           # Primary key
    "username": String,        # Unique username
    "email": String,           # Unique email address
    "password_hash": String,    # Encrypted password
    "role": String,           # User role (user/admin)
    "created_at": DateTime,    # Account creation time
    "last_login": DateTime,    # Last login timestamp
    "is_active": Boolean,      # Account status
    "preferences": Object       # User settings and preferences
}
```
**Relationships**: 
- One-to-many with Analyses (one user can have many analyses)
- One-to-many with Admin_Logs (one admin can have many logs)
- One-to-many with Extension_Data (one user can have many extension sessions)

**Indexes**:
- email (unique) - Fast login queries
- username (unique) - Fast user lookups
- created_at - For user analytics

#### **Analyses Table**
**Purpose**: Stores all scan results and analysis data
```python
{
    "_id": ObjectId,           # Primary key
    "user_id": ObjectId,       # Foreign key to Users
    "url": String,             # Analyzed URL
    "html_content": String,     # Page HTML content
    "scan_results": Object,      # Complete scan results
    "trust_score": Integer,     # 0-100 trust score
    "detected_patterns": Array, # List of detected patterns
    "created_at": DateTime,    # Scan timestamp
    "status": String,          # Scan status
    "metadata": Object         # Additional metadata
}
```
**Relationships**:
- Many-to-one with Users (many analyses belong to one user)
- One-to-many with Scan_Results (one analysis has many results)

**Indexes**:
- user_id - Fast user history queries
- created_at - For chronological sorting
- url - For duplicate detection

#### **Patterns Table**
**Purpose**: Defines all dark pattern types and detection rules
```python
{
    "_id": ObjectId,           # Primary key
    "pattern_id": String,      # Unique pattern identifier
    "pattern_name": String,     # Human-readable name
    "pattern_type": String,     # Category (linguistic/visual/behavioral)
    "description": String,      # Pattern description
    "severity_level": String,   # Severity classification
    "detection_rules": Array,   # Detection algorithm rules
    "is_active": Boolean,      # Pattern status
    "created_at": DateTime     # Pattern creation time
}
```
**Relationships**:
- One-to-many with Scan_Results (one pattern can appear in many results)

**Indexes**:
- pattern_id (unique) - Fast pattern lookups
- pattern_type - For category filtering
- is_active - For active pattern queries

#### **Engines Table**
**Purpose**: Configuration for detection engines
```python
{
    "_id": ObjectId,           # Primary key
    "engine_name": String,      # Engine name (NLP/Visual/Behavioral)
    "engine_type": String,      # Engine classification
    "configuration": Object,     # Engine settings
    "supported_patterns": Array,  # List of supported patterns
    "is_active": Boolean,      # Engine status
    "last_updated": DateTime    # Last update timestamp
}
```
**Relationships**:
- One-to-many with Scan_Results (one engine produces many results)

**Indexes**:
- engine_name - Fast engine lookups
- is_active - For active engine queries

#### **Scan_Results Table**
**Purpose**: Detailed results from each engine for each analysis
```python
{
    "_id": ObjectId,           # Primary key
    "analysis_id": ObjectId,    # Foreign key to Analyses
    "engine_id": ObjectId,      # Foreign key to Engines
    "pattern_id": ObjectId,      # Foreign key to Patterns
    "detection_data": Object,   # Raw detection data
    "confidence_score": Float,   # Detection confidence (0-1)
    "detected_at": DateTime,    # Detection timestamp
    "remediation": Object      # Suggested fixes
}
```
**Relationships**:
- Many-to-one with Analyses (many results belong to one analysis)
- Many-to-one with Engines (many results from one engine)
- Many-to-one with Patterns (many results for one pattern)

**Indexes**:
- analysis_id - Fast result retrieval
- engine_id - For engine-specific queries
- pattern_id - For pattern analytics

#### **Admin_Logs Table**
**Purpose**: Tracks all administrative actions for security and auditing
```python
{
    "_id": ObjectId,           # Primary key
    "admin_id": ObjectId,       # Foreign key to Users
    "action": String,           # Action performed
    "resource": String,         # Target resource
    "details": Object,          # Action details
    "ip_address": String,       # Admin IP address
    "timestamp": DateTime       # Action timestamp
}
```
**Relationships**:
- Many-to-one with Users (many logs from one admin)

**Indexes**:
- admin_id - For admin-specific logs
- timestamp - For chronological queries
- action - For action type filtering

#### **Extension_Data Table**
**Purpose**: Stores Chrome extension session data
```python
{
    "_id": ObjectId,           # Primary key
    "user_id": ObjectId,       # Foreign key to Users
    "browser_session": String,   # Unique session identifier
    "page_scans": Array,       # List of scanned pages
    "settings": Object,         # Extension settings
    "last_sync": DateTime,      # Last sync timestamp
    "is_active": Boolean       # Session status
}
```
**Relationships**:
- Many-to-one with Users (many sessions for one user)

**Indexes**:
- user_id - For user session queries
- browser_session - For session lookups
- last_sync - For cleanup operations

### **Relationship Visualization**
The Mermaid diagram shows:
- **One-to-Many**: Users to Analyses (one user, many analyses)
- **Many-to-One**: Scan_Results to Analyses (many results, one analysis)
- **Junction Tables**: Complex many-to-many relationships
- **Foreign Keys**: Proper relational integrity

### **Data Flow Through Schema**
1. **User Registration**: Creates Users record
2. **Page Analysis**: Creates Analyses record
3. **Pattern Detection**: Creates Scan_Results records
4. **Admin Actions**: Creates Admin_Logs records
5. **Extension Usage**: Creates Extension_Data records

---

## 4. System Architecture & Design - Detailed Explanation

### **Purpose of Architecture Documentation**
The system architecture defines how different components interact and work together to provide the complete Aegis Pro functionality.

### **High-Level Architecture Explained**

#### **Layer 1: Client Layer**
**Purpose**: User-facing interfaces that interact with end users

**Chrome Extension**:
- **Background Service Worker**: Runs in background, handles API calls
- **Content Script**: Injected into web pages, monitors DOM changes
- **Popup Interface**: Quick access to features and settings
- **Side Panel**: Detailed analysis results and controls

**Web Interface**:
- **React Application**: Full-featured web application
- **Responsive Design**: Works on all device sizes
- **Progressive Web App**: Installable as desktop app
- **Real-time Updates**: WebSocket connections for live data

**Admin Dashboard**:
- **Management Interface**: System administration tools
- **Analytics Dashboard**: System performance and usage metrics
- **User Management**: User account administration
- **System Monitoring**: Health and performance monitoring

#### **Layer 2: API Gateway**
**Purpose**: Central entry point for all client requests

**Flask REST API**:
- **Request Routing**: Routes requests to appropriate handlers
- **Authentication**: Validates user sessions and permissions
- **Request Validation**: Validates and sanitizes input data
- **Response Formatting**: Standardizes API responses

**Authentication Service**:
- **Session Management**: Handles user login/logout
- **Token Validation**: JWT token verification
- **Permission Checking**: Role-based access control
- **Security Headers**: Adds security headers to responses

**CORS Handler**:
- **Cross-Origin Requests**: Handles browser security policies
- **Origin Validation**: Validates request origins
- **Header Management**: Manages CORS headers
- **Preflight Handling**: Handles OPTIONS requests

#### **Layer 3: Business Logic**
**Purpose**: Core application logic and data processing

**Tri-Engine Analyzer**:
- **Engine Coordination**: Orchestrates multiple detection engines
- **Result Aggregation**: Combines results from all engines
- **Trust Score Calculation**: Computes overall trustworthiness score
- **Pattern Prioritization**: Ranks patterns by severity and confidence

**NLP Engine**:
- **Text Analysis**: Processes text content for linguistic patterns
- **Pattern Matching**: Matches text against known patterns
- **Sentiment Analysis**: Detects emotional manipulation
- **Context Understanding**: Analyzes text in context

**Visual Engine**:
- **DOM Analysis**: Parses HTML structure and CSS
- **Contrast Checking**: Validates color contrast ratios
- **Layout Analysis**: Detects visual hierarchy issues
- **Hidden Element Detection**: Finds concealed UI elements

**Behavioral Engine**:
- **Network Monitoring**: Analyzes HTTP requests and responses
- **JavaScript Analysis**: Detects manipulative scripts
- **User Interaction Tracking**: Monitors user behavior patterns
- **Timing Analysis**: Detects countdown and time-based patterns

**Trust Pipeline**:
- **Score Aggregation**: Combines scores from all engines
- **Weight Calculation**: Applies weights to different pattern types
- **Confidence Assessment**: Evaluates detection confidence
- **Risk Assessment**: Determines overall risk level

#### **Layer 4: Data Layer**
**Purpose**: Data storage and retrieval systems

**MongoDB Atlas**:
- **Primary Database**: Stores all application data
- **Document Storage**: Flexible schema for complex data
- **Indexing**: Optimized query performance
- **Replication**: High availability and backup

**Redis Cache**:
- **Session Storage**: Fast user session access
- **Result Caching**: Caches frequent analysis results
- **Rate Limiting**: Stores rate limit counters
- **Temporary Data**: Short-term data storage

**File Storage**:
- **Static Assets**: Serves frontend files
- **User Uploads**: Stores user-submitted files
- **Log Files**: Stores application logs
- **Backup Storage**: Maintains data backups

#### **Layer 5: External Services**
**Purpose**: Third-party services that enhance functionality

**Ollama AI**:
- **Model Serving**: Provides AI model inference
- **Natural Language Processing**: Advanced text analysis
- **Pattern Recognition**: Machine learning-based detection
- **Insight Generation**: Provides AI-powered insights

**Email Service**:
- **User Notifications**: Sends email alerts
- **Account Verification**: Handles email verification
- **Password Reset**: Manages password recovery
- **System Alerts**: Sends administrative notifications

**Monitoring Service**:
- **Health Checks**: Monitors system health
- **Performance Metrics**: Tracks system performance
- **Error Tracking**: Captures and reports errors
- **Usage Analytics**: Tracks system usage patterns

### **Component Architecture Explained**

#### **Frontend Component Structure**
The frontend is organized into logical components for maintainability:

**Common Components**:
- **Header**: Navigation and user menu
- **Footer**: Links and information
- **Loading**: Loading indicators and spinners
- **Modal**: Dialog boxes and popups
- **Toast**: Notification system

**Chart Components**:
- **LineChart**: Time-series data visualization
- **PieChart**: Categorical data display
- **BarChart**: Comparative data display
- **GaugeChart**: Metric visualization

**Form Components**:
- **Input**: Text input fields
- **Select**: Dropdown menus
- **Checkbox**: Boolean selections
- **Button**: Action triggers
- **Form**: Form containers and validation

**UI Components**:
- **Card**: Content containers
- **Table**: Data tables
- **Badge**: Status indicators
- **Alert**: Warning and error messages
- **Spinner**: Loading indicators

#### **Backend Component Structure**
The backend follows modular architecture for scalability:

**Main Application**:
- **Flask App**: Core application setup
- **Configuration**: Environment and settings
- **Error Handlers**: Global error handling
- **Middleware**: Request/response processing

**Detection Engines**:
- **Linguistic Engine**: Text pattern detection
- **Visual Engine**: Visual pattern detection
- **Behavioral Engine**: Behavior pattern detection
- **Tri-Engine Analyzer**: Engine coordination

**Data Models**:
- **User Model**: User data structure
- **Analysis Model**: Analysis data structure
- **Pattern Model**: Pattern data structure
- **Validation**: Data validation rules

**Services**:
- **Auth Service**: Authentication logic
- **Email Service**: Email sending logic
- **Monitoring Service**: System monitoring
- **Cache Service**: Caching logic

#### **Chrome Extension Architecture**
The extension uses modern Chrome Extension Manifest V3:

**Manifest Configuration**:
- **Permissions**: Required browser permissions
- **Background Scripts**: Service worker setup
- **Content Scripts**: Page injection rules
- **Action Configuration**: Popup and side panel setup

**Background Service Worker**:
- **API Communication**: Handles backend communication
- **Event Handling**: Manages browser events
- **State Management**: Maintains extension state
- **Message Passing**: Communicates with content scripts

**Content Scripts**:
- **DOM Monitoring**: Watches for page changes
- **Pattern Detection**: Real-time pattern checking
- **Alert Display**: Shows warnings to users
- **Data Collection**: Gathers page data

**User Interface**:
- **Popup**: Quick access interface
- **Side Panel**: Detailed analysis view
- **Options**: Settings and preferences
- **Icons**: Visual indicators

### **Data Flow Architecture Explained**

#### **Request Flow**
1. **User Action**: User interacts with interface
2. **API Request**: Frontend sends request to backend
3. **Authentication**: API validates user session
4. **Business Logic**: Request processed by appropriate service
5. **Data Access**: Service interacts with database
6. **Response**: Results returned to frontend
7. **UI Update**: Frontend updates user interface

#### **Analysis Flow**
1. **Page Load**: User navigates to new page
2. **Data Collection**: Extension collects page data
3. **API Call**: Data sent to tri-engine analyzer
4. **Engine Processing**: Each engine processes data
5. **Result Aggregation**: Results combined and scored
6. **Storage**: Results stored in database
7. **Alert Display**: User notified of findings

#### **Real-time Updates**
1. **WebSocket Connection**: Frontend establishes connection
2. **Event Subscription**: Subscribes to relevant events
3. **Server Push**: Server pushes updates when events occur
4. **Client Update**: Frontend updates interface
5. **Connection Management**: Handles connection lifecycle

---

## 5. How It Works - Technical Flow - Detailed Explanation

### **Purpose of Technical Flow Documentation**
This section explains the step-by-step processes that make Aegis Pro function, from system startup to real-time pattern detection.

### **5.1 System Initialization Explained**

#### **5.1.1 Backend Startup Process**
**Step-by-Step Backend Initialization**:

1. **Environment Loading**:
   ```python
   # Load configuration from .env file
   load_dotenv()
   MONGO_URI = os.getenv("MONGO_URI")
   OLLAMA_URL = os.getenv("OLLAMA_URL")
   ```
   **Purpose**: Loads database URLs, API keys, and settings
   **Importance**: Secure configuration management

2. **Database Connection**:
   ```python
   # Establish MongoDB connection
   client = MongoClient(MONGO_URI)
   db = client['aegis_pro']
   ```
   **Purpose**: Connects to cloud database
   **Importance**: Data persistence and retrieval

3. **Engine Initialization**:
   ```python
   # Initialize detection engines
   tri_engine = TriEngineAnalyzer()
   tri_engine.initialize_engines()
   ```
   **Purpose**: Loads NLP, Visual, and Behavioral engines
   **Importance**: Core detection capabilities

4. **Dataset Loading**:
   ```python
   # Load pattern datasets
   load_datasets()
   ```
   **Purpose**: Loads known dark patterns and rules
   **Importance**: Pattern recognition database

5. **API Server Start**:
   ```python
   # Start Flask server
   app.run(host='0.0.0.0', port=5000)
   ```
   **Purpose**: Starts web server for API requests
   **Importance**: Enables client communication

6. **Health Check**:
   ```python
   # Verify all systems operational
   check_system_health()
   ```
   **Purpose**: Ensures all components working
   **Importance**: System reliability

#### **5.1.2 Frontend Initialization Process**
**React Application Startup**:

1. **React App Load**:
   ```javascript
   // Main React application entry
   import React from 'react';
   import ReactDOM from 'react-dom/client';
   import App from './App';
   
   const root = ReactDOM.createRoot(document.getElementById('root'));
   root.render(<App />);
   ```
   **Purpose**: Initializes React application
   **Importance**: User interface foundation

2. **API Connection**:
   ```javascript
   // Establish backend connection
   import API_BASE_URL from './config';
   axios.defaults.baseURL = API_BASE_URL;
   ```
   **Purpose**: Connects frontend to backend API
   **Importance**: Data communication

3. **Authentication Check**:
   ```javascript
   // Verify user session
   const isLoggedIn = !!Cookies.get('user');
   const isAdmin = !!Cookies.get('is_admin');
   ```
   **Purpose**: Checks if user is logged in
   **Importance**: Route protection and personalization

4. **Route Setup**:
   ```javascript
   // Configure application routes
   <Router>
     <Routes>
       <Route path="/" element={isLoggedIn ? <EnhancedClientHome /> : <LandingPage />} />
       <Route path="/admin" element={isAdmin ? <EnhancedAdminDashboard /> : <AdminLogin />} />
     </Routes>
   </Router>
   ```
   **Purpose**: Sets up navigation routes
   **Importance**: User navigation and access control

5. **Component Mount**:
   ```javascript
   // Mount appropriate components
   useEffect(() => {
     // Component initialization logic
   }, []);
   ```
   **Purpose**: Initializes page components
   **Importance**: Page-specific functionality

#### **5.1.3 Chrome Extension Load Process**
**Extension Initialization**:

1. **Manifest Load**:
   ```json
   {
     "manifest_version": 3,
     "name": "Aegis Pro",
     "background": { "service_worker": "background.js" },
     "content_scripts": [{ "matches": ["<all_urls>"], "js": ["content.js"] }]
   }
   ```
   **Purpose**: Extension configuration and permissions
   **Importance**: Browser integration

2. **Service Worker Start**:
   ```javascript
   // Background service worker
   chrome.runtime.onInstalled.addListener(() => {
     console.log('Aegis Pro extension installed');
   });
   ```
   **Purpose**: Background processing
   **Importance**: Continuous monitoring

3. **Content Script Inject**:
   ```javascript
   // Inject into web pages
   const script = document.createElement('script');
   script.src = chrome.runtime.getURL('content.js');
   document.head.appendChild(script);
   ```
   **Purpose**: Page monitoring capabilities
   **Importance**: Real-time detection

4. **Event Listeners**:
   ```javascript
   // Set up page monitoring
   document.addEventListener('DOMContentLoaded', startMonitoring);
   window.addEventListener('load', performInitialScan);
   ```
   **Purpose**: Monitor page changes
   **Importance**: Dynamic content detection

5. **API Registration**:
   ```javascript
   // Register with backend
   fetch('/api/extension/register', {
     method: 'POST',
     body: JSON.stringify({ extensionId: chrome.runtime.id })
   });
   ```
   **Purpose**: Register extension with backend
   **Importance**: System integration

### **5.2 Pattern Detection Flow Explained**

#### **5.2.1 Page Analysis Request**
**Complete Analysis Process**:

1. **Request Reception**:
   ```python
   @app.route('/api/tri-engine-analyze', methods=['POST'])
   def tri_engine_analyze():
       data = request.get_json()
       url = data.get('url')
       html_content = data.get('html_content')
   ```
   **Purpose**: Receives analysis request
   **Importance**: Entry point for detection

2. **Data Validation**:
   ```python
   # Validate input data
   if not url or not html_content:
       return jsonify({'error': 'Missing required data'}), 400
   ```
   **Purpose**: Ensures data quality
   **Importance**: Prevents errors and attacks

3. **Engine Initialization**:
   ```python
   # Initialize tri-engine analyzer
   tri_engine = TriEngineAnalyzer()
   tri_engine.setup_engines()
   ```
   **Purpose**: Prepares detection engines
   **Importance**: Ready for analysis

4. **Comprehensive Analysis**:
   ```python
   # Perform analysis
   results = tri_engine.analyze_comprehensive(
       url=url,
       html_content=html_content
   )
   ```
   **Purpose**: Runs all detection engines
   **Importance**: Thorough pattern detection

5. **Result Processing**:
   ```python
   # Process and format results
   formatted_results = {
       'trust_score': results['trust_score'],
       'patterns': results['findings'],
       'analysis_time': results['analysis_time'],
       'url': url
   }
   ```
   **Purpose**: Format for client consumption
   **Importance**: Consistent API responses

6. **Response Return**:
   ```python
   return jsonify(formatted_results)
   ```
   **Purpose**: Send results to client
   **Importance**: Complete analysis cycle

#### **5.2.2 NLP Engine Processing**
**Natural Language Processing Steps**:

1. **Text Extraction**:
   ```python
   def extract_text(self, html_content):
       soup = BeautifulSoup(html_content, 'html.parser')
       # Remove script and style elements
       for script in soup(["script", "style"]):
           script.decompose()
       return soup.get_text()
   ```
   **Purpose**: Extract clean text from HTML
   **Importance**: Text-based pattern detection

2. **Pattern Detection**:
   ```python
   def detect_urgency(self, text):
       urgency_patterns = [
           r'\b(hurry|urgent|immediate|limited time|expires soon)\b',
           r'\b(only \d+ left|few remaining|almost gone)\b',
           r'\b(offer ends|deal expires|last chance)\b'
       ]
       
       findings = []
       for pattern in urgency_patterns:
           matches = re.findall(pattern, text, re.IGNORECASE)
           if matches:
               findings.append({
                   'type': 'urgency',
                   'matches': matches,
                   'severity': 'medium'
               })
       return findings
   ```
   **Purpose**: Detect urgency-based manipulation
   **Importance**: Common dark pattern identification

3. **Sentiment Analysis**:
   ```python
   def analyze_sentiment(self, text):
       # Use AI model for sentiment analysis
       sentiment = self.ai_model.analyze(text)
       return {
           'positive': sentiment.positive,
           'negative': sentiment.negative,
           'manipulative': sentiment.manipulation_score
       }
   ```
   **Purpose**: Analyze emotional manipulation
   **Importance**: Detect psychological manipulation

4. **Context Understanding**:
   ```python
   def understand_context(self, text, position):
       # Analyze text in surrounding context
       context_window = text[max(0, position-50):position+50]
       return {
           'context': context_window,
           'relevance': self.calculate_relevance(context_window)
       }
   ```
   **Purpose**: Understand pattern context
   **Importance**: Reduce false positives

#### **5.2.3 Visual Engine Processing**
**Visual Pattern Detection Steps**:

1. **HTML Structure Parsing**:
   ```python
   def parse_html(self, html_content):
       soup = BeautifulSoup(html_content, 'html.parser')
       return {
           'soup': soup,
           'styles': self.extract_styles(soup),
           'layout': self.analyze_layout(soup)
       }
   ```
   **Purpose**: Parse HTML and CSS
   **Importance**: Visual analysis foundation

2. **Contrast Checking**:
   ```python
   def check_contrast(self, soup):
       contrast_issues = []
       
       for element in soup.find_all():
           if element.name in ['button', 'link', 'a']:
               fg_color = self.get_color(element, 'color')
               bg_color = self.get_color(element, 'background-color')
               
               if fg_color and bg_color:
                   ratio = self.calculate_contrast_ratio(fg_color, bg_color)
                   if ratio < 3.0:  # WCAG AA minimum
                       contrast_issues.append({
                           'element': str(element),
                           'ratio': ratio,
                           'severity': 'high'
                       })
       
       return contrast_issues
   ```
   **Purpose**: Check color contrast compliance
   **Importance**: Accessibility and hidden elements

3. **Hidden Element Detection**:
   ```python
   def detect_hidden_elements(self, soup):
       hidden_elements = []
       
       for element in soup.find_all():
           # Check for hidden elements
           styles = element.get('style', '')
           if 'display:none' in styles or 'visibility:hidden' in styles:
               hidden_elements.append({
                   'element': str(element),
                   'type': 'completely_hidden',
                   'severity': 'critical'
               })
           elif self.is_low_contrast_hidden(element):
               hidden_elements.append({
                   'element': str(element),
                   'type': 'contrast_hidden',
                   'severity': 'high'
               })
       
       return hidden_elements
   ```
   **Purpose**: Find intentionally hidden elements
   **Importance**: Deceptive design detection

4. **Layout Analysis**:
   ```python
   def analyze_layout(self, soup):
       layout_issues = []
       
       # Check for misleading hierarchy
       headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
       buttons = soup.find_all('button')
       
       # Check if important buttons are visually de-emphasized
       for button in buttons:
           if self.is_important_button(button) and self.is_de_emphasized(button):
               layout_issues.append({
                   'element': str(button),
                   'issue': 'misleading_hierarchy',
                   'severity': 'medium'
               })
       
       return layout_issues
   ```
   **Purpose**: Analyze visual hierarchy
   **Importance**: Manipulative layout detection

#### **5.2.4 Behavioral Engine Processing**
**Behavioral Pattern Detection Steps**:

1. **Network Analysis**:
   ```python
   def analyze_network_requests(self, har_data):
       tracking_requests = []
       
       for entry in har_data.get('log', {}).get('entries', []):
           url = entry['request']['url']
           
           # Check for tracking domains
           if self.is_tracking_domain(url):
               tracking_requests.append({
                   'url': url,
                   'type': 'tracking_pixel',
                   'severity': 'medium'
               })
           
           # Check for forced redirects
           if self.is_forced_redirect(entry):
               tracking_requests.append({
                   'url': url,
                   'type': 'forced_redirect',
                   'severity': 'high'
               })
       
       return tracking_requests
   ```
   **Purpose**: Analyze HTTP requests and responses
   **Importance**: Tracking and manipulation detection

2. **JavaScript Analysis**:
   ```python
   def analyze_javascript(self, html_content):
       js_issues = []
       
       # Extract JavaScript code
       soup = BeautifulSoup(html_content, 'html.parser')
       scripts = soup.find_all('script')
       
       for script in scripts:
           if script.string:
               # Check for countdown timers
               if self.detect_countdown_reset(script.string):
                   js_issues.append({
                       'type': 'countdown_reset',
                       'code': script.string[:100],
                       'severity': 'high'
                   })
               
               # Check for fake activity
               if self.detect_fake_activity(script.string):
                   js_issues.append({
                       'type': 'fake_activity',
                       'code': script.string[:100],
                       'severity': 'medium'
                   })
       
       return js_issues
   ```
   **Purpose**: Analyze JavaScript for manipulative code
   **Importance**: Dynamic behavior detection

3. **Timing Analysis**:
   ```python
   def analyze_timing_patterns(self, page_data):
       timing_issues = []
       
       # Check for countdown timers
       countdowns = self.find_countdown_elements(page_data)
       for countdown in countdowns:
           if self.is_manipulative_countdown(countdown):
               timing_issues.append({
                   'element': countdown,
                   'type': 'manipulative_countdown',
                   'severity': 'high'
               })
       
       # Check for time pressure
       time_pressure = self.detect_time_pressure(page_data)
       if time_pressure:
           timing_issues.append({
               'type': 'time_pressure',
               'elements': time_pressure,
               'severity': 'medium'
           })
       
       return timing_issues
   ```
   **Purpose**: Analyze time-based manipulation
   **Importance**: Urgency and scarcity detection

### **5.3 Trust Scoring Algorithm Explained**

#### **5.3.1 Score Calculation Logic**
**Trust Score Computation**:

1. **Base Score Initialization**:
   ```python
   def calculate_trust_score(self, findings):
       base_score = 100  # Start with perfect score
       severity_weights = {
           'low': 5,
           'medium': 15,
           'high': 30,
           'critical': 50
       }
   ```
   **Purpose**: Initialize scoring system
   **Importance**: Fair and consistent scoring

2. **Pattern Impact Calculation**:
   ```python
   for finding in findings:
       weight = severity_weights.get(finding['severity'], 10)
       
       # Apply confidence factor
       confidence_factor = finding.get('confidence', 1.0)
       adjusted_weight = weight * confidence_factor
       
       base_score -= adjusted_weight
   ```
   **Purpose**: Calculate impact of each pattern
   **Importance**: Accurate risk assessment

3. **Score Normalization**:
   ```python
   # Ensure score is within bounds
   final_score = max(0, min(100, base_score))
   
   # Apply additional factors
   if self.has_ssl_certificate(url):
       final_score += 5
   if self.is_reputable_domain(url):
       final_score += 10
   if self.has_privacy_policy(url):
       final_score += 5
   
   return final_score
   ```
   **Purpose**: Normalize and adjust score
   **Importance**: Balanced assessment

#### **5.3.2 Severity Classification**
**Pattern Severity Levels**:

1. **Low Severity**:
   - **Definition**: Minor UI issues, slight manipulations
   - **Examples**: Poor contrast, slightly misleading labels
   - **Impact**: Minimal user impact
   - **Weight**: 5 points

2. **Medium Severity**:
   - **Definition**: Noticeable dark patterns, some user impact
   - **Examples**: Fake scarcity, misleading urgency
   - **Impact**: Moderate user impact
   - **Weight**: 15 points

3. **High Severity**:
   - **Definition**: Significant manipulation, major user impact
   - **Examples**: Hidden cancel buttons, forced actions
   - **Impact**: Significant user impact
   - **Weight**: 30 points

4. **Critical Severity**:
   - **Definition**: Severe exploitation, maximum user impact
   - **Examples**: Data theft, financial manipulation
   - **Impact**: Severe user impact
   - **Weight**: 50 points

### **5.4 Real-time Detection Process Explained**

#### **5.4.1 Chrome Extension Flow**
**Real-time Monitoring Implementation**:

1. **Page Monitor Class**:
   ```javascript
   class PageMonitor {
       constructor() {
           this.observer = new MutationObserver(this.handleChanges.bind(this));
           this.scanInterval = 5000; // Scan every 5 seconds
           this.lastScan = Date.now();
       }
       
       startMonitoring() {
           // Monitor DOM changes
           this.observer.observe(document.body, {
               childList: true,
               subtree: true,
               attributes: true,
               attributeFilter: ['style', 'class', 'id']
           });
           
           // Periodic scanning
           setInterval(this.performScan.bind(this), this.scanInterval);
       }
   }
   ```
   **Purpose**: Continuous page monitoring
   **Importance**: Real-time detection

2. **Change Detection**:
   ```javascript
   handleChanges(mutations) {
       let hasSignificantChanges = false;
       
       mutations.forEach(mutation => {
           if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
               hasSignificantChanges = true;
           }
           if (mutation.type === 'attributes') {
               hasSignificantChanges = true;
           }
       });
       
       if (hasSignificantChanges) {
           this.debounceScan();
       }
   }
   ```
   **Purpose**: Detect significant page changes
   **Importance**: Dynamic content detection

3. **Debounced Scanning**:
   ```javascript
   debounceScan() {
       clearTimeout(this.scanTimeout);
       this.scanTimeout = setTimeout(() => {
           this.performScan();
       }, 1000); // Wait 1 second after changes
   }
   ```
   **Purpose**: Prevent excessive scanning
   **Importance**: Performance optimization

4. **Scan Execution**:
   ```javascript
   async performScan() {
       const now = Date.now();
       if (now - this.lastScan < this.scanInterval) {
           return; // Don't scan too frequently
       }
       
       const pageData = {
           url: window.location.href,
           html: document.documentElement.outerHTML,
           timestamp: now,
           title: document.title,
           meta: this.extractMetaTags()
       };
       
       try {
           const results = await this.sendToBackend(pageData);
           this.displayResults(results);
           this.lastScan = now;
       } catch (error) {
           console.error('Scan failed:', error);
       }
   }
   ```
   **Purpose**: Execute pattern detection scan
   **Importance**: Core detection functionality

#### **5.4.2 Alert System**
**User Alert Implementation**:

1. **Alert Manager Class**:
   ```javascript
   class AlertManager {
       constructor() {
           this.activeAlerts = new Map();
           this.maxAlerts = 5;
           this.alertTimeout = 10000; // 10 seconds
       }
       
       displayAlerts(results) {
           results.findings.forEach(finding => {
               if (this.shouldAlert(finding)) {
                   this.createAlert(finding);
               }
           });
       }
   }
   ```
   **Purpose**: Manage user alerts
   **Importance**: User communication

2. **Alert Creation**:
   ```javascript
   createAlert(finding) {
       const alertId = `alert-${Date.now()}-${Math.random()}`;
       
       const alert = document.createElement('div');
       alert.className = `aegis-alert ${finding.severity}`;
       alert.innerHTML = `
           <div class="alert-header">
               <span class="alert-icon">⚠️</span>
               <span class="alert-title">Dark Pattern Detected</span>
               <button class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
           </div>
           <div class="alert-content">
               <h4>${finding.pattern_name}</h4>
               <p>${finding.description}</p>
               <div class="alert-actions">
                   <button onclick="this.showDetails()">Learn More</button>
                   <button onclick="this.dismiss()">Dismiss</button>
               </div>
           </div>
       `;
       
       // Position alert
       alert.style.position = 'fixed';
       alert.style.top = '20px';
       alert.style.right = '20px';
       alert.style.zIndex = '9999';
       
       document.body.appendChild(alert);
       this.activeAlerts.set(alertId, alert);
       
       // Auto-remove after timeout
       setTimeout(() => {
           this.removeAlert(alertId);
       }, this.alertTimeout);
   }
   ```
   **Purpose**: Create user-facing alerts
   **Importance**: User awareness and protection

3. **Alert Management**:
   ```javascript
       removeAlert(alertId) {
           const alert = this.activeAlerts.get(alertId);
           if (alert) {
               alert.remove();
               this.activeAlerts.delete(alertId);
           }
       }
       
       shouldAlert(finding) {
           // Don't alert for low severity patterns
           if (finding.severity === 'low') {
               return false;
           }
           
           // Check if we've already alerted for this pattern
           for (const [id, alert] of this.activeAlerts) {
               if (alert.dataset.patternId === finding.pattern_id) {
                   return false;
               }
           }
           
           // Check alert limit
           if (this.activeAlerts.size >= this.maxAlerts) {
               return false;
           }
           
           return true;
       }
   ```
   **Purpose**: Manage alert lifecycle
   **Importance**: User experience optimization

### **5.5 Data Persistence Flow Explained**

#### **5.5.1 Analysis Storage**
**Data Storage Process**:

1. **Analysis Endpoint**:
   ```python
   @app.route('/api/store-analysis', methods=['POST'])
   @login_required
   def store_analysis():
       data = request.get_json()
       
       # Validate required data
       required_fields = ['url', 'results', 'trust_score']
       for field in required_fields:
           if field not in data:
               return jsonify({'error': f'Missing {field}'}), 400
   ```
   **Purpose**: Store analysis results
   **Importance**: Data persistence and history

2. **Data Preparation**:
   ```python
       # Prepare analysis document
       analysis = {
           'user_id': session.get('user_id'),
           'username': session.get('user'),
           'url': data['url'],
           'scan_results': data['results'],
           'trust_score': data['trust_score'],
           'detected_patterns': data['results'].get('findings', []),
           'analysis_time': data.get('analysis_time', 0),
           'created_at': datetime.utcnow(),
           'status': 'completed',
           'metadata': {
               'user_agent': request.headers.get('User-Agent'),
               'ip_address': request.remote_addr,
               'browser': data.get('browser_info', {}),
               'page_title': data.get('page_title', '')
           }
       }
   ```
   **Purpose**: Format data for storage
   **Importance**: Consistent data structure

3. **Database Storage**:
   ```python
       try:
           # Store in MongoDB
           result = analyses_col.insert_one(analysis)
           
           # Update user statistics
           users_col.update_one(
               {'_id': session.get('user_id')},
               {
                   '$inc': {'total_scans': 1},
                   '$set': {'last_scan': datetime.utcnow()}
               }
           )
           
           return jsonify({
               'success': True,
               'analysis_id': str(result.inserted_id),
               'message': 'Analysis stored successfully'
           })
           
       except Exception as e:
           return jsonify({
               'success': False,
               'error': str(e)
           }), 500
   ```
   **Purpose**: Persist analysis data
   **Importance**: Data reliability and user history

#### **5.5.2 User History Retrieval**
**History Access Process**:

1. **History Endpoint**:
   ```python
   @app.route('/api/get-history')
   @login_required
   def get_history():
       username = session.get('user')
       
       # Pagination parameters
       page = int(request.args.get('page', 1))
       limit = int(request.args.get('limit', 20))
       skip = (page - 1) * limit
   ```
   **Purpose**: Retrieve user's scan history
   **Importance**: User data access and analytics

2. **Query Construction**:
   ```python
       # Build query with filters
       query = {'username': username}
       
       # Apply date filter if provided
       if request.args.get('date_from'):
           query['created_at'] = {'$gte': datetime.fromisoformat(request.args.get('date_from'))}
       
       if request.args.get('date_to'):
           if 'created_at' not in query:
               query['created_at'] = {}
           query['created_at']['$lte'] = datetime.fromisoformat(request.args.get('date_to'))
   ```
   **Purpose**: Build flexible database query
   **Importance**: Advanced filtering capabilities

3. **Data Retrieval**:
   ```python
       try:
           # Execute query with pagination
           history = list(analyses_col.find(query)
               .sort('created_at', -1)
               .skip(skip)
               .limit(limit))
           
           # Get total count for pagination
           total = analyses_col.count_documents(query)
           
           # Convert ObjectId to string for JSON
           for item in history:
               item['_id'] = str(item['_id'])
               # Format dates
               item['created_at'] = item['created_at'].isoformat()
           
           return jsonify({
               'history': history,
               'pagination': {
                   'page': page,
                   'limit': limit,
                   'total': total,
                   'pages': (total + limit - 1) // limit
               }
           })
           
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   ```
   **Purpose**: Retrieve and format history data
   **Importance**: User-friendly data presentation

### **5.6 Admin Dashboard Flow Explained**

#### **5.6.1 System Monitoring**
**Admin Statistics Process**:

1. **Stats Endpoint**:
   ```python
   @app.route('/api/admin/stats')
   @admin_required
   def admin_stats():
       # Get current time for calculations
       now = datetime.utcnow()
       week_ago = now - timedelta(days=7)
       month_ago = now - timedelta(days=30)
   ```
   **Purpose**: Provide system statistics
   **Importance**: Administrative oversight

2. **User Statistics**:
   ```python
       # User metrics
       total_users = users_col.count_documents({})
       active_users = users_col.count_documents({
           'last_login': {'$gte': week_ago}
       })
       new_users = users_col.count_documents({
           'created_at': {'$gte': month_ago}
       })
       
       user_stats = {
           'total': total_users,
           'active': active_users,
           'new': new_users,
           'retention_rate': (active_users / total_users * 100) if total_users > 0 else 0
       }
   ```
   **Purpose**: Calculate user metrics
   **Importance**: User engagement tracking

3. **Analysis Statistics**:
   ```python
       # Analysis metrics
       total_scans = analyses_col.count_documents({})
       recent_scans = analyses_col.count_documents({
           'created_at': {'$gte': week_ago}
       })
       
       # Pattern detection statistics
       pattern_stats = analyses_col.aggregate([
           {'$unwind': '$detected_patterns'},
           {'$group': {
               '_id': '$detected_patterns.pattern_type',
               'count': {'$sum': 1}
           }},
           {'$sort': {'count': -1}}
       ])
       
       # Trust score distribution
       score_distribution = analyses_col.aggregate([
           {'$group': {
               '_id': {
                   '$switch': {
                       'branches': [
                           {'case': {'$lte': ['$trust_score', 25]}, 'then': 'Very Low'},
                           {'case': {'$lte': ['$trust_score', 50]}, 'then': 'Low'},
                           {'case': {'$lte': ['$trust_score', 75]}, 'then': 'Medium'},
                           {'case': {'$lte': ['$trust_score', 90]}, 'then': 'High'},
                           {'case': {'$else': 'then': 'Very High'}
                       ]
                   }
               },
               'count': {'$sum': 1}
           }},
           {'$sort': {'_id': 1}}
       ])
   ```
   **Purpose**: Analyze scan patterns and trends
   **Importance**: System effectiveness metrics

4. **System Health**:
   ```python
       # System health metrics
       system_health = {
           'database': 'CONNECTED' if db else 'OFFLINE',
           'engines': ['NLP', 'VISUAL', 'BEHAVIORAL'],
           'uptime': get_system_uptime(),
           'memory_usage': get_memory_usage(),
           'cpu_usage': get_cpu_usage(),
           'disk_usage': get_disk_usage()
       }
       
       return jsonify({
           'user_stats': user_stats,
           'analysis_stats': {
               'total': total_scans,
               'recent': recent_scans,
               'pattern_distribution': list(pattern_stats),
               'score_distribution': list(score_distribution)
           },
           'system_health': system_health,
           'timestamp': now.isoformat()
       })
   ```
   **Purpose**: Monitor system health and performance
   **Importance**: System reliability and maintenance

#### **5.6.2 User Management**
**User Administration Process**:

1. **Users Endpoint**:
   ```python
   @app.route('/api/admin/users')
   @admin_required
   def admin_users():
       # Pagination and filtering
       page = int(request.args.get('page', 1))
       limit = int(request.args.get('limit', 50))
       skip = (page - 1) * limit
       
       # Search filter
       search = request.args.get('search', '')
       query = {}
       if search:
           query['$or'] = [
               {'username': {'$regex': search, '$options': 'i'}},
               {'email': {'$regex': search, '$options': 'i'}}
           ]
   ```
   **Purpose**: Manage user accounts
   **Importance**: User administration and security

2. **User Data Retrieval**:
   ```python
       try:
           # Get users with pagination
           users = list(users_col.find(query, {
               'username': 1,
               'email': 1,
               'role': 1,
               'created_at': 1,
               'last_login': 1,
               'is_active': 1,
               'total_scans': 1
           })
           .sort('created_at', -1)
           .skip(skip)
           .limit(limit))
           
           # Convert ObjectId to string
           for user in users:
               user['_id'] = str(user['_id'])
               user['created_at'] = user['created_at'].isoformat()
               if user.get('last_login'):
                   user['last_login'] = user['last_login'].isoformat()
           
           # Get total count
           total = users_col.count_documents(query)
           
           return jsonify({
               'users': users,
               'pagination': {
                   'page': page,
                   'limit': limit,
                   'total': total,
                   'pages': (total + limit - 1) // limit
               }
           })
           
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   ```
   **Purpose**: Retrieve and format user data
   **Importance**: Admin interface functionality

3. **User Actions**:
   ```python
   @app.route('/api/admin/update-role/<user_id>', methods=['POST'])
   @admin_required
   def update_user_role(user_id):
       data = request.get_json()
       new_role = data.get('role')
       
       if new_role not in ['user', 'admin']:
           return jsonify({'error': 'Invalid role'}), 400
       
       try:
           # Update user role
           result = users_col.update_one(
               {'_id': ObjectId(user_id)},
               {'$set': {'role': new_role, 'updated_at': datetime.utcnow()}}
           )
           
           if result.matched_count == 0:
               return jsonify({'error': 'User not found'}), 404
           
           # Log the action
           log_admin_action(session.get('admin_id'), 'update_role', user_id, {
               'old_role': data.get('old_role'),
               'new_role': new_role
           })
           
           return jsonify({
               'success': True,
               'message': f'User role updated to {new_role}'
           })
           
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   ```
   **Purpose**: Perform user management actions
   **Importance**: System administration and security

---

## Conclusion

This detailed explanation covers every aspect of the Aegis Pro documentation, providing comprehensive understanding of:

1. **Project Synopsis**: Vision, features, and target users
2. **SRS**: Detailed functional and non-functional requirements
3. **ER Diagram**: Database structure and relationships
4. **System Architecture**: Component design and interactions
5. **Technical Flow**: Step-by-step operational processes

Each section serves specific stakeholders:
- **Developers**: Technical specifications and implementation details
- **Administrators**: System management and monitoring
- **Users**: Feature understanding and usage guidance
- **Stakeholders**: Project scope and capabilities

The documentation provides a complete foundation for understanding, implementing, and maintaining the Aegis Pro dark pattern detection system.

---

**Document Version**: 1.0.0  
**Last Updated**: April 22, 2026  
**Purpose**: Comprehensive Documentation Explanation
