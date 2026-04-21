"""
Aegis Pro Phase 8: Link Destination Integrity Test Suite
Testing redirect chains, bait-and-switch URLs, homograph attacks (TC-86 to TC-100)
"""

import pytest
import sys
import os
import json
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer

class TestPhase8_LinkIntegrity:
    """Phase 8: Link Destination Integrity Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC86_redirect_chain_detection(self):
        """TC-86: Redirect Chain Detection - Detect excessive redirect chains"""
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/offer'},
                    'response': {'status': 301, 'headers': [{'name': 'location', 'value': 'https://tracking.example.com/step1'}]},
                    'time': '2024-01-01T10:00:00Z'
                },
                {
                    'request': {'url': 'https://tracking.example.com/step1'},
                    'response': {'status': 302, 'headers': [{'name': 'location', 'value': 'https://ads.example.com/step2'}]},
                    'time': '2024-01-01T10:00:01Z'
                },
                {
                    'request': {'url': 'https://ads.example.com/step2'},
                    'response': {'status': 302, 'headers': [{'name': 'location', 'value': 'https://scam.example.com/final'}]},
                    'time': '2024-01-01T10:00:02Z'
                },
                {
                    'request': {'url': 'https://scam.example.com/final'},
                    'response': {'status': 200, 'content': {'text': '<h1>Final Destination - Scam Page</h1>'}},
                    'time': '2024-01-01T10:00:03Z'
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/redirect-test",
            har_data=har_data
        )
        
        redirect_chain_found = any(
            f['type'] in ['redirect_chain', 'excessive_redirects'] or
            ('redirect' in f.get('explanation', '').lower() or 'chain' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert redirect_chain_found, "Expected detection of redirect chain"
    
    def test_TC87_bait_and_switch_urls(self):
        """TC-87: Bait and Switch URLs - Detect URL deception"""
        html_content = """
        <div class="deceptive-links">
            <a href="https://amazon.com/deals" onclick="window.location='https://fake-amazon.scam.com'; return false;">
                Amazon Special Deal
            </a>
            <a href="https://paypal.com/secure" onclick="window.location='https://phishing-paypal.com'; return false;">
                Secure PayPal Payment
            </a>
            <a href="https://google.com/search" onclick="window.location='https://malware-site.com'; return false;">
                Google Search Results
            </a>
            <a href="#" onclick="window.location='https://scam.example.com'; return false;">
                Click Here for Prize
            </a>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/bait-switch-test",
            html_content=html_content
        )
        
        bait_switch_found = any(
            f['type'] in ['bait_and_switch', 'url_deception'] or
            ('bait' in f.get('explanation', '').lower() or 'switch' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert bait_switch_found, "Expected detection of bait and switch URLs"
    
    def test_TC88_homograph_attack_detection(self):
        """TC-88: Homograph Attack Detection - Detect lookalike domain attacks"""
        html_content = """
        <div class="homograph-attacks">
            <a href="https://www.googlé.com/search?q=buy+now">Google Search</a>
            <a href="https://www.arnazon.com/deals">Amazon Deals</a>
            <a href="https://www.facebòok.com/login">Facebook Login</a>
            <a href="https://www.paypaI.com/secure">PayPal Secure</a>
            <a href="https://www.microsoft.com/security">Microsoft Security</a>
        </div>
        <script>
            // JavaScript with homograph domains
            const fakeDomains = [
                'https://www.yahóo.com',
                'https://www.linkedìn.com',
                'https://www.instágram.com',
                'https://www.twítter.com'
            ];
            
            fakeDomains.forEach(domain => {
                const link = document.createElement('a');
                link.href = domain;
                link.textContent = 'Visit Trusted Site';
                document.querySelector('.homograph-attacks').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/homograph-test",
            html_content=html_content
        )
        
        homograph_attack_found = any(
            f['type'] in ['homograph_attack', 'lookalike_domain'] or
            ('homograph' in f.get('explanation', '').lower() or 'lookalike' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert homograph_attack_found, "Expected detection of homograph attack"
    
    def test_TC89_subdomain_deception(self):
        """TC-89: Subdomain Deception - Detect malicious subdomain usage"""
        html_content = """
        <div class="subdomain-deception">
            <a href="https://secure.paypal.example.com/login">Secure PayPal Login</a>
            <a href="https://accounts.google.trusted-site.com/signin">Google Account Sign In</a>
            <a href="https://support.microsoft.official-help.com/security">Microsoft Support</a>
            <a href="https://api.facebook.verification.com/auth">Facebook Verification</a>
            <a href="https://cdn.amazon.cloudfront.net/checkout">Amazon Checkout</a>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/subdomain-test",
            html_content=html_content
        )
        
        subdomain_deception_found = any(
            f['type'] in ['subdomain_deception', 'malicious_subdomain'] or
            ('subdomain' in f.get('explanation', '').lower() or 'deception' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert subdomain_deception_found, "Expected detection of subdomain deception"
    
    def test_TC90_url_shortener_abuse(self):
        """TC-90: URL Shortener Abuse - Detect malicious short URL usage"""
        html_content = """
        <div class="shortener-abuse">
            <a href="https://bit.ly/3xY7Z9A">Click here for amazing deal!</a>
            <a href="https://tinyurl.com/abc123xyz">Limited time offer!</a>
            <a href="https://t.co/shortlink">Twitter special promotion</a>
            <a href="https://goo.gl/abcdef">Google exclusive deal</a>
            <a href="https://ow.ly/xyz789">Ow.ly special content</a>
        </div>
        <script>
            // Dynamic short URLs
            const shortUrls = [
                'https://bit.ly/scam123',
                'https://tinyurl.com/fake456',
                'https://t.co/phishing789'
            ];
            
            shortUrls.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.textContent = 'Special Offer - Click Now!';
                document.querySelector('.shortener-abuse').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/shortener-test",
            html_content=html_content
        )
        
        shortener_abuse_found = any(
            f['type'] in ['url_shortener_abuse', 'malicious_short_url'] or
            ('shortener' in f.get('explanation', '').lower() or 'short' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert shortener_abuse_found, "Expected detection of URL shortener abuse"
    
    def test_TC91_domain_spoofing(self):
        """TC-91: Domain Spoofing - Detect domain impersonation"""
        html_content = """
        <div class="domain-spoofing">
            <a href="https://www-amazon.com/deals">Amazon Official Site</a>
            <a href="https://www.pay-pal.com/login">PayPal Login</a>
            <a href="https://www.face_book.com">Facebook</a>
            <a href="https://www.you_tube.com">YouTube</a>
            <a href="https://www.linked_in.com">LinkedIn</a>
        </div>
        <script>
            // JavaScript with spoofed domains
            const spoofedDomains = {
                'google': 'https://www.g00gle.com',
                'microsoft': 'https://www.micros0ft.com',
                'apple': 'https://www.appl3.com',
                'netflix': 'https://www.netfliix.com'
            };
            
            Object.keys(spoofedDomains).forEach(brand => {
                const link = document.createElement('a');
                link.href = spoofedDomains[brand];
                link.textContent = `Visit ${brand.charAt(0).toUpperCase() + brand.slice(1)} Official Site`;
                document.querySelector('.domain-spoofing').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/domain-spoofing-test",
            html_content=html_content
        )
        
        domain_spoofing_found = any(
            f['type'] in ['domain_spoofing', 'domain_impersonation'] or
            ('spoof' in f.get('explanation', '').lower() or 'impersonation' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert domain_spoofing_found, "Expected detection of domain spoofing"
    
    def test_TC92_phishing_url_patterns(self):
        """TC-92: Phishing URL Patterns - Detect common phishing URL structures"""
        html_content = """
        <div class="phishing-patterns">
            <a href="https://secure-login-paypal.com">Secure PayPal Login</a>
            <a href="https://account-verification-google.com">Google Account Verification</a>
            <a href="https://amazon-order-confirm.com">Amazon Order Confirmation</a>
            <a href="https://netflix-account-suspended.com">Netflix Account Suspended</a>
            <a href="https://microsoft-security-alert.com">Microsoft Security Alert</a>
        </div>
        <script>
            // Dynamic phishing URLs
            const phishingPatterns = [
                'https://apple-id-verification.com',
                'https://facebook-security-check.com',
                'https://instagram-account-lock.com',
                'https://twitter-password-reset.com'
            ];
            
            phishingPatterns.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.textContent = 'Security Alert - Click Here';
                document.querySelector('.phishing-patterns').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/phishing-patterns-test",
            html_content=html_content
        )
        
        phishing_patterns_found = any(
            f['type'] in ['phishing_url', 'phishing_pattern'] or
            ('phishing' in f.get('explanation', '').lower() or 'security' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert phishing_patterns_found, "Expected detection of phishing URL patterns"
    
    def test_TC93_malicious_redirect_detection(self):
        """TC-93: Malicious Redirect Detection - Detect harmful redirects"""
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://trusted-site.com/secure-login'},
                    'response': {
                        'status': 302,
                        'headers': [{'name': 'location', 'value': 'http://malicious-phishing.com/steal-credentials'}]
                    },
                    'time': '2024-01-01T10:00:00Z'
                },
                {
                    'request': {'url': 'https://bank-website.com/online-banking'},
                    'response': {
                        'status': 301,
                        'headers': [{'name': 'location', 'value': 'https://fake-banking.scam.com/login'}]
                    },
                    'time': '2024-01-01T10:00:01Z'
                },
                {
                    'request': {'url': 'https://email-provider.com/login'},
                    'response': {
                        'status': 302,
                        'headers': [{'name': 'location', 'value': 'http://phishing-email.com/harvest'}]
                    },
                    'time': '2024-01-01T10:00:02Z'
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/malicious-redirect-test",
            har_data=har_data
        )
        
        malicious_redirect_found = any(
            f['type'] in ['malicious_redirect', 'harmful_redirect'] or
            ('malicious' in f.get('explanation', '').lower() or 'redirect' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert malicious_redirect_found, "Expected detection of malicious redirect"
    
    def test_TC94_url_encoding_attacks(self):
        """TC-94: URL Encoding Attacks - Detect encoded malicious URLs"""
        html_content = """
        <div class="encoding-attacks">
            <a href="https://www.paypal.com/login%00%00%00scam">PayPal Login</a>
            <a href="https://www.amazon.com/deals%0d%0aLocation: http://scam.com">Amazon Deals</a>
            <a href="https://www.google.com/search%20%3Cscript%3Ealert('X')%3C/script%3E">Google Search</a>
            <a href="https://www.facebook.com/login%3Fredirect=http://phishing.com">Facebook Login</a>
        </div>
        <script>
            // JavaScript with encoded URLs
            const encodedUrls = [
                'https://www.paypal.com/login%00%00%00malicious',
                'https://www.amazon.com/deals%0d%0aSet-Cookie: session=stolen',
                'https://www.google.com/search%3Cimg%20src=x%20onerror=alert(1)%3E'
            ];
            
            encodedUrls.forEach(url => {
                const link = document.createElement('a');
                link.href = decodeURIComponent(url);
                link.textContent = 'Special Offer';
                document.querySelector('.encoding-attacks').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/encoding-attack-test",
            html_content=html_content
        )
        
        encoding_attack_found = any(
            f['type'] in ['url_encoding_attack', 'malicious_encoding'] or
            ('encoding' in f.get('explanation', '').lower() or 'url' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert encoding_attack_found, "Expected detection of URL encoding attack"
    
    def test_TC95_protocol_manipulation(self):
        """TC-95: Protocol Manipulation - Detect protocol-based attacks"""
        html_content = """
        <div class="protocol-manipulation">
            <a href="javascript:alert('XSS Attack')">Click Here</a>
            <a href="data:text/html,<script>alert('XSS')</script>">Data URL</a>
            <a href="vbscript:msgbox('VBScript Attack')">VBScript Link</a>
            <a href="file:///C:/Windows/System32/cmd.exe">File Protocol</a>
            <a href="ftp://malicious-server.com/payload.exe">FTP Download</a>
        </div>
        <script>
            // Dynamic protocol manipulation
            const maliciousProtocols = [
                'javascript:document.location="http://scam.com"',
                'data:text/html,<h1>Malicious Content</h1>',
                'vbscript:Execute("malicious code")'
            ];
            
            maliciousProtocols.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.textContent = 'Click for Prize';
                document.querySelector('.protocol-manipulation').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/protocol-manipulation-test",
            html_content=html_content
        )
        
        protocol_manipulation_found = any(
            f['type'] in ['protocol_manipulation', 'malicious_protocol'] or
            ('protocol' in f.get('explanation', '').lower() or 'javascript' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert protocol_manipulation_found, "Expected detection of protocol manipulation"
    
    def test_TC96_query_string_manipulation(self):
        """TC-96: Query String Manipulation - Detect malicious query parameters"""
        html_content = """
        <div class="query-manipulation">
            <a href="https://trusted-site.com/login?redirect=http://phishing.com">Login</a>
            <a href="https://bank-site.com/transfer?to=attacker&amount=1000">Transfer</a>
            <a href="https://email-provider.com/compose?to=spam@scam.com&subject=Phishing">Email</a>
            <a href="https://social-site.com/share?url=http://malicious.com">Share</a>
        </div>
        <script>
            // Dynamic query string manipulation
            const maliciousQueries = [
                'https://paypal.com/login?return_to=http://scam.com',
                'https://amazon.com/checkout?redirect=phishing-site.com',
                'https://google.com/search?q=malicious+site+download+virus'
            ];
            
            maliciousQueries.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.textContent = 'Click Here';
                document.querySelector('.query-manipulation').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/query-manipulation-test",
            html_content=html_content
        )
        
        query_manipulation_found = any(
            f['type'] in ['query_string_manipulation', 'malicious_query'] or
            ('query' in f.get('explanation', '').lower() or 'parameter' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert query_manipulation_found, "Expected detection of query string manipulation"
    
    def test_TC97_fragment_manipulation(self):
        """TC-97: Fragment Manipulation - Detect fragment-based attacks"""
        html_content = """
        <div class="fragment-manipulation">
            <a href="https://trusted-site.com/page#javascript:alert('XSS')">Trusted Link</a>
            <a href="https://bank-site.com/login#data:text/html,<script>alert(1)</script>">Bank Login</a>
            <a href="https://email-site.com/compose#file:///etc/passwd">Email Compose</a>
        </div>
        <script>
            // Dynamic fragment manipulation
            const maliciousFragments = [
                'https://social-site.com/share#javascript:location="http://scam.com"',
                'https://news-site.com/article#data:text/html,<h1>FAKE NEWS</h1>',
                'https://video-site.com/watch#vbscript:msgbox("ATTACK")'
            ];
            
            maliciousFragments.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.textContent = 'Click Here';
                document.querySelector('.fragment-manipulation').appendChild(link);
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/fragment-manipulation-test",
            html_content=html_content
        )
        
        fragment_manipulation_found = any(
            f['type'] in ['fragment_manipulation', 'malicious_fragment'] or
            ('fragment' in f.get('explanation', '').lower() or 'javascript' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert fragment_manipulation_found, "Expected detection of fragment manipulation"
    
    def test_TC98_dns_rebinding_attacks(self):
        """TC-98: DNS Rebinding Attacks - Detect DNS-based attacks"""
        html_content = """
        <div class="dns-rebinding">
            <img src="https://rebind-attack.com/image.jpg" onload="fetch('http://localhost:8080/steal-data')">
            <script src="https://dns-rebind.com/malicious.js"></script>
            <iframe src="https://rebind-target.com/"></iframe>
        </div>
        <script>
            // Simulate DNS rebinding attack
            const rebindingTargets = [
                'https://localhost:8080/admin-panel',
                'https://127.0.0.1:3000/internal-api',
                'https://0.0.0.0:9000/management'
            ];
            
            rebindingTargets.forEach(url => {
                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify({action: 'exfiltrate'})
                });
            });
        </script>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/dns-rebinding-test",
            html_content=html_content
        )
        
        dns_rebinding_found = any(
            f['type'] in ['dns_rebinding', 'rebinding_attack'] or
            ('dns' in f.get('explanation', '').lower() or 'rebind' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert dns_rebinding_found, "Expected detection of DNS rebinding attack"
    
    def test_TC99_cross_site_request_forgery(self):
        """TC-99: Cross-Site Request Forgery - Detect CSRF attacks"""
        html_content = """
        <div class="csrf-attacks">
            <img src="https://bank-site.com/transfer?to=attacker&amount=1000&auto_submit=true" width="1" height="1">
            <form action="https://email-site.com/send" method="POST" id="csrf-form">
                <input type="hidden" name="to" value="spam@scam.com">
                <input type="hidden" name="subject" value="Phishing Email">
                <input type="hidden" name="body" value="Click here to claim prize">
            </form>
            <script>document.getElementById('csrf-form').submit();</script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/csrf-attack-test",
            html_content=html_content
        )
        
        csrf_attack_found = any(
            f['type'] in ['csrf_attack', 'cross_site_request_forgery'] or
            ('csrf' in f.get('explanation', '').lower() or 'forgery' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert csrf_attack_found, "Expected detection of CSRF attack"
    
    def test_TC100_clickjacking_attacks(self):
        """TC-100: Clickjacking Attacks - Detect clickjacking vulnerabilities"""
        html_content = """
        <div class="clickjacking">
            <iframe src="https://bank-site.com/transfer" style="opacity:0.01;position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;"></iframe>
            <div style="position:absolute;top:100px;left:50px;z-index:9999;">
                <button>Click here for amazing deal!</button>
            </div>
            <script>
                // Make iframe clickable
                document.querySelector('iframe').style.pointerEvents = 'auto';
                document.querySelector('iframe').style.opacity = '0.01';
            </script>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com/clickjacking-test",
            html_content=html_content
        )
        
        clickjacking_found = any(
            f['type'] in ['clickjacking', 'ui_redress'] or
            ('clickjack' in f.get('explanation', '').lower() or 'iframe' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert clickjacking_found, "Expected detection of clickjacking attack"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
