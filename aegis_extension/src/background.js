// Aegis Pro Background Service Worker
// Coordinates between content scripts, backend, and side panel

class AegisBackground {
    constructor() {
        this.currentAnalysis = null;
        this.ghostWriterEnabled = false;
        this.init();
    }

    init() {
        // Listen for tab navigation
        chrome.webNavigation.onCompleted.addListener((details) => {
            if (details.frameId === 0) { // Main frame only
                this.analyzePage(details.tabId, details.url);
            }
        });

        // Listen for messages from content script and popup
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // Keep message channel open for async response
        });

        // Listen for extension icon click
        chrome.action.onClicked.addListener((tab) => {
            this.openSidePanel(tab.id);
        });
    }

    async handleMessage(message, sender, sendResponse) {
        try {
            switch (message.type) {
                case 'ANALYZE_PAGE':
                    await this.analyzePage(sender.tab.id, sender.tab.url);
                    sendResponse({ success: true });
                    break;

                case 'GET_CURRENT_ANALYSIS':
                    sendResponse({ analysis: this.currentAnalysis });
                    break;

                case 'TOGGLE_GHOST_WRITER':
                    this.ghostWriterEnabled = message.enabled;
                    this.broadcastToContentScript(sender.tab.id, {
                        type: 'GHOST_WRITER_TOGGLE',
                        enabled: this.ghostWriterEnabled
                    });
                    sendResponse({ success: true, enabled: this.ghostWriterEnabled });
                    break;

                case 'CAPTURE_SCREENSHOT':
                    const screenshot = await this.captureScreenshot(sender.tab.id);
                    sendResponse({ screenshot });
                    break;

                case 'GET_HAR_DATA':
                    const harData = await this.captureHarData(sender.tab.id);
                    sendResponse({ har: harData });
                    break;

                default:
                    sendResponse({ error: 'Unknown message type' });
            }
        } catch (error) {
            console.error('Background script error:', error);
            sendResponse({ error: error.message });
        }
    }

    async analyzePage(tabId, url) {
        try {
            console.log('Aegis Pro: Analyzing page', url);

            // Get HTML content from content script
            const htmlContent = await this.sendMessageToContentScript(tabId, {
                type: 'GET_HTML_CONTENT'
            });

            // Capture screenshot
            const screenshot = await this.captureScreenshot(tabId);

            // Capture HAR data
            const harData = await this.captureHarData(tabId);

            // Send to backend for analysis
            const analysis = await this.sendToBackend({
                url: url,
                html_content: htmlContent,
                screenshot_b64: screenshot,
                har_data: harData
            });

            this.currentAnalysis = analysis;

            // Broadcast results to side panel and content script
            this.broadcastToContentScript(tabId, {
                type: 'ANALYSIS_COMPLETE',
                analysis: analysis
            });

            this.broadcastToSidePanel({
                type: 'ANALYSIS_COMPLETE',
                analysis: analysis
            });

            return analysis;

        } catch (error) {
            console.error('Analysis failed:', error);
            this.broadcastToSidePanel({
                type: 'ANALYSIS_ERROR',
                error: error.message
            });
        }
    }

    async captureScreenshot(tabId) {
        return new Promise((resolve) => {
            chrome.tabs.captureVisibleTab(null, { format: 'png' }, (dataUrl) => {
                resolve(dataUrl);
            });
        });
    }

    async captureHarData(tabId) {
        return new Promise((resolve) => {
            chrome.debugger.attach({ tabId }, '1.3', () => {
                chrome.debugger.sendCommand({ tabId }, 'Network.enable', {}, () => {
                    // Wait a bit for network data
                    setTimeout(() => {
                        chrome.debugger.sendCommand({ tabId }, 'Network.getResponseBody', {}, (result) => {
                            chrome.debugger.detach({ tabId });
                            resolve({ entries: [] }); // Simplified HAR data
                        });
                    }, 2000);
                });
            });
        });
    }

    async sendToBackend(data) {
        const response = await fetch('http://localhost:5000/api/tri-engine-analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        return await response.json();
    }

    sendMessageToContentScript(tabId, message) {
        return new Promise((resolve) => {
            chrome.tabs.sendMessage(tabId, message, (response) => {
                resolve(response?.data);
            });
        });
    }

    broadcastToContentScript(tabId, message) {
        chrome.tabs.sendMessage(tabId, message);
    }

    broadcastToSidePanel(message) {
        chrome.runtime.sendMessage(message);
    }

    openSidePanel(tabId) {
        chrome.sidePanel.open({ tabId });
    }
}

// Initialize the background service
const aegisBackground = new AegisBackground();
