# Aegis Pro Chrome Extension - Free Installation Guide

## Quick Start (Free Installation)

### Step 1: Download the Extension
The extension package is ready at: `aegis_pro_extension_v1.0.0.zip`

### Step 2: Install in Chrome (Developer Mode)

1. **Open Chrome Extensions Page**
   - Type `chrome://extensions` in Chrome address bar
   - Press Enter

2. **Enable Developer Mode**
   - Look for "Developer mode" toggle in top-right corner
   - Click to enable it

3. **Load the Extension**
   - Click the "Load unpacked" button
   - Navigate to and select the `aegis_extension` folder
   - Click "Select Folder"

4. **Verify Installation**
   - Look for Aegis Pro icon in Chrome toolbar
   - Click the icon to test the extension

## Alternative Installation Methods

### Method A: Extract from ZIP
1. Download `aegis_pro_extension_v1.0.0.zip`
2. Extract to a folder (e.g., `aegis_extension`)
3. Follow steps above using the extracted folder

### Method B: Clone from Repository
```bash
git clone [repository-url]
cd aegis_extension
# Then load in Chrome Developer Mode
```

## Testing the Extension

### Basic Test
1. Visit any website (e.g., amazon.com, booking.com)
2. Click Aegis Pro icon in toolbar
3. Click "Scan Page"
4. View trust score and results

### Advanced Test
1. Click "View Details" to open side panel
2. Enable "Ghost-Writer Mode" in settings
3. Refresh page to see remediation in action

## Required Backend (Optional)

For full functionality, start the backend server:

```bash
cd newanti
python app.py
```

The extension will automatically connect to `http://localhost:5000`

## Troubleshooting

### Extension Not Loading
- Make sure Developer Mode is enabled
- Check folder path is correct
- Restart Chrome if needed

### Scanning Issues
- Refresh the webpage
- Check if backend server is running
- Look for browser console errors

## File Structure (What's Included)

```
aegis_extension/
  manifest.json           # Extension configuration
  src/
    background.js          # Service worker
    content.js            # Page analysis
    ghost-writer.js       # Active remediation
    popup/
      popup.html         # Extension popup
      popup.js           # Popup logic
    panel/
      panel.html         # Analysis dashboard
      components/        # React components
  public/icons/           # Extension icons
  README.md              # Documentation
```

## Features Included

### Core Detection
- Confirm shaming patterns
- Urgency and scarcity tactics
- Social proof manipulation
- Visual hierarchy issues
- Hidden elements
- Pre-selected checkboxes
- Low contrast buttons

### Advanced Features
- Real-time scanning
- Trust scoring (0-100)
- Side panel dashboard
- Ghost-Writer remediation
- Scan history
- Pattern evidence logging

## Privacy & Permissions

The extension requires:
- `activeTab`: Scan current webpage
- `scripting`: Inject analysis scripts
- `storage`: Save user preferences
- `sidePanel`: Show analysis dashboard

**No personal data is collected or transmitted.**

## Support

- Check the README.md in the extension folder
- Report issues on GitHub
- Join community discussions

---

**This is 100% FREE. No payment required for any features.**
