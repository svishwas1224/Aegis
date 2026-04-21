// Aegis Pro Popup Script
class AegisProPopup {
    constructor() {
        this.currentTab = null;
        this.scanResults = null;
        this.init();
    }

    async init() {
        // Get current active tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        this.currentTab = tab;

        // Setup event listeners
        this.setupEventListeners();

        // Scan the current page
        await this.scanCurrentPage();
    }

    setupEventListeners() {
        document.getElementById('view-details').addEventListener('click', () => {
            this.openSidePanel();
        });

        document.getElementById('scan-page').addEventListener('click', () => {
            this.scanCurrentPage();
        });
    }

    async scanCurrentPage() {
        try {
            // Show loading state
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('results').style.display = 'none';

            // Send scan request to content script
            const response = await chrome.tabs.sendMessage(this.currentTab.id, { 
                action: 'scan_page' 
            });

            if (response && response.success) {
                this.displayResults(response.data);
            } else {
                throw new Error('Scan failed');
            }

        } catch (error) {
            console.error('Scan error:', error);
            this.showError();
        }
    }

    displayResults(results) {
        this.scanResults = results;
        
        // Hide loading, show results
        document.getElementById('loading').style.display = 'none';
        document.getElementById('results').style.display = 'block';

        // Update trust score
        const score = results.trust_score || 100;
        document.getElementById('score-value').textContent = Math.round(score);
        
        // Update progress bar
        const progressFill = document.getElementById('progress-fill');
        progressFill.style.width = `${score}%`;
        
        // Update risk indicator and color
        const riskIndicator = document.getElementById('risk-indicator');
        const findingsText = document.getElementById('findings-text');
        
        if (score >= 75) {
            riskIndicator.textContent = ' Safe';
            progressFill.style.background = '#4ade80';
            findingsText.textContent = `${results.findings?.length || 0} issues found`;
        } else if (score >= 45) {
            riskIndicator.textContent = 'Caution';
            progressFill.style.background = '#f59e0b';
            findingsText.textContent = `${results.findings?.length || 0} issues detected`;
        } else {
            riskIndicator.textContent = 'Danger';
            progressFill.style.background = '#ef4444';
            findingsText.textContent = `${results.findings?.length || 0} dangerous patterns`;
        }
    }

    showError() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
        document.getElementById('results').style.display = 'none';
    }

    async openSidePanel() {
        try {
            // Open side panel
            await chrome.sidePanel.open({ windowId: this.currentTab.windowId });
            
            // Send data to side panel
            if (this.scanResults) {
                chrome.runtime.sendMessage({
                    action: 'update_panel_data',
                    data: this.scanResults
                });
            }
        } catch (error) {
            console.error('Failed to open side panel:', error);
            // Fallback: open new tab with dashboard
            chrome.tabs.create({
                url: 'src/panel/panel.html'
            });
        }
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AegisProPopup();
});

// Handle messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'scan_complete') {
        // Update popup with new scan results
        const popup = new AegisProPopup();
        popup.displayResults(message.data);
    }
});
