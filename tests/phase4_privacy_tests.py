"""
Dark Pattern Detection Phase 4: Privacy & Data Protection Test Suite
Testing consent patterns, data collection, privacy policy analysis (TC-41 to TC-50)
"""

import pytest
import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer

class TestPhase4_PrivacyDataProtection:
    """Phase 4: Privacy & Data Protection Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC41_privacy_policy_obfuscation(self):
        """TC-41: Privacy Policy Obfuscation - Detect legal jargon and unclear language"""
        html_content = """
        <div class="privacy-policy">
            <h2>Privacy Policy</h2>
            <p>We may utilize cookies and similar technologies for the purposes of 
            data aggregation, behavioral analysis, and targeted advertising initiatives 
            pursuant to applicable regulatory frameworks and user consent protocols.</p>
            <p>Your personal information may be shared with third-party service providers 
            and affiliates for business purposes as explicitly outlined in our terms of service.</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/privacy",
            html_content=html_content
        )
        
        privacy_obfuscation_found = any(
            f['type'] in ['privacy_obfuscation', 'complex_legal_jargon'] or 
            ('obfuscat' in f.get('explanation', '').lower() or 'jargon' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert privacy_obfuscation_found, "Expected detection of privacy policy obfuscation"
    
    def test_TC42_data_minimization_violation(self):
        """TC-42: Data Minimization Violation - Excessive data collection"""
        html_content = """
        <form class="registration-form">
            <h3>Create Account</h3>
            <input type="text" name="full_name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="tel" name="phone" placeholder="Phone Number" required>
            <input type="text" name="address" placeholder="Street Address" required>
            <input type="text" name="city" placeholder="City" required>
            <input type="text" name="state" placeholder="State" required>
            <input type="text" name="zip" placeholder="ZIP Code" required>
            <input type="date" name="birth_date" placeholder="Date of Birth" required>
            <input type="text" name="ssn" placeholder="Social Security Number" required>
            <input type="text" name="mothers_maiden" placeholder="Mother's Maiden Name" required>
            <input type="text" name="pet_name" placeholder="First Pet Name" required>
            <input type="text" name="school" placeholder="High School" required>
            <button type="submit">Create Account</button>
        </form>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/register",
            html_content=html_content
        )
        
        data_minimization_violation_found = any(
            f['type'] in ['excessive_data_collection', 'data_minimization_violation'] or
            ('excessive' in f.get('explanation', '').lower() and 'data' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert data_minimization_violation_found, "Expected detection of excessive data collection"
    
    def test_TC43_cookie_consent_bypass(self):
        """TC-43: Cookie Consent Bypass - Non-compliant cookie banners"""
        html_content = """
        <div class="cookie-banner" style="position: fixed; bottom: 0; width: 100%; background: #333; color: white; padding: 10px;">
            <p>We use cookies to enhance your experience. By continuing, you accept our use of cookies.</p>
            <button onclick="this.parentElement.style.display='none'" style="background: #4CAF50; color: white; padding: 5px 10px;">Accept</button>
            <button onclick="location.reload()" style="background: #f44336; color: white; padding: 5px 10px;">Reject</button>
        </div>
        <script>
            // Auto-accept cookies after 5 seconds
            setTimeout(() => {
                document.querySelector('.cookie-banner button').click();
            }, 5000);
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        cookie_consent_bypass_found = any(
            f['type'] in ['cookie_consent_bypass', 'auto_accept_cookies'] or
            ('cookie' in f.get('explanation', '').lower() and 'auto' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert cookie_consent_bypass_found, "Expected detection of cookie consent bypass"
    
    def test_TC44_data_retention_violation(self):
        """TC-44: Data Retention Violation - No clear data deletion policy"""
        html_content = """
        <div class="data-policy">
            <h3>Data Retention Policy</h3>
            <p>We retain user data for business purposes and may keep it indefinitely 
            to improve our services and comply with legal requirements.</p>
            <p>User data may be stored permanently for analytics and marketing purposes.</p>
            <p>We do not provide automatic data deletion options.</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/data-policy",
            html_content=html_content
        )
        
        data_retention_violation_found = any(
            f['type'] in ['data_retention_violation', 'permanent_data_storage'] or
            ('retention' in f.get('explanation', '').lower() and 'violation' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert data_retention_violation_found, "Expected detection of data retention violation"
    
    def test_TC45_third_party_sharing(self):
        """TC-45: Third Party Sharing - Hidden data sharing agreements"""
        html_content = """
        <div class="partners">
            <h3>Our Trusted Partners</h3>
            <p>We work with leading companies to provide you with the best experience.</p>
            <script src="https://google-analytics.com/analytics.js"></script>
            <script src="https://facebook.com/tracking.js"></script>
            <script src="https://doubleclick.net/advertising.js"></script>
            <script>
                // Share user data with partners
                const userBehavior = trackUserActions();
                fetch('https://partners.example.com/share-data', {
                    method: 'POST',
                    body: JSON.stringify(userBehavior)
                });
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        third_party_sharing_found = any(
            f['type'] in ['third_party_sharing', 'data_sharing'] or
            ('sharing' in f.get('explanation', '').lower() and 'third' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert third_party_sharing_found, "Expected detection of third party data sharing"
    
    def test_TC46_location_tracking(self):
        """TC-46: Location Tracking - Excessive geolocation data collection"""
        html_content = """
        <div class="app-features">
            <h3>Enhanced Location Services</h3>
            <button onclick="enableLocationTracking()">Enable Location</button>
            <script>
                function enableLocationTracking() {
                    // Track user location continuously
                    setInterval(() => {
                        navigator.geolocation.getCurrentPosition(
                            position => {
                                const locationData = {
                                    latitude: position.coords.latitude,
                                    longitude: position.coords.longitude,
                                    timestamp: Date.now(),
                                    accuracy: position.coords.accuracy,
                                    altitude: position.coords.altitude,
                                    speed: position.coords.speed
                                };
                                // Send to server every 30 seconds
                                fetch('/api/location', {
                                    method: 'POST',
                                    body: JSON.stringify(locationData)
                                });
                            }
                        );
                    }, 30000);
                }
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        location_tracking_found = any(
            f['type'] in ['excessive_location_tracking', 'location_tracking'] or
            ('location' in f.get('explanation', '').lower() and 'tracking' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert location_tracking_found, "Expected detection of excessive location tracking"
    
    def test_TC47_biometric_data_collection(self):
        """TC-47: Biometric Data Collection - Unauthorized biometric data"""
        html_content = """
        <div class="security-features">
            <h3>Advanced Security</h3>
            <p>Use your face for secure login</p>
            <video id="face-scan" autoplay></video>
            <button onclick="startFaceScan()">Scan Face</button>
            <script>
                function startFaceScan() {
                    const video = document.getElementById('face-scan');
                    navigator.mediaDevices.getUserMedia({ video: true })
                        .then(stream => {
                            video.srcObject = stream;
                            // Capture face data every 5 seconds
                            setInterval(() => {
                                const canvas = document.createElement('canvas');
                                canvas.width = video.videoWidth;
                                canvas.height = video.videoHeight;
                                const ctx = canvas.getContext('2d');
                                ctx.drawImage(video, 0, 0);
                                const faceData = canvas.toDataURL();
                                // Send face data to server
                                fetch('/api/biometric', {
                                    method: 'POST',
                                    body: JSON.stringify({ faceData, timestamp: Date.now() })
                                });
                            }, 5000);
                        });
                }
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/security",
            html_content=html_content
        )
        
        biometric_collection_found = any(
            f['type'] in ['biometric_data_collection', 'unauthorized_biometric'] or
            ('biometric' in f.get('explanation', '').lower() or 'face' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert biometric_collection_found, "Expected detection of biometric data collection"
    
    def test_TC48_children_privacy_violation(self):
        """TC-48: Children Privacy Violation - COPPA violations"""
        html_content = """
        <div class="kids-section">
            <h3>Fun Games for Kids!</h3>
            <p>Join our kids club and get special prizes!</p>
            <form class="kids-signup">
                <input type="text" name="child_name" placeholder="Your Name" required>
                <input type="number" name="age" placeholder="Your Age" required>
                <input type="text" name="parent_email" placeholder="Parent's Email" required>
                <input type="text" name="school" placeholder="Your School" required>
                <button type="submit">Join Now!</button>
            </form>
            <script>
                // Collect kids data without parental consent
                document.querySelector('.kids-signup').addEventListener('submit', (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const kidData = {
                        name: formData.get('child_name'),
                        age: formData.get('age'),
                        email: formData.get('parent_email'),
                        school: formData.get('school')
                    };
                    // Send to marketing database
                    fetch('/api/kids-data', {
                        method: 'POST',
                        body: JSON.stringify(kidData)
                    });
                });
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/kids",
            html_content=html_content
        )
        
        children_privacy_violation_found = any(
            f['type'] in ['children_privacy_violation', 'coppa_violation'] or
            ('children' in f.get('explanation', '').lower() or 'coppa' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert children_privacy_violation_found, "Expected detection of children privacy violation"
    
    def test_TC49_dark_pattern_consent(self):
        """TC-49: Dark Pattern Consent - Manipulative consent mechanisms"""
        html_content = """
        <div class="consent-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999;">
            <div class="consent-content" style="background: white; padding: 20px; margin: 100px auto; max-width: 400px;">
                <h2>Get the Best Experience!</h2>
                <p>Accept our terms to continue using our amazing features.</p>
                <button onclick="acceptAll()" style="background: #4CAF50; color: white; padding: 15px 30px; font-size: 18px; width: 100%; margin-bottom: 10px;">Accept All & Continue</button>
                <button onclick="showMoreOptions()" style="background: #f0f0f0; color: #666; padding: 5px 10px; font-size: 12px; text-decoration: underline; border: none; background: none;">Learn more</button>
                <div id="more-options" style="display: none;">
                    <p>Detailed options for data processing preferences...</p>
                    <button onclick="customizeSettings()" style="background: #ccc; padding: 5px 10px; font-size: 12px;">Customize</button>
                </div>
            </div>
            <script>
                function acceptAll() {
                    // Accept all tracking and data sharing
                    localStorage.setItem('consent', 'all');
                    document.querySelector('.consent-modal').style.display = 'none';
                }
                function showMoreOptions() {
                    document.getElementById('more-options').style.display = 'block';
                }
                function customizeSettings() {
                    // Make it difficult to customize
                    alert('Customization temporarily unavailable. Please accept all to continue.');
                }
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        dark_pattern_consent_found = any(
            f['type'] in ['dark_pattern_consent', 'manipulative_consent'] or
            ('consent' in f.get('explanation', '').lower() and ('dark' in f.get('explanation', '').lower() or 'manipulative' in f.get('explanation', '').lower()))
            for f in result['findings']
        )
        assert dark_pattern_consent_found, "Expected detection of dark pattern consent"
    
    def test_TC50_surveillance_capitalism(self):
        """TC-50: Surveillance Capitalism - Data monetization without transparency"""
        html_content = """
        <div class="data-monetization">
            <h3>Personalized Experience</h3>
            <p>We use advanced AI to provide you with tailored recommendations.</p>
            <script>
                // Comprehensive user profiling
                const userProfile = {
                    demographics: collectDemographics(),
                    behavior: trackUserBehavior(),
                    preferences: analyzePreferences(),
                    socialGraph: mapSocialConnections(),
                    financialData: inferFinancialStatus(),
                    healthData: predictHealthRisks(),
                    politicalViews: analyzePoliticalLeanings()
                };
                
                // Monetize user data
                fetch('https://data-broker.example.com/sell-profile', {
                    method: 'POST',
                    body: JSON.stringify({
                        profile: userProfile,
                        price: calculateDataValue(userProfile),
                        buyers: ['advertisers', 'insurers', 'employers', 'political_campaigns']
                    })
                });
                
                function collectDemographics() {
                    return {
                        age: inferAge(),
                        gender: inferGender(),
                        location: getLocation(),
                        income: inferIncome(),
                        education: inferEducation(),
                        ethnicity: inferEthnicity()
                    };
                }
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        surveillance_capitalism_found = any(
            f['type'] in ['surveillance_capitalism', 'data_monetization'] or
            ('surveillance' in f.get('explanation', '').lower() or 'monetization' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert surveillance_capitalism_found, "Expected detection of surveillance capitalism"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
