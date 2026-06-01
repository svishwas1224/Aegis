# Aegis Dark-Pattern Detector

## Advanced Dark Pattern Detection System with Tri-Engine Analysis

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.2-green.svg)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-19.2.0-blue.svg)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com)

---

## 🎯 Overview

**Aegis Dark-Pattern Detector** is a sophisticated, real-time dark pattern detection system that shields users from manipulative web design tactics. The system employs a powerful tri-engine architecture combining Natural Language Processing (NLP), Visual HTML/CSS analysis, and Behavioral HTTP Archive (HAR) analysis, augmented by a custom-trained scikit-learn machine learning model, to identify over 25 distinct types of dark patterns, including crawler traps.

### 🚀 Key Features

- **Tri-Engine Analysis**: Combines NLP, Visual, and Behavioral analysis for comprehensive detection
- **25+ Dark Pattern Types Detected**: Including urgency, scarcity, hidden costs, subscription traps, crawler traps, and more
- **Trust Scoring**: Quantified 0-100 trust score with risk levels (Low/Medium/High)
- **JavaScript Support**: Analyzes modern SPAs using Playwright
- **User Authentication System**: Secure login/signup with password hashing and OTP verification
- **Dual Dashboards**: Client dashboard and Admin dashboard for comprehensive management
- **Real-Time Analysis**: Live feedback as you browse
- **MongoDB Atlas Integration**: Cloud database for scan history and user data
- **Ollama AI Integration**: Optional AI-powered insights (if configured)

---

## 🛠️ Technology Stack

### Backend

- **Python 3.10+**: Modern Python with advanced features
- **Flask 3.0.2**: Lightweight, flexible web framework
- **MongoDB Atlas**: Cloud-hosted NoSQL database
- **Scikit-learn 1.8.0**: Machine learning model training and inference
- **Playwright for Python**: Web scraping with JavaScript rendering
- **spaCy**: Natural language processing
- **Beautiful Soup 4.12.3**: HTML parsing
- **Werkzeug Security**: Password hashing and security

### Frontend

- **React 19.2.0**: Modern UI library
- **Vite 7.3.1**: Fast build tool and development server
- **Lucide React 0.577.0**: Beautiful, consistent icon library
- **Recharts 3.8.0**: Interactive data visualization
- **React Router DOM 7.13.1**: Routing
- **Axios 1.13.6**: HTTP client for API communication
- **SweetAlert2**: Beautiful alerts
- **js-cookie**: Cookie management

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- MongoDB Atlas account (or local MongoDB)
- (Optional) Ollama running locally for AI insights

### Installation & Setup

1. **Clone Repository**

   ```bash
   git clone https://github.com/svishwas1224/newanti.git
   cd newanti
   ```

2. **Backend Setup**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Install Playwright browsers
   playwright install chromium
   ```

3. **Frontend Setup**

   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:

   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
   SECRET_KEY=your-secret-key-here
   APP_SESSION_KEY=your-session-key-here
   OLLAMA_URL=http://localhost:11434/api/generate
   MODEL_NAME=qwen2.5:7b
   SMTP_EMAIL=your-email@gmail.com
   SMTP_APP_PASSWORD=your-gmail-app-password
   ```

5. **Train ML Model** (if not already trained)

   ```bash
   python engines/train_ml_model.py
   ```

6. **Run the Application**

   ```bash
   # Option 1: Run everything together (from project root)
   npm run dev-all

   # Option 2: Run separately
   # Backend (from project root)
   python app.py

   # Admin Dashboard (from project root)
   npm run frontend-admin

   # Client Dashboard (from project root)
   npm run frontend-client
   ```

7. **Access the Application**
   - Admin Dashboard: http://localhost:5173
   - Client Dashboard: http://localhost:5174
   - Backend API: http://localhost:5000

---

## 🎯 Core Capabilities

### Dark Pattern Detection

- **Linguistic Patterns**: Confirm shaming, urgency, scarcity, manipulative language
- **Visual Patterns**: Hidden elements, deceptive positioning, visual hierarchy manipulation
- **Behavioral Patterns**: Forced actions, countdown manipulation, fake notifications
- **Advanced Patterns**: Subscription traps, price flickering, cookie walls, drip pricing
- **Crawler Traps**: Honeypot links, infinite URL loops, hidden form fields

### User Features

- **Text Analysis**: Analyze raw text for dark patterns
- **URL Analysis**: Scrape and analyze live websites
- **Real-Time Feedback**: Live analysis as you type
- **Trust Score**: 0-100 trust score with risk levels
- **Detailed Findings**: Pattern explanations and remediation suggestions
- **Scan History**: View your past analyses
- **Profile Management**: Update username and password
- **Password Reset**: OTP-based password reset via email

### Admin Features

- **Secure Admin Login**: Separate admin authentication
- **User Management**: View all registered users
- **Analytics Dashboard**: Comprehensive usage statistics
- **Scan History**: View all scans across all users
- **Real-Time Stats**: Hourly, weekly, and monthly scan metrics

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      React Frontends                        │
│  ┌────────────────────────┐  ┌───────────────────────────┐  │
│  │  Admin Dashboard       │  │  Client Dashboard         │  │
│  │  (localhost:5173)      │  │  (localhost:5174)         │  │
│  └─────────────┬──────────┘  └───────────────┬───────────┘  │
└────────────────┼──────────────────────────────┼──────────────┘
                 │                              │
                 └───────────┬──────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend API                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Authentication & Authorization (login/signup/OTP)      │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Tri-Engine Analyzer                         │  │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────────────┐       │  │
│  │ │ NLP      │ │ Visual   │ │ Behavioral/HAR   │       │  │
│  │ │ Engine   │ │ Engine   │ │ Engine           │       │  │
│  │ └──────────┘ └──────────┘ └──────────────────┘       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      MongoDB Databases                       │
│  ┌──────────────────┐ ┌──────────────────┐ ┌───────────────┐ │
│  │ dark-pattern-    │ │ dark-pattern-    │ │ aegis-pro     │ │
│  │ users            │ │ admin            │ │               │ │
│  └──────────────────┘ └──────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Documentation

### API Endpoints

- **Authentication**:
  - `POST /api/signup`: User registration
  - `POST /api/login`: User login
  - `POST /api/forgot-password`: Request password reset OTP
  - `POST /api/verify-otp`: Verify OTP
  - `POST /api/reset-password`: Reset password
  - `GET /api/logout`: User logout
  - `POST /api/admin/login`: Admin login

- **Analysis**:
  - `POST /api/analyze`: Analyze URL
  - `POST /api/analyze-text`: Analyze text
  - `POST /api/tri-engine-analyze`: Comprehensive tri-engine analysis
  - `POST /api/ext-analyze`: Chrome extension analysis
  - `POST /api/scrape-details`: Scrape website details

- **User Dashboard**:
  - `GET /api/dashboard`: User dashboard data
  - `GET /api/get-history`: User scan history
  - `POST /api/clear-history`: Clear user history
  - `POST /api/update-profile`: Update user profile
  - `GET /api/compliance-score`: User compliance score

- **Admin Dashboard**:
  - `GET /api/admin/stats`: Admin statistics
  - (And more admin endpoints)

- **System**:
  - `GET /api/health`: System health check
  - `GET /api/verify-session`: Verify user session
  - `POST /api/detect-device`: Detect user device

---

## 🔒 Security & Privacy

### Privacy

- **No Personal Data Sharing**: No data shared with third parties
- **Local Analysis Option**: All core analysis happens locally
- **Hashed Passwords**: Passwords stored using Werkzeug's secure hashing
- **Session Management**: Secure session cookies with SameSite=Lax

### Security

- **Secure Authentication**: Password hashing and session management
- **Input Validation**: Comprehensive validation and sanitization
- **CORS Configuration**: Strict allowed origins
- **Environment Variables**: Sensitive data stored in environment variables
- **Audit Logging**: Local audit logs for critical operations

---

## 📈 Performance Metrics

### System Performance

- **Analysis Speed**: ~2-5 seconds per URL analysis
- **Concurrent Users**: 100+ simultaneous users supported
- **Memory Usage**: Optimized for efficient operation
- **Database Performance**: Indexed collections for fast queries

### Detection Metrics

- **Pattern Coverage**: 25+ distinct dark pattern types
- **False Positive Rate**: Low false positives with ML enhancement
- **Scraping Success Rate**: High success rate with Playwright fallback

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎉 Acknowledgments

### Core Technologies

- **Flask**: Web framework
- **React 19**: UI library
- **Vite**: Build tool
- **MongoDB**: Database
- **Playwright**: Web scraping
- **spaCy**: NLP
- **Scikit-learn**: Machine learning
- **Lucide React**: Icons
- **Recharts**: Charts

---

## 📞 Contact

- **Project Repository**: https://github.com/svishwas1224/newanti
- **Issues**: https://github.com/svishwas1224/newanti/issues

---

## 🔮 Future Scope

- Browser extension for Chrome, Firefox, Edge
- Multi-language support
- Mobile applications
- Advanced crawler trap detection
- Real-time browser monitoring
- More ML model improvements
- Batch analysis
- Public API access
- Advanced reporting

---

Built with ❤️ for a safer digital world!

**Aegis Dark-Pattern Detector** - Protecting Users, Empowering Choices, Creating Trust 🛡️
