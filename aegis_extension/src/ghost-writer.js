// Aegis Pro Ghost-Writer Module
// Active remediation for detected dark patterns

class GhostWriter {
    constructor() {
        this.remediations = new Map();
        this.originalContent = new Map();
        this.isActive = false;
    }

    // Initialize Ghost-Writer mode
    init() {
        this.isActive = true;
        console.log('Aegis Pro Ghost-Writer activated');
        this.setupMutationObserver();
        this.remediateCurrentPage();
    }

    // Setup observer to catch dynamic content changes
    setupMutationObserver() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            this.checkAndRemediate(node);
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Remediate current page content
    remediateCurrentPage() {
        this.remediateConfirmShaming();
        this.remediateUrgency();
        this.remediateHiddenElements();
        this.remediateLowContrast();
        this.remediateVisualHierarchy();
        this.remediatePreselected();
    }

    // Remediate confirm shaming patterns
    remediateConfirmShaming() {
        const patterns = [
            /no thanks,? i (don't|do not|hate) want to/gi,
            /cancel.*and lose.*benefits/gi,
            /stay.*and get.*discount/gi
        ];

        document.querySelectorAll('button, p, span, div').forEach(element => {
            const text = element.textContent;
            patterns.forEach(pattern => {
                if (pattern.test(text)) {
                    this.saveOriginal(element);
                    element.textContent = text.replace(pattern, this.getNeutralAlternative(text));
                    this.highlightRemediated(element);
                }
            });
        });
    }

    // Remediate urgency patterns
    remediateUrgency() {
        const urgencyElements = document.querySelectorAll('[class*="timer"], [class*="countdown"], [class*="urgent"]');
        
        urgencyElements.forEach(element => {
            if (element.textContent.match(/only\s+\d+\s+left|limited\s+time|ends\s+in/gi)) {
                this.saveOriginal(element);
                element.textContent = this.getNeutralUrgencyText(element.textContent);
                this.highlightRemediated(element);
            }
        });
    }

    // Remediate hidden elements
    remediateHiddenElements() {
        const hiddenElements = document.querySelectorAll('[style*="display: none"], [style*="visibility: hidden"]');
        
        hiddenElements.forEach(element => {
            // Check if it's a close button or important element
            if (element.textContent.match(/^[x×]$/i) || element.getAttribute('aria-label')?.match(/close/i)) {
                this.saveOriginal(element);
                element.style.display = 'block';
                element.style.visibility = 'visible';
                element.style.backgroundColor = '#ff4444';
                element.style.color = 'white';
                element.style.padding = '4px';
                element.style.borderRadius = '4px';
                this.highlightRemediated(element);
            }
        });
    }

    // Remediate low contrast elements
    remediateLowContrast() {
        const buttons = document.querySelectorAll('button, [role="button"]');
        
        buttons.forEach(button => {
            const computedStyle = window.getComputedStyle(button);
            const bgColor = this.rgbToHex(computedStyle.backgroundColor);
            const textColor = this.rgbToHex(computedStyle.color);
            
            if (this.getContrastRatio(bgColor, textColor) < 3) {
                this.saveOriginal(button);
                button.style.color = this.getContrastingColor(bgColor);
                this.highlightRemediated(button);
            }
        });
    }

    // Remediate visual hierarchy issues
    remediateVisualHierarchy() {
        const buttons = document.querySelectorAll('button');
        
        buttons.forEach(button => {
            const text = button.textContent.toLowerCase();
            if (text.includes('purchase') || text.includes('buy')) {
                // Make primary actions more prominent
                if (button.style.backgroundColor === 'gray' || !button.style.backgroundColor) {
                    this.saveOriginal(button);
                    button.style.backgroundColor = '#4ade80';
                    button.style.color = '#065f46';
                    button.style.fontWeight = 'bold';
                    this.highlightRemediated(button);
                }
            }
        });
    }

    // Remediate pre-selected checkboxes
    remediatePreselected() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][checked]');
        
        checkboxes.forEach(checkbox => {
            const label = checkbox.closest('label') || document.querySelector(`label[for="${checkbox.id}"]`);
            if (label && label.textContent.match(/newsletter|marketing|terms/i)) {
                this.saveOriginal(checkbox);
                checkbox.checked = false;
                checkbox.parentElement.style.border = '2px solid #4ade80';
                this.highlightRemediated(checkbox);
            }
        });
    }

    // Helper methods
    saveOriginal(element) {
        if (!this.originalContent.has(element)) {
            this.originalContent.set(element, {
                html: element.innerHTML,
                text: element.textContent,
                style: element.getAttribute('style')
            });
        }
    }

    getNeutralAlternative(text) {
        const alternatives = {
            'no thanks, i hate saving money': 'No thanks, I prefer not to receive updates',
            'cancel and lose benefits': 'Continue without benefits',
            'stay and get discount': 'Continue at regular price'
        };
        
        const lowerText = text.toLowerCase();
        for (const [pattern, alternative] of Object.entries(alternatives)) {
            if (lowerText.includes(pattern)) {
                return alternative;
            }
        }
        
        return 'Continue without additional features';
    }

    getNeutralUrgencyText(text) {
        return text.replace(/only\s+\d+\s+left/gi, 'Limited availability')
                 .replace(/limited\s+time/gi, 'Available for now')
                 .replace(/ends\s+in/gi, 'Time-limited offer');
    }

    rgbToHex(rgb) {
        const match = rgb.match(/\d+/g);
        if (!match || match.length < 3) return '#000000';
        
        const r = parseInt(match[0]);
        const g = parseInt(match[1]);
        const b = parseInt(match[2]);
        
        return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }

    getContrastRatio(bgColor, textColor) {
        // Simplified contrast ratio calculation
        const bgLuma = this.getLuminance(bgColor);
        const textLuma = this.getLuminance(textColor);
        
        const lighter = Math.max(bgLuma, textLuma);
        const darker = Math.min(bgLuma, textLuma);
        
        return (lighter + 0.05) / (darker + 0.05);
    }

    getLuminance(hex) {
        const r = parseInt(hex.slice(1, 3), 16) / 255;
        const g = parseInt(hex.slice(3, 5), 16) / 255;
        const b = parseInt(hex.slice(5, 7), 16) / 255;
        
        return 0.299 * r + 0.587 * g + 0.114 * b;
    }

    getContrastingColor(bgColor) {
        const luma = this.getLuminance(bgColor);
        return luma > 0.5 ? '#000000' : '#ffffff';
    }

    highlightRemediated(element) {
        element.style.border = '2px dashed #4ade80';
        element.style.boxShadow = '0 0 10px rgba(74, 222, 128, 0.3)';
        
        // Add tooltip
        const tooltip = document.createElement('div');
        tooltip.textContent = 'Aegis Pro: Dark pattern remediated';
        tooltip.style.cssText = `
            position: absolute;
            background: #065f46;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10000;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.appendChild(tooltip);
        
        // Show tooltip on hover
        element.addEventListener('mouseenter', () => {
            tooltip.style.display = 'block';
        });
        
        element.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });
    }

    // Check and remediate new elements
    checkAndRemediate(node) {
        if (!this.isActive) return;
        
        // Check for patterns in new content
        if (node.textContent) {
            const patterns = [/no thanks.*hate/i, /limited time/i, /only \d+ left/i];
            patterns.forEach(pattern => {
                if (pattern.test(node.textContent)) {
                    setTimeout(() => this.remediateCurrentPage(), 100);
                }
            });
        }
    }

    // Restore original content
    restoreOriginal() {
        this.originalContent.forEach((original, element) => {
            element.innerHTML = original.html;
            element.textContent = original.text;
            if (original.style) {
                element.setAttribute('style', original.style);
            } else {
                element.removeAttribute('style');
            }
        });
        
        this.originalContent.clear();
        this.isActive = false;
        console.log('Aegis Pro Ghost-Writer deactivated');
    }

    // Get remediation summary
    getRemediationSummary() {
        return {
            isActive: this.isActive,
            remediatedElements: this.originalContent.size,
            timestamp: new Date().toISOString()
        };
    }
}

// Make Ghost-Writer available globally
window.AegisProGhostWriter = new GhostWriter();

// Auto-initialize if enabled
chrome.storage.sync.get(['ghostWriterEnabled'], (result) => {
    if (result.ghostWriterEnabled) {
        window.AegisProGhostWriter.init();
    }
});
