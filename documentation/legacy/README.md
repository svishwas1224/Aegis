# Aegis Pro - Advanced Dark Pattern Detection System

A comprehensive dark pattern detection system with tri-engine architecture combining NLP, Computer Vision, and Network Forensics analysis.

## 🛡️ Features

### Tri-Engine Architecture
- **NLP Engine**: Analyzes text content for manipulative language patterns
- **Visual Engine**: Detects accessibility issues and visual dark patterns
- **Behavioral Engine**: Analyzes network behavior and user interaction patterns

### Chrome Extension
- **Real-time Analysis**: Scans pages as you browse
- **Ghost-Writer Mode**: Automatically fixes detected dark patterns
- **Visual Overlays**: Highlights problematic areas on web pages
- **Side Panel**: Comprehensive analysis dashboard

### AI-Powered Insights
- **Local AI**: Integration with Ollama for privacy-first analysis
- **Smart Recommendations**: Context-aware remediation suggestions
- **Risk Assessment**: Comprehensive trust scoring system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- Node.js 16+
- Ollama (optional, for AI features)

### Installation

1. **Clone and Setup Backend**
```bash
git clone <repository>
cd newanti
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your MongoDB URI and other settings
```

3. **Start Backend**
```bash
python app.py
```

4. **Setup Chrome Extension**
```bash
cd aegis_extension
npm install
npm run build
```

5. **Load Extension in Chrome**
- Open `chrome://extensions/`
- Enable Developer Mode
- Click "Load Unpacked"
- Select `aegis_extension/dist` folder

### Ollama Setup (Optional)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended model
ollama pull qwen2.5:7b

# Start Ollama
ollama serve
```

## 📊 Architecture

### Backend Components
- **Flask API**: RESTful services for analysis
- **Tri-Engine Analyzer**: Coordinates multiple analysis engines
- **MongoDB**: Stores scan results and user data
- **AI Integration**: Local LLM for enhanced insights

### Chrome Extension Components
- **Background Script**: Service worker for page analysis
- **Content Script**: Injects into pages for data capture
- **Side Panel**: React-based analysis dashboard
- **Popup**: Quick access to features

### Analysis Engines

#### NLP Engine
- Dark pattern detection using regex and spaCy
- Supports multiple pattern types:
  - Confirm shaming
  - Urgency tactics
  - Scarcity indicators
  - Social proof manipulation
  - Misdirection
  - Forced actions

#### Visual Engine
- Computer vision analysis using OpenCV
- Detects:
  - Low contrast issues (WCAG compliance)
  - Small touch targets
  - Hidden elements
  - Deceptive positioning

#### Behavioral Engine
- Network forensics using HAR analysis
- Identifies:
  - Fake countdown timers
  - Excessive tracking
  - Redirect chains
  - Dynamic price changes

## 🔧 Configuration

### Environment Variables
```env
MONGO_URI=mongodb://localhost:27017
OLLAMA_URL=http://localhost:11434/api/generate
MODEL_NAME=qwen2.5:7b
APP_SESSION_KEY=your-secret-key
SMTP_EMAIL=your-email@gmail.com
SMTP_APP_PASSWORD=your-app-password
```

### Extension Permissions
The Chrome Extension requires:
- `activeTab` - Analyze current page
- `scripting` - Inject content scripts
- `storage` - Save settings and data
- `declarativeNetRequest` - Network analysis
- `sidePanel` - Display analysis panel

## 📈 API Endpoints

### Core Analysis
- `POST /api/tri-engine-analyze` - Comprehensive analysis
- `POST /api/analyze` - Legacy URL analysis
- `POST /api/analyze-text` - Text analysis
- `POST /api/ext-analyze` - Extension analysis

### User Management
- `POST /api/signup` - User registration
- `POST /api/login` - User authentication
- `POST /api/logout` - User logout
- `GET /api/dashboard` - User dashboard data

### Utilities
- `GET /api/health` - System health check
- `GET /api/get-history` - Scan history
- `POST /api/clear-history` - Clear history

## 🧪 Testing

### Run Tests
```bash
# Backend tests
python -m pytest tests/

# Extension tests
cd aegis_extension
npm test
```

### Test Cases
The system includes comprehensive test cases covering:
- Linguistic pattern detection
- Visual analysis accuracy
- Behavioral forensics
- Integration scenarios
- Privacy and security

## 🔒 Privacy & Security

### Data Protection
- **Local Processing**: AI analysis runs locally
- **No Data Leakage**: User data never leaves the system
- **Secure Storage**: Encrypted database connections
- **Privacy First**: Minimal data collection

### Security Features
- Session management
- CSRF protection
- Input validation
- Secure headers
- Rate limiting

## 📝 Documentation

### Code Structure
```
newanti/
├── engines/              # Tri-engine analysis modules
│   ├── linguistic_engine.py
│   ├── visual_engine.py
│   ├── behavioral_engine.py
│   └── tri_engine_analyzer.py
├── aegis_extension/       # Chrome extension
│   ├── src/
│   │   ├── background.js
│   │   ├── content.js
│   │   └── panel/
│   └── manifest.json
├── trust_pipeline/        # Legacy analysis system
├── frontend/             # Web frontend
├── app.py               # Flask backend
└── requirements.txt      # Python dependencies
```

### Database Schema
- **scans**: Individual scan results
- **sites**: Domain-level statistics
- **users**: User accounts
- **analyses**: Legacy analysis records

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting guide
2. Review existing issues
3. Create a new issue with details
4. Include system information and error logs

## 🔮 Roadmap

### Upcoming Features
- [ ] Advanced machine learning models
- [ ] Mobile browser support
- [ ] Team collaboration features
- [ ] Advanced reporting dashboard
- [ ] API for third-party integration

### Improvements
- [ ] Enhanced pattern recognition
- [ ] Real-time collaboration
- [ ] Performance optimizations
- [ ] Additional language support

---

**Build with purpose. Protect with precision.** 🛡️
