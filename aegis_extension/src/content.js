// Aegis Pro Content Script
// Runs in the context of web pages to capture data and apply remediations

class AegisContentScript {
    constructor() {
        this.ghostWriterEnabled = false;
        this.currentAnalysis = null;
        this.domObserver = null;
        this.init();
    }

    init() {
        console.log('Aegis Pro Content Script initialized');

        // Set up DOM observer for dynamic content
        this.setupDOMObserver();

        // Listen for messages from background script
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true;
        });

        // Send initial page content
        this.sendPageContent();
    }

    setupDOMObserver() {
        this.domObserver = new MutationObserver((mutations) => {
            if (this.ghostWriterEnabled && this.currentAnalysis) {
                this.applyGhostWriterChanges();
            }
        });

        this.domObserver.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            characterData: true
        });
    }

    handleMessage(message, sender, sendResponse) {
        try {
            switch (message.type) {
                case 'GET_HTML_CONTENT':
                    const htmlContent = this.getHTMLContent();
                    sendResponse({ data: htmlContent });
                    break;

                case 'ANALYSIS_COMPLETE':
                    this.currentAnalysis = message.analysis;
                    this.highlightDarkPatterns();
                    if (this.ghostWriterEnabled) {
                        this.applyGhostWriterChanges();
                    }
                    sendResponse({ success: true });
                    break;

                case 'GHOST_WRITER_TOGGLE':
                    this.ghostWriterEnabled = message.enabled;
                    if (message.enabled) {
                        this.applyGhostWriterChanges();
                    } else {
                        this.removeGhostWriterChanges();
                    }
                    sendResponse({ success: true });
                    break;

                case 'HIGHLIGHT_PATTERNS':
                    this.highlightDarkPatterns();
                    sendResponse({ success: true });
                    break;

                case 'REMOVE_HIGHLIGHTS':
                    this.removeHighlights();
                    sendResponse({ success: true });
                    break;

                default:
                    sendResponse({ error: 'Unknown message type' });
            }
        } catch (error) {
            console.error('Content script error:', error);
            sendResponse({ error: error.message });
        }
    }

    getHTMLContent() {
        return document.documentElement.outerHTML;
    }

    sendPageContent() {
        const htmlContent = this.getHTMLContent();
        chrome.runtime.sendMessage({
            type: 'PAGE_CONTENT_READY',
            data: htmlContent
        });
    }

    highlightDarkPatterns() {
        if (!this.currentAnalysis || !this.currentAnalysis.findings) return;

        this.removeHighlights(); // Clear existing highlights

        this.currentAnalysis.findings.forEach((finding, index) => {
            if (finding.engine === 'NLP' && finding.source_text) {
                this.highlightTextPattern(finding, index);
            } else if (finding.engine === 'VISUAL' && finding.bbox) {
                this.highlightVisualPattern(finding, index);
            }
        });
    }

    highlightTextPattern(finding, index) {
        const text = finding.source_text;
        if (!text) return;

        // Find and highlight text in the page
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        let node;
        while (node = walker.nextNode()) {
            if (node.textContent.includes(text)) {
                const span = document.createElement('span');
                span.className = `aegis-highlight aegis-severity-${finding.severity.toLowerCase()}`;
                span.setAttribute('data-aegis-index', index);
                span.setAttribute('data-aegis-type', finding.type);
                span.setAttribute('title', `${finding.type}: ${finding.explanation}`);

                const parent = node.parentNode;
                const textContent = node.textContent;
                const startIndex = textContent.indexOf(text);

                if (startIndex !== -1) {
                    // Split the text node and wrap the matching part
                    const beforeText = textContent.substring(0, startIndex);
                    const afterText = textContent.substring(startIndex + text.length);

                    const beforeNode = document.createTextNode(beforeText);
                    const highlightNode = document.createTextNode(text);
                    const afterNode = document.createTextNode(afterText);

                    span.appendChild(highlightNode);
                    parent.insertBefore(beforeNode, node);
                    parent.insertBefore(span, node);
                    parent.insertBefore(afterNode, node);
                    parent.removeChild(node);

                    break;
                }
            }
        }
    }

    highlightVisualPattern(finding, index) {
        const [x, y, width, height] = finding.bbox;
        
        const overlay = document.createElement('div');
        overlay.className = `aegis-visual-overlay aegis-severity-${finding.severity.toLowerCase()}`;
        overlay.setAttribute('data-aegis-index', index);
        overlay.setAttribute('data-aegis-type', finding.type);
        overlay.style.cssText = `
            position: absolute;
            left: ${x}px;
            top: ${y}px;
            width: ${width}px;
            height: ${height}px;
            border: 2px solid ${this.getSeverityColor(finding.severity)};
            background-color: ${this.getSeverityColor(finding.severity)}20;
            pointer-events: none;
            z-index: 999999;
            box-sizing: border-box;
        `;

        // Add tooltip
        overlay.setAttribute('title', `${finding.type}: ${finding.explanation}`);

        document.body.appendChild(overlay);
    }

    applyGhostWriterChanges() {
        if (!this.currentAnalysis || !this.currentAnalysis.findings) return;

        this.currentAnalysis.findings.forEach((finding) => {
            if (finding.engine === 'NLP' && finding.remediation) {
                this.replaceTextPattern(finding);
            }
        });
    }

    replaceTextPattern(finding) {
        const originalText = finding.source_text;
        const remediation = finding.remediation;
        
        if (!originalText || !remediation) return;

        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        let node;
        while (node = walker.nextNode()) {
            if (node.textContent.includes(originalText)) {
                node.textContent = node.textContent.replace(originalText, remediation);
                
                // Add a subtle indicator that text was modified
                const parent = node.parentNode;
                if (parent && parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE') {
                    parent.setAttribute('data-aegis-remediated', 'true');
                    parent.style.backgroundColor = '#e8f5e8';
                }
            }
        }
    }

    removeGhostWriterChanges() {
        // Remove remediation indicators
        const remediatedElements = document.querySelectorAll('[data-aegis-remediated="true"]');
        remediatedElements.forEach(element => {
            element.removeAttribute('data-aegis-remediated');
            element.style.backgroundColor = '';
        });
    }

    removeHighlights() {
        // Remove text highlights
        const highlights = document.querySelectorAll('.aegis-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            const text = highlight.textContent;
            parent.replaceChild(document.createTextNode(text), highlight);
            parent.normalize(); // Merge adjacent text nodes
        });

        // Remove visual overlays
        const overlays = document.querySelectorAll('.aegis-visual-overlay');
        overlays.forEach(overlay => overlay.remove());
    }

    getSeverityColor(severity) {
        const colors = {
            'HIGH': '#ff4444',
            'MEDIUM': '#ffaa00',
            'LOW': '#44ff44'
        };
        return colors[severity] || '#ffaa00';
    }

    // Inject CSS for highlights
    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .aegis-highlight {
                background-color: #ffeb3b;
                padding: 2px 4px;
                border-radius: 3px;
                cursor: help;
                position: relative;
            }
            
            .aegis-severity-high {
                background-color: #ffcccc !important;
                border: 1px solid #ff4444;
            }
            
            .aegis-severity-medium {
                background-color: #fff3cd !important;
                border: 1px solid #ffaa00;
            }
            
            .aegis-severity-low {
                background-color: #d4edda !important;
                border: 1px solid #44ff44;
            }
            
            .aegis-highlight:hover::after {
                content: attr(title);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1000000;
                max-width: 300px;
                word-wrap: break-word;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize content script
const aegisContent = new AegisContentScript();
