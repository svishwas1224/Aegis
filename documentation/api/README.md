# Aegis Pro Chrome Extension - Free Installation Guide

## Overview
Aegis Pro is an advanced dark pattern detection Chrome extension that uses tri-engine analysis (NLP, Visual, Behavioral) to protect users from manipulative design patterns.

## Free Installation Methods

### Method 1: Developer Mode Installation (Recommended)

#### Step 1: Enable Developer Mode in Chrome
1. Open Chrome browser
2. Navigate to `chrome://extensions/`
3. Toggle on "Developer mode" (top right corner)
4. Developer options will appear

#### Step 2: Load the Extension
1. Click the "Load unpacked" button
2. Navigate to the `aegis_extension` folder
3. Select the folder and click "Select Folder"
4. Aegis Pro will appear in your extensions list

#### Step 3: Verify Installation
1. Look for the Aegis Pro icon in your toolbar
2. Click the icon to open the popup
3. Visit any website and click "Scan Page" to test

### Method 2: Direct Download Installation

#### Step 1: Download Extension Files
1. Download the extension ZIP file from GitHub Releases
2. Extract the ZIP file to a folder on your computer

#### Step 2: Install in Developer Mode
1. Follow Method 1 steps to enable Developer Mode
2. Use "Load unpacked" to select the extracted folder

### Method 3: GitHub Pages Installation

#### Step 1: Visit Installation Page
1. Go to `https://[username].github.io/aegis-pro/`
2. Click the "Install Aegis Pro" button
3. Follow the automatic installation prompts

## Extension Features

### Core Functionality
- **Real-time Scanning**: Analyzes web pages for dark patterns
- **Trust Score**: Provides a 0-100 trust score for websites
- **Pattern Detection**: Identifies 15+ types of dark patterns
- **Side Panel**: Detailed analysis dashboard
- **Ghost-Writer Mode**: Active remediation of detected patterns

### Detected Pattern Types
- Confirm Shaming
- Urgency & Scarcity
- Social Proof Manipulation
- Visual Hierarchy Issues
- Hidden Elements
- Pre-selected Checkboxes
- Low Contrast Buttons
- Tracking & Privacy Issues
- Subscription Traps

## Usage Instructions

### Basic Usage
1. Navigate to any website
2. Click the Aegis Pro icon in your toolbar
3. View the trust score and scan results
4. Click "View Details" for comprehensive analysis

### Advanced Features
- **Side Panel**: Click "View Details" to open the analysis dashboard
- **Ghost-Writer Mode**: Enable active remediation in settings
- **History**: View scan history across websites
- **Settings**: Configure detection sensitivity

## Configuration

### Backend Connection
The extension connects to a local backend server for advanced analysis:

1. Start the backend server:
   ```bash
   cd newanti
   python app.py
   ```

2. The extension will automatically connect to `http://localhost:5000`

### Local Mode
If the backend is unavailable, the extension operates in local mode with basic pattern detection.

## Troubleshooting

### Common Issues

#### Extension Not Loading
- Ensure Developer Mode is enabled
- Check that the folder path is correct
- Verify all required files are present

#### Scanning Not Working
- Check if backend server is running
- Refresh the webpage and try again
- Check browser console for errors

#### Permissions Issues
- Make sure `<all_urls>` permission is granted
- Check that scripting permission is enabled
- Restart Chrome if needed

### Error Messages

#### "Unable to scan page"
- Refresh the webpage
- Check internet connection
- Verify backend server is running

#### "Backend connection failed"
- Extension will work in local mode
- Start the backend server for full functionality

## File Structure

```
aegis_extension/
  manifest.json          # Extension manifest
  package.json           # Build configuration
  src/
    background.js         # Service worker
    content.js           # Content script
    ghost-writer.js      # Active remediation
    popup/
      popup.html        # Extension popup
      popup.js          # Popup logic
    panel/
      panel.html        # Side panel
      components/       # React components
    styles/
      panel.css         # Styling
  public/
    icons/
      icon16.png       # 16x16 icon
      icon32.png       # 32x32 icon
      icon48.png       # 48x48 icon
      icon128.png      # 128x128 icon
```

## Development

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   cd aegis_extension
   npm install
   ```
3. Build the extension:
   ```bash
   npm run build
   ```

### Testing
1. Load the extension in Developer Mode
2. Visit test websites with known dark patterns
3. Verify detection and remediation work correctly

## Privacy & Security

### Data Collection
- No personal data is collected
- Scans are performed locally
- Optional backend connection for enhanced analysis

### Permissions Explained
- `activeTab`: Scan current webpage
- `scripting`: Inject content scripts
- `storage`: Save user preferences
- `sidePanel`: Show analysis dashboard
- `tabs`: Get current tab information

## Support

### Getting Help
- Check the troubleshooting section
- Report issues on GitHub
- Join our community discussions

### Contributing
- Fork the repository
- Create a feature branch
- Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Updates

### Automatic Updates
- Chrome will check for updates periodically
- Manual updates available from GitHub Releases

### Version History
- v1.0.0: Initial release with core functionality
- Future versions will include additional pattern types and features

---

**Note**: This is a free and open-source extension. No payment is required for installation or use.
