"""
Dark Pattern Detection Behavioral & Network Forensics Test Suite
Phase 3: Testing the "lies" in the code (TC-31 to TC-40)
"""

import pytest
import sys
import os
import json
import time
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer
from engines.behavioral_engine import BehavioralEngine

class TestPhase3_BehavioralNetwork:
    """Phase 3: Behavioral & Network (Forensics) Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC31_fake_countdown_reset(self):
        """TC-31: Fake Countdown - Check if timer resets after page refresh"""
        # Simulate HAR data showing countdown that doesn't sync with server
        har_data = {
            'entries': [
                {
                    'request': {
                        'url': 'https://example.com/api/countdown',
                        'method': 'GET'
                    },
                    'response': {
                        'status': 200,
                        'headers': [
                            {'name': 'cache-control', 'value': 'no-cache'},
                            {'name': 'pragma', 'value': 'no-cache'}
                        ],
                        'content': {
                            'text': '{"time": "05:00", "resetOnRefresh": true}'
                        }
                    },
                    'time': datetime.now().isoformat()
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        fake_countdown_found = any(
            f['type'] == 'fake_countdown' or 'countdown' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert fake_countdown_found, "Expected detection of fake countdown timer"
    
    def test_TC32_network_sync_check(self):
        """TC-32: Network Sync - Check if timer data exists in API response"""
        # Simulate HAR with no server-side timer synchronization
        har_data = {
            'entries': [
                {
                    'request': {
                        'url': 'https://example.com/api/timer',
                        'method': 'GET'
                    },
                    'response': {
                        'status': 200,
                        'content': {
                            'text': '{"clientTime": "04:59"}'  # Only client-side time
                        }
                    }
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        sync_issue_found = any(
            f['type'] == 'countdown_sync' or 'sync' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert sync_issue_found, "Expected detection of countdown sync issue"
    
    def test_TC33_fake_activity_notifications(self):
        """TC-33: Fake Activity - Detect JS-generated purchase notifications"""
        # Simulate HAR showing fake activity notifications
        har_data = {
            'entries': [
                {
                    'request': {
                        'url': 'https://example.com/api/activity',
                        'method': 'GET'
                    },
                    'response': {
                        'status': 200,
                        'content': {
                            'text': '{"notifications": [{"user": "John", "action": "purchased", "timestamp": "random"}]}'
                        }
                    }
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        fake_activity_found = any(
            f['type'] == 'fake_activity' or 'activity' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert fake_activity_found, "Expected detection of fake activity notifications"
    
    def test_TC34_hidden_tracking_pixels(self):
        """TC-34: Hidden Tracking - Detect background tracking pings"""
        # Simulate HAR with multiple tracking requests
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://google-analytics.com/collect'},
                    'response': {'status': 200}
                },
                {
                    'request': {'url': 'https://facebook.com/tr'},
                    'response': {'status': 200}
                },
                {
                    'request': {'url': 'https://doubleclick.net/ad'},
                    'response': {'status': 200}
                },
                {
                    'request': {'url': 'https://tracking-pixel.example.com/1x1.gif'},
                    'response': {'status': 200}
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        tracking_found = any(
            f['type'] == 'excessive_tracking' or 'tracking' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert tracking_found, "Expected detection of excessive tracking"
    
    def test_TC35_sneak_into_basket(self):
        """TC-35: Sneak into Basket - Monitor items added without user click"""
        # Simulate HAR showing items added to cart automatically
        har_data = {
            'entries': [
                {
                    'request': {
                        'url': 'https://example.com/api/cart/add',
                        'method': 'POST',
                        'postData': {
                            'text': 'item_id=123&quantity=1&auto_add=true'
                        }
                    },
                    'response': {'status': 200}
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        sneak_basket_found = any(
            f['type'] == 'auto_add' or 'basket' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert sneak_basket_found, "Expected detection of sneak into basket"
    
    def test_TC36_forced_action_email_signup(self):
        """TC-36: Forced Action - Home page inaccessible without email"""
        # Simulate HAR showing redirect to signup page
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/'},
                    'response': {
                        'status': 302,
                        'headers': [
                            {'name': 'location', 'value': 'https://example.com/signup'}
                        ]
                    }
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        forced_action_found = any(
            f['type'] == 'forced_action' or 'forced' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert forced_action_found, "Expected detection of forced action"
    
    def test_TC37_price_flickering(self):
        """TC-37: Price Flickering - Detect price changes based on dwell time"""
        # Simulate HAR showing price changes over time
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/api/price'},
                    'response': {'content': {'text': '{"price": 99.99}'}},
                    'time': '2024-01-01T10:00:00Z'
                },
                {
                    'request': {'url': 'https://example.com/api/price'},
                    'response': {'content': {'text': '{"price": 129.99}'}},
                    'time': '2024-01-01T10:05:00Z'
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        price_flicker_found = any(
            f['type'] == 'price_flickering' or 'price' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert price_flicker_found, "Expected detection of price flickering"
    
    def test_TC38_cookie_walls(self):
        """TC-38: Cookie Walls - Detect if "Reject All" leads to broken site"""
        # Simulate HAR showing broken experience after rejecting cookies
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/api/cookies/reject'},
                    'response': {'status': 500}
                },
                {
                    'request': {'url': 'https://example.com/content'},
                    'response': {'status': 403, 'content': {'text': 'Cookies required'}}
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        cookie_wall_found = any(
            f['type'] == 'cookie_wall' or 'cookie' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert cookie_wall_found, "Expected detection of cookie wall"
    
    def test_TC39_hardcoded_lies(self):
        """TC-39: Hardcoded Lies - Check if "people viewing" is random generator"""
        # Simulate HAR showing inconsistent "people viewing" numbers
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/api/viewers'},
                    'response': {'content': {'text': '{"viewers": 1234}'}},
                    'time': '2024-01-01T10:00:00Z'
                },
                {
                    'request': {'url': 'https://example.com/api/viewers'},
                    'response': {'content': {'text': '{"viewers": 5678}'}},
                    'time': '2024-01-01T10:00:01Z'
                },
                {
                    'request': {'url': 'https://example.com/api/viewers'},
                    'response': {'content': {'text': '{"viewers": 9012}'}},
                    'time': '2024-01-01T10:00:02Z'
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        hardcoded_lies_found = any(
            f['type'] == 'fake_social_proof' or 'random' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert hardcoded_lies_found, "Expected detection of hardcoded lies"
    
    def test_TC40_subscription_trap(self):
        """TC-40: Subscription Trap - "Cancel" requires more clicks than "Sign Up" """
        # Simulate HAR showing complex cancellation flow
        har_data = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/signup', 'method': 'POST'},
                    'response': {'status': 200}
                },
                {
                    'request': {'url': 'https://example.com/cancel/step1'},
                    'response': {'status': 302, 'headers': [{'name': 'location', 'value': '/cancel/step2'}]}
                },
                {
                    'request': {'url': 'https://example.com/cancel/step2'},
                    'response': {'status': 302, 'headers': [{'name': 'location', 'value': '/cancel/step3'}]}
                },
                {
                    'request': {'url': 'https://example.com/cancel/step3'},
                    'response': {'status': 302, 'headers': [{'name': 'location', 'value': '/cancel/confirm'}]}
                },
                {
                    'request': {'url': 'https://example.com/cancel/confirm'},
                    'response': {'status': 200}
                }
            ]
        }
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            har_data=har_data
        )
        
        subscription_trap_found = any(
            f['type'] == 'subscription_trap' or 'cancel' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert subscription_trap_found, "Expected detection of subscription trap"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
