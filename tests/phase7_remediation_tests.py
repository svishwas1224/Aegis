"""
Dark Pattern Detection Phase 7: Remediation Features Test Suite
Testing Ghost-Writer mode, color override, auto-hide, timer neutralization (TC-76 to TC-85)
"""

import pytest
import sys
import os
import json
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer

class TestPhase7_Remediation:
    """Phase 7: Remediation Features Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC76_ghost_writer_mode(self):
        """TC-76: Ghost-Writer Mode - Test active remediation functionality"""
        html_content = """
        <div class="dark-patterns">
            <button onclick="alert('No thanks, I hate saving money!')">Decline Offer</button>
            <p>Limited time offer! Only 2 items left!</p>
            <div style="background-color: white;">
                <button style="background-color: white; color: white;">X Close</button>
            </div>
            <form>
                <input type="checkbox" name="newsletter" checked> Subscribe to newsletter
            </form>
        </div>
        """
        
        # Test Ghost-Writer remediation
        result = self.engine.analyze_comprehensive(
            url="https://example.com/ghost-writer-test",
            html_content=html_content
        )
        
        # Check if Ghost-Writer mode is available
        ghost_writer_available = 'remediation' in str(result).lower() or 'ghost' in str(result).lower()
        
        # Test remediation suggestions
        remediation_found = any(
            'remediation' in f.get('remediation', '').lower() or 
            'neutral' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert ghost_writer_available or remediation_found, "Expected Ghost-Writer mode or remediation features"
    
    def test_TC77_color_override_functionality(self):
        """TC-77: Color Override - Test color-based remediation"""
        html_content = """
        <div class="low-contrast-content">
            <button style="background-color: #f0f0f0; color: #f5f5f5; padding: 15px;">
                Hard to Read Button
            </button>
            <p style="color: #cccccc; background-color: #dddddd;">
                Low contrast text that's hard to read
            </p>
            <div style="background-color: white;">
                <span style="color: white; background-color: white;">Hidden text</span>
            </div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/color-override-test",
            html_content=html_content
        )
        
        # Check for contrast issues detection
        contrast_issues_found = any(
            f['type'] in ['low_contrast', 'contrast_issue'] or
            ('contrast' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for color-based remediation suggestions
        color_remediation_found = any(
            'color' in f.get('remediation', '').lower() or
            'contrast' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert contrast_issues_found, "Expected detection of color contrast issues"
        assert color_remediation_found, "Expected color-based remediation suggestions"
    
    def test_TC78_auto_hide_mechanism(self):
        """TC-78: Auto-Hide Mechanism - Test automatic hiding of dark patterns"""
        html_content = """
        <div class="auto-hide-test">
            <div class="popup-overlay" id="urgent-popup">
                <div style="position: fixed; top: 0; width: 100%; background: red; color: white; padding: 10px; z-index: 9999;">
                    URGENT: Only 2 left! Buy now!
                    <button onclick="this.parentElement.parentElement.style.display='none'">X</button>
                </div>
            </div>
            
            <div class="fake-countdown" id="timer">
                <span style="position: fixed; bottom: 0; background: black; color: lime; padding: 5px;">
                    05:00
                </span>
            </div>
            
            <div class="social-proof-fake" id="social">
                <div style="position: fixed; right: 0; top: 100px; background: green; color: white; padding: 10px;">
                    1,247 people viewing!
                </div>
            </div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/auto-hide-test",
            html_content=html_content
        )
        
        # Check for detection of auto-hide candidates
        auto_hide_candidates_found = any(
            f['type'] in ['urgency', 'social_proof', 'fake_countdown'] or
            ('fixed' in str(result) and ('position' in str(result) or 'overlay' in str(result)))
            for f in result['findings']
        )
        
        # Check for hiding mechanism suggestions
        hide_remediation_found = any(
            'hide' in f.get('remediation', '').lower() or
            'remove' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert auto_hide_candidates_found, "Expected detection of auto-hide candidates"
        assert hide_remediation_found, "Expected hiding mechanism suggestions"
    
    def test_TC79_timer_neutralization(self):
        """TC-79: Timer Neutralization - Test countdown timer remediation"""
        html_content = """
        <div class="timer-test">
            <div class="countdown-1">
                <span id="timer1">05:00</span>
                <script>
                    let time1 = 300;
                    setInterval(() => {
                        time1--;
                        document.getElementById('timer1').textContent = 
                            Math.floor(time1/60) + ':' + (time1%60).toString().padStart(2, '0');
                    }, 1000);
                </script>
            </div>
            
            <div class="countdown-2">
                <div class="fake-timer">
                    Only <span class="hours">2</span> hours <span class="minutes">30</span> minutes left!
                </div>
                <script>
                    // Fake countdown that resets
                    setInterval(() => {
                        document.querySelector('.hours').textContent = Math.floor(Math.random() * 24);
                        document.querySelector('.minutes').textContent = Math.floor(Math.random() * 60);
                    }, 5000);
                </script>
            </div>
            
            <div class="countdown-3">
                <div id="progress-timer">
                    <div style="width: 80%; background: red; color: white; padding: 5px;">
                        Offer expires in <span id="expiry-time">1 hour</span>
                    </div>
                </div>
            </div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/timer-neutralization-test",
            html_content=html_content
        )
        
        # Check for timer detection
        timer_patterns_found = any(
            f['type'] in ['fake_countdown', 'urgency', 'timer_manipulation'] or
            ('timer' in f.get('explanation', '').lower() or 'countdown' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for timer neutralization suggestions
        timer_remediation_found = any(
            'timer' in f.get('remediation', '').lower() or
            'countdown' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert timer_patterns_found, "Expected detection of timer patterns"
        assert timer_remediation_found, "Expected timer neutralization suggestions"
    
    def test_TC80_text_replacement_engine(self):
        """TC-80: Text Replacement Engine - Test text-based remediation"""
        html_content = """
        <div class="text-manipulation">
            <p>No thanks, I hate saving money and don't want exclusive deals!</p>
            <p>Limited time offer! Only 2 items left in stock!</p>
            <p>Join 1,247 satisfied customers who bought today!</p>
            <p>Your PC is infected with 5 viruses! Download antivirus now!</p>
            <button>Continue without saving $50</button>
            <button>Skip and pay more later</button>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/text-replacement-test",
            html_content=html_content
        )
        
        # Check for text-based dark pattern detection
        text_patterns_found = any(
            f['type'] in ['confirm_shaming', 'urgency', 'social_proof', 'security_pressure'] or
            ('text' in f.get('source_text', '') and f.get('engine') == 'NLP')
            for f in result['findings']
        )
        
        # Check for text replacement suggestions
        text_remediation_found = any(
            'text' in f.get('remediation', '').lower() or
            'replace' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert text_patterns_found, "Expected detection of text-based dark patterns"
        assert text_remediation_found, "Expected text replacement suggestions"
    
    def test_TC81_layout_restoration(self):
        """TC-81: Layout Restoration - Test layout-based remediation"""
        html_content = """
        <div class="layout-manipulation">
            <!-- Visual hierarchy misdirection -->
            <button style="background-color: gray; padding: 15px; font-size: 14px;">
                Primary Action - Purchase Now
            </button>
            <button style="background-color: red; padding: 20px; font-size: 18px; font-weight: bold;">
                Secondary - Maybe Later
            </button>
            
            <!-- Hidden important elements -->
            <div style="position: absolute; left: -9999px; top: -9999px;">
                <a href="/cancel-subscription">Cancel Subscription</a>
            </div>
            
            <!-- Misleading positioning -->
            <div style="position: fixed; bottom: 0; width: 100%; z-index: 9999;">
                <button style="background: #4CAF50; color: white; padding: 20px; width: 100%;">
                    ACCEPT ALL COOKIES
                </button>
                <button style="background: #f0f0f0; color: #666; padding: 5px; font-size: 10px;">
                    Settings
                </button>
            </div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/layout-restoration-test",
            html_content=html_content
        )
        
        # Check for layout manipulation detection
        layout_patterns_found = any(
            f['type'] in ['visual_hierarchy', 'hidden_element', 'misdirection'] or
            ('layout' in f.get('explanation', '').lower() or 'hierarchy' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for layout restoration suggestions
        layout_remediation_found = any(
            'layout' in f.get('remediation', '').lower() or
            'hierarchy' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert layout_patterns_found, "Expected detection of layout manipulation"
        assert layout_remediation_found, "Expected layout restoration suggestions"
    
    def test_TC82_behavioral_intervention(self):
        """TC-82: Behavioral Intervention - Test behavior-based remediation"""
        html_content = """
        <div class="behavioral-manipulation">
            <!-- Forced action -->
            <script>
                if (!localStorage.getItem('email')) {
                    window.location.href = '/signup-required';
                }
            </script>
            
            <!-- Sneak into basket -->
            <script>
                fetch('/api/cart/add', {
                    method: 'POST',
                    body: JSON.stringify({item_id: 'auto-add-123', auto_add: true})
                });
            </script>
            
            <!-- Price flickering -->
            <script>
                let basePrice = 99.99;
                setInterval(() => {
                    const price = basePrice + (Math.random() * 30);
                    document.getElementById('dynamic-price').textContent = '$' + price.toFixed(2);
                }, 3000);
            </script>
            
            <div id="dynamic-price">$99.99</div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/behavioral-intervention-test",
            html_content=html_content
        )
        
        # Check for behavioral manipulation detection
        behavioral_patterns_found = any(
            f['type'] in ['forced_action', 'sneak_basket', 'price_flickering'] or
            ('behavior' in f.get('explanation', '').lower() or 'script' in f.get('source_text', ''))
            for f in result['findings']
        )
        
        # Check for behavioral intervention suggestions
        behavioral_remediation_found = any(
            'behavior' in f.get('remediation', '').lower() or
            'script' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert behavioral_patterns_found, "Expected detection of behavioral manipulation"
        assert behavioral_remediation_found, "Expected behavioral intervention suggestions"
    
    def test_TC83_accessibility_enhancement(self):
        """TC-83: Accessibility Enhancement - Test accessibility-based remediation"""
        html_content = """
        <div class="accessibility-issues">
            <!-- Poor color contrast -->
            <button style="background-color: #e0e0e0; color: #f0f0f0; padding: 10px;">
                Low Contrast Button
            </button>
            
            <!-- Missing alt text -->
            <img src="product.jpg" width="200" height="150">
            
            <!-- Poor heading structure -->
            <div style="font-size: 18px; font-weight: bold;">Product Title</div>
            <div style="font-size: 16px; font-weight: bold;">Product Description</div>
            
            <!-- No focus indicators -->
            <a href="/product" style="text-decoration: none; color: #333; outline: none;">
                Product Link
            </a>
            
            <!-- Small touch targets -->
            <button style="width: 20px; height: 20px; font-size: 10px;">
                X
            </button>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/accessibility-enhancement-test",
            html_content=html_content
        )
        
        # Check for accessibility issues detection
        accessibility_issues_found = any(
            f['type'] in ['low_contrast', 'accessibility_issue'] or
            ('accessibility' in f.get('explanation', '').lower() or 'contrast' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for accessibility enhancement suggestions
        accessibility_remediation_found = any(
            'accessibility' in f.get('remediation', '').lower() or
            'wcag' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert accessibility_issues_found, "Expected detection of accessibility issues"
        assert accessibility_remediation_found, "Expected accessibility enhancement suggestions"
    
    def test_TC84_privacy_protection(self):
        """TC-84: Privacy Protection - Test privacy-based remediation"""
        html_content = """
        <div class="privacy-violations">
            <!-- Excessive data collection -->
            <form>
                <input type="text" name="full_name" placeholder="Full Name" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="tel" name="phone" placeholder="Phone Number" required>
                <input type="text" name="ssn" placeholder="Social Security Number" required>
                <input type="text" name="address" placeholder="Full Address" required>
                <button type="submit">Submit</button>
            </form>
            
            <!-- Auto-accept cookies -->
            <script>
                setTimeout(() => {
                    document.cookie = 'marketing=true; path=/; max-age=31536000';
                    document.cookie = 'tracking=true; path=/; max-age=31536000';
                    document.cookie = 'analytics=true; path=/; max-age=31536000';
                }, 1000);
            </script>
            
            <!-- Location tracking -->
            <script>
                navigator.geolocation.getCurrentPosition(
                    position => {
                        fetch('/api/location', {
                            method: 'POST',
                            body: JSON.stringify({
                                lat: position.coords.latitude,
                                lng: position.coords.longitude
                            })
                        });
                    }
                );
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/privacy-protection-test",
            html_content=html_content
        )
        
        # Check for privacy violations detection
        privacy_violations_found = any(
            f['type'] in ['excessive_data_collection', 'privacy_violation'] or
            ('privacy' in f.get('explanation', '').lower() or 'data' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for privacy protection suggestions
        privacy_remediation_found = any(
            'privacy' in f.get('remediation', '').lower() or
            'data' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert privacy_violations_found, "Expected detection of privacy violations"
        assert privacy_remediation_found, "Expected privacy protection suggestions"
    
    def test_TC85_performance_optimization(self):
        """TC-85: Performance Optimization - Test performance-based remediation"""
        html_content = """
        <div class="performance-issues">
            <!-- Excessive tracking scripts -->
            <script src="https://google-analytics.com/analytics.js"></script>
            <script src="https://facebook.com/tracking.js"></script>
            <script src="https://doubleclick.net/ad.js"></script>
            <script src="https://taboola.com/libtrc.js"></script>
            <script src="https://outbrain.com/track.js"></script>
            
            <!-- Large images without optimization -->
            <img src="huge-image.jpg" width="2000" height="1500" alt="Large Image">
            <img src="another-huge-image.jpg" width="1800" height="1200" alt="Another Large Image">
            
            <!-- Inefficient animations -->
            <script>
                setInterval(() => {
                    document.body.style.backgroundColor = 
                        '#' + Math.floor(Math.random()*16777215).toString(16);
                }, 100);
                
                setInterval(() => {
                    const elements = document.querySelectorAll('*');
                    elements.forEach(el => {
                        el.style.transform = `rotate(${Math.random() * 360}deg)`;
                    });
                }, 50);
            </script>
            
            <!-- Memory leaks -->
            <script>
                const leakyArray = [];
                setInterval(() => {
                    leakyArray.push(new Array(1000).fill('leak'));
                }, 1000);
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/performance-optimization-test",
            html_content=html_content
        )
        
        # Check for performance issues detection
        performance_issues_found = any(
            f['type'] in ['excessive_tracking', 'performance_issue'] or
            ('performance' in f.get('explanation', '').lower() or 'tracking' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        
        # Check for performance optimization suggestions
        performance_remediation_found = any(
            'performance' in f.get('remediation', '').lower() or
            'optimize' in f.get('remediation', '').lower()
            for f in result['findings']
        )
        
        assert performance_issues_found, "Expected detection of performance issues"
        assert performance_remediation_found, "Expected performance optimization suggestions"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
