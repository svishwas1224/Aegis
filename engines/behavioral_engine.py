"""
Aegis Pro Behavioral Engine
Analyzes network behavior and user interactions for dark patterns
"""

import json
import re
from typing import Dict, List, Any
from urllib.parse import urlparse
import time

class BehavioralEngine:
    def __init__(self):
        self.suspicious_patterns = {
            'fake_countdown': [
                r'resetOnRefresh["\']?\s*:\s*true',
                r'"resetOnRefresh"\s*:\s*true',
                r'"time"\s*:\s*"\d+:\d+"',
                r'countdown.*reset',
                r'timer.*reset.*refresh',
                r'fake.*countdown',
                r'simulated.*timer',
                r'countdown.*\d+.*seconds?',
                r'ends in.*\d+.*minutes?',
                r'limited time.*\d+.*hours?'
            ],
            'price_manipulation': [
                r'was.*\$\d+.*now.*\$\d+',
                r'save.*\$\d+.*today',
                r'flash sale.*\$\d+'
            ],
            'forced_actions': [
                r'subscribe.*to continue',
                r'share.*to unlock',
                r'login.*to proceed'
            ]
        }
    
    def analyze_har(self, har_data: Dict) -> Dict[str, Any]:
        """Analyze HAR (HTTP Archive) for behavioral patterns"""
        findings = []
        total_penalty = 0
        
        if not har_data or 'entries' not in har_data:
            return {'findings': [], 'trust_score': 100}
        
        entries = har_data.get('entries', [])
        
        # Analyze response patterns
        countdown_findings = self._detect_fake_countdowns(entries)
        findings.extend(countdown_findings)
        total_penalty += sum(f.get('severity_score', 10) for f in countdown_findings)
        
        # Analyze network sync issues
        sync_findings = self._detect_sync_issues(entries)
        findings.extend(sync_findings)
        total_penalty += sum(f.get('severity_score', 15) for f in sync_findings)
        
        # Analyze fake activity notifications
        activity_findings = self._detect_fake_activity(entries)
        findings.extend(activity_findings)
        total_penalty += sum(f.get('severity_score', 15) for f in activity_findings)
        
        # Analyze sneak into basket
        basket_findings = self._detect_sneak_basket(entries)
        findings.extend(basket_findings)
        total_penalty += sum(f.get('severity_score', 20) for f in basket_findings)
        
        # Analyze price flickering
        price_findings = self._detect_price_flickering(entries)
        findings.extend(price_findings)
        total_penalty += sum(f.get('severity_score', 25) for f in price_findings)
        
        # Analyze cookie walls
        cookie_findings = self._detect_cookie_walls(entries)
        findings.extend(cookie_findings)
        total_penalty += sum(f.get('severity_score', 20) for f in cookie_findings)
        
        # Analyze hardcoded lies
        lies_findings = self._detect_hardcoded_lies(entries)
        findings.extend(lies_findings)
        total_penalty += sum(f.get('severity_score', 15) for f in lies_findings)
        
        # Analyze tracking
        tracking_findings = self._analyze_tracking(entries)
        findings.extend(tracking_findings)
        total_penalty += sum(f.get('severity_score', 5) for f in tracking_findings)
        
        # Analyze redirect chains
        redirect_findings = self._analyze_redirects(entries)
        findings.extend(redirect_findings)
        total_penalty += sum(f.get('severity_score', 8) for f in redirect_findings)
        
        # Analyze forced actions
        forced_action_findings = self._analyze_forced_actions(entries)
        findings.extend(forced_action_findings)
        total_penalty += sum(f.get('severity_score', 20) for f in forced_action_findings)
        
        # Analyze subscription traps
        subscription_trap_findings = self._analyze_subscription_traps(entries)
        findings.extend(subscription_trap_findings)
        total_penalty += sum(f.get('severity_score', 25) for f in subscription_trap_findings)
        
        base_score = 100
        final_score = max(0, base_score - total_penalty)
        
        return {
            'findings': findings,
            'trust_score': final_score,
            'patterns_detected': len(findings),
            'analysis_type': 'behavioral'
        }
    
    def _detect_fake_countdowns(self, entries: List[Dict]) -> List[Dict]:
        """Detect fake countdown timers"""
        findings = []
        
        for entry in entries:
            response = entry.get('response', {})
            content = response.get('content', {})
            text = content.get('text', '')
            
            if not text:
                continue
                
            # Look for countdown patterns
            for pattern_type, patterns in self.suspicious_patterns.items():
                if pattern_type != 'fake_countdown':
                    continue
                    
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        # Check if this is a real countdown or fake
                        if self._is_fake_countdown(entry, match.group()):
                            findings.append({
                                'engine': 'BEHAVIORAL',
                                'type': 'fake_countdown',
                                'severity': 'HIGH',
                                'source_text': match.group(),
                                'evidence': {'url': entry.get('request', {}).get('url')},
                                'remediation': 'Use real-time countdowns or remove artificial urgency',
                                'explanation': 'Countdown timer appears to be fake or manipulated',
                                'severity_score': 25
                            })
        
        return findings
    
    def _analyze_tracking(self, entries: List[Dict]) -> List[Dict]:
        """Analyze excessive tracking"""
        findings = []
        
        tracking_domains = [
            'google-analytics', 'facebook.com/tr', 'doubleclick', 
            'googletagmanager', 'facebook.net', 'googlesyndication',
            'tracking-pixel', 'analytics', 'pixel', 'tracker'
        ]
        
        tracking_count = 0
        tracking_urls = []
        for entry in entries:
            url = entry.get('request', {}).get('url', '')
            if any(domain in url for domain in tracking_domains):
                tracking_count += 1
                tracking_urls.append(url)
        
        if tracking_count >= 3:  # Lower threshold for testing
            findings.append({
                'engine': 'BEHAVIORAL',
                'type': 'excessive_tracking',
                'severity': 'MEDIUM',
                'source_text': f'{tracking_count} tracking requests detected',
                'evidence': {'tracking_count': tracking_count},
                'remediation': 'Reduce tracking scripts to essential ones only',
                'explanation': f'Excessive tracking ({tracking_count} requests) may compromise user privacy',
                'severity_score': 15
            })
        
        return findings
    
    def _analyze_redirects(self, entries: List[Dict]) -> List[Dict]:
        """Analysis redirect chains"""
        findings = []
        
        redirect_count = 0
        for entry in entries:
            response = entry.get('response', {})
            if response.get('status', 0) in [301, 302, 303, 307, 308]:
                redirect_count += 1
        
        if redirect_count > 3:
            findings.append({
                'engine': 'BEHAVIORAL',
                'type': 'excessive_redirects',
                'severity': 'MEDIUM',
                'source_text': f'{redirect_count} redirects detected',
                'evidence': {'redirect_count': redirect_count},
                'remediation': 'Simplify URL structure to reduce redirects',
                'explanation': f'Excessive redirects ({redirect_count}) may indicate suspicious behavior',
                'severity_score': 12
            })
        
        return findings
    
    def _is_fake_countdown(self, entry: Dict, countdown_text: str) -> bool:
        """Determine if countdown is likely fake"""
        # Check if countdown is hardcoded in response
        response = entry.get('response', {})
        headers = response.get('headers', [])
        
        # Look for cache headers
        cache_control = ''
        pragma = ''
        for header in headers:
            header_name = header.get('name', '').lower()
            header_value = header.get('value', '')
            
            if header_name == 'cache-control':
                cache_control = header_value
            elif header_name == 'pragma':
                pragma = header_value
        
        # Check for fake countdown indicators
        fake_indicators = [
            'resetOnRefresh' in countdown_text,
            'resetOnRefresh' in countdown_text,
            '"time"' in countdown_text and '":' in countdown_text,
            'no-cache' in cache_control,
            'no-cache' in pragma
        ]
        
        # If content is cached for long time, countdown is likely fake
        if 'max-age=' in cache_control:
            try:
                max_age = int(cache_control.split('max-age=')[1].split(',')[0])
                if max_age > 3600:  # More than 1 hour
                    return True
            except:
                pass
        
        # If any fake indicators are present, it's likely fake
        if any(fake_indicators):
            return True
        
        return False
    
    def _analyze_forced_actions(self, entries: List[Dict]) -> List[Dict]:
        """Analyze forced action patterns"""
        findings = []
        
        for entry in entries:
            response = entry.get('response', {})
            status = response.get('status', 0)
            headers = response.get('headers', [])
            request_url = entry.get('request', {}).get('url', '')
            
            # Check for redirects to signup/login pages
            if status in [301, 302, 303, 307, 308]:
                location_header = None
                for header in headers:
                    if header.get('name', '').lower() == 'location':
                        location_header = header.get('value', '')
                        break
                
                if location_header and any(keyword in location_header.lower() for keyword in ['signup', 'login', 'register', 'auth']):
                    findings.append({
                        'engine': 'BEHAVIORAL',
                        'type': 'forced_action',
                        'severity': 'HIGH',
                        'source_text': f'Redirect to {location_header}',
                        'evidence': {'redirect_url': location_header, 'original_url': request_url},
                        'remediation': 'Allow access to content without forced authentication',
                        'explanation': 'Forced action detected - user redirected to signup/login page',
                        'severity_score': 25
                    })
            
            # Check for 403 errors requiring authentication
            if status == 403:
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'forced_action',
                    'severity': 'MEDIUM',
                    'source_text': f'Access denied (403) for {request_url}',
                    'evidence': {'status_code': status, 'url': request_url},
                    'remediation': 'Provide content access without mandatory authentication',
                    'explanation': 'Content blocked behind authentication wall',
                    'severity_score': 15
                })
        
        return findings
    
    def _analyze_subscription_traps(self, entries: List[Dict]) -> List[Dict]:
        """Analyze subscription trap patterns"""
        findings = []
        
        signup_count = 0
        cancel_steps = []
        
        for entry in entries:
            url = entry.get('request', {}).get('url', '')
            method = entry.get('request', {}).get('method', 'GET')
            response = entry.get('response', {})
            status = response.get('status', 0)
            
            # Count signup requests
            if 'signup' in url and method == 'POST':
                signup_count += 1
            
            # Track cancellation flow complexity
            if 'cancel' in url:
                cancel_steps.append(url)
                if status in [301, 302, 303, 307, 308]:
                    # Check if redirect leads to another cancel step
                    headers = response.get('headers', [])
                    for header in headers:
                        if header.get('name', '').lower() == 'location':
                            location = header.get('value', '')
                            if 'cancel' in location:
                                cancel_steps.append(location)
        
        # Detect subscription trap if cancel requires more steps than signup
        if len(cancel_steps) >= 3 and signup_count > 0:
            findings.append({
                'engine': 'BEHAVIORAL',
                'type': 'subscription_trap',
                'severity': 'HIGH',
                'source_text': f'Complex cancellation flow with {len(cancel_steps)} steps',
                'evidence': {'cancel_steps': len(cancel_steps), 'signup_count': signup_count},
                'remediation': 'Simplify cancellation process to match signup complexity',
                'explanation': f'Subscription trap detected - cancellation requires {len(cancel_steps)} steps vs simple signup',
                'severity_score': 30
            })
        
        return findings
    
    def _detect_sync_issues(self, entries: List[Dict]) -> List[Dict]:
        """Detect network sync issues with countdowns"""
        findings = []
        
        for entry in entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            response = entry.get('response', {})
            content = response.get('content', {})
            text = content.get('text', '')
            
            if not text:
                continue
            
            # Look for client-side only timer data
            sync_patterns = [
                r'clientTime["\']?\s*:\s*["\']?\d+:\d+["\']?',
                r'"clientTime"',
                r'"localTime"',
                r'"browserTime"',
                r'"currentTime"'
            ]
            
            # Check if response contains only client-side time
            has_client_time = any(pattern in text for pattern in sync_patterns)
            has_server_time = 'serverTime' in text or 'server_time' in text
            
            if has_client_time and not has_server_time:
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'countdown_sync',
                    'severity': 'HIGH',
                    'source_text': text[:100] + '...' if len(text) > 100 else text,
                    'evidence': {'url': url, 'has_client_time': has_client_time, 'has_server_time': has_server_time},
                    'remediation': 'Synchronize timer with server time to prevent manipulation',
                    'explanation': 'Countdown timer not synchronized with server - vulnerable to manipulation',
                    'severity_score': 20
                })
        
        return findings
    
    def _detect_fake_activity(self, entries: List[Dict]) -> List[Dict]:
        """Detect fake activity notifications"""
        findings = []
        
        for entry in entries:
            response = entry.get('response', {})
            content = response.get('content', {})
            text = content.get('text', '')
            
            if not text:
                continue
            
            # Look for fake activity patterns
            activity_patterns = [
                r'user.*purchased.*\d+.*seconds? ago',
                r'\d+.*people.*viewing.*right now',
                r'just.*sold.*in.*your area',
                r'join.*\d+.*customers.*today',
                r'"action":\s*"purchased"',
                r'"timestamp":\s*"random"',
                r'"notifications":\[.*"purchased"',
                r'"user":.*"action":.*"purchased"'
            ]
            
            for pattern in activity_patterns:
                import re
                if re.search(pattern, text, re.IGNORECASE):
                    findings.append({
                        'engine': 'BEHAVIORAL',
                        'type': 'fake_activity',
                        'severity': 'HIGH',
                        'source_text': text,
                        'evidence': {'url': entry.get('request', {}).get('url'), 'pattern_matched': pattern},
                        'remediation': 'Remove fake activity notifications or use real data',
                        'explanation': 'Fake activity notification detected - appears to be generated to create false urgency',
                        'severity_score': 25
                    })
                    break
        
        return findings
    
    def _detect_sneak_basket(self, entries: List[Dict]) -> List[Dict]:
        """Detect items added to cart without user interaction"""
        findings = []
        
        for entry in entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            method = request.get('method', '')
            post_data = request.get('postData', {})
            
            # Look for automatic cart additions
            if 'cart' in url.lower() and method == 'POST':
                data_text = post_data.get('text', '')
                
                suspicious_patterns = [
                    'auto_add=true',
                    'automatic=true',
                    'silent_add=true',
                    'background_add=true'
                ]
                
                if any(pattern in data_text for pattern in suspicious_patterns):
                    findings.append({
                        'engine': 'BEHAVIORAL',
                        'type': 'auto_add',
                        'severity': 'HIGH',
                        'source_text': f'Automatic cart addition: {data_text}',
                        'evidence': {'url': url, 'post_data': data_text},
                        'remediation': 'Remove automatic cart additions without user consent',
                        'explanation': 'Item added to cart automatically without user interaction',
                        'severity_score': 30
                    })
        
        return findings
    
    def _detect_price_flickering(self, entries: List[Dict]) -> List[Dict]:
        """Detect price changes over time"""
        findings = []
        
        price_entries = []
        for entry in entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            
            if 'price' in url.lower() or 'pricing' in url.lower():
                response = entry.get('response', {})
                content = response.get('content', {})
                text = content.get('text', '')
                
                # Extract price from response
                import re
                # Try JSON format first
                json_price_match = re.search(r'"price"\s*:\s*(\d+\.?\d*)', text)
                if json_price_match:
                    price = float(json_price_match.group(1))
                    timestamp = entry.get('time', '')
                    price_entries.append({'price': price, 'time': timestamp, 'url': url})
                else:
                    # Try dollar sign format
                    price_match = re.search(r'\$\s*(\d+\.?\d*)', text)
                    if price_match:
                        price = float(price_match.group(1))
                        timestamp = entry.get('time', '')
                        price_entries.append({'price': price, 'time': timestamp, 'url': url})
        
        # Check for price variations
        if len(price_entries) >= 2:
            prices = [entry['price'] for entry in price_entries]
            min_price = min(prices)
            max_price = max(prices)
            
            # If price varies significantly
            if (max_price - min_price) / min_price > 0.1:  # 10% variation
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'price_flickering',
                    'severity': 'HIGH',
                    'source_text': f'Price range: ${min_price:.2f} - ${max_price:.2f}',
                    'evidence': {'price_range': [min_price, max_price], 'entries': price_entries},
                    'remediation': 'Use consistent pricing or clearly explain price changes',
                    'explanation': f'Price flickering detected - price varies by {(max_price/min_price - 1)*100:.1f}%',
                    'severity_score': 30
                })
        
        return findings
    
    def _detect_cookie_walls(self, entries: List[Dict]) -> List[Dict]:
        """Detect cookie walls that block content"""
        findings = []
        
        cookie_reject_responses = []
        content_access_responses = []
        
        for entry in entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            response = entry.get('response', {})
            status = response.get('status', 0)
            
            # Track cookie rejection responses
            if 'cookie' in url.lower() and 'reject' in url.lower():
                cookie_reject_responses.append({'status': status, 'url': url})
            
            # Track content access attempts
            if 'content' in url.lower() or 'page' in url.lower():
                content_access_responses.append({'status': status, 'url': url})
        
        # Check if rejecting cookies leads to content blocking
        if cookie_reject_responses and content_access_responses:
            reject_errors = sum(1 for r in cookie_reject_responses if r['status'] >= 400)
            content_errors = sum(1 for c in content_access_responses if c['status'] >= 400)
            
            if reject_errors > 0 and content_errors > 0:
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'cookie_wall',
                    'severity': 'HIGH',
                    'source_text': f'Cookie rejection leads to {content_errors} access errors',
                    'evidence': {'reject_errors': reject_errors, 'content_errors': content_errors},
                    'remediation': 'Allow content access regardless of cookie preferences',
                    'explanation': 'Cookie wall detected - rejecting cookies blocks content access',
                    'severity_score': 25
                })
        
        return findings
    
    def _detect_hardcoded_lies(self, entries: List[Dict]) -> List[Dict]:
        """Detect hardcoded fake numbers and statistics"""
        findings = []
        
        # Track "people viewing" numbers over time
        viewer_numbers = []
        for entry in entries:
            request = entry.get('request', {})
            url = request.get('url', '')
            
            if 'viewers' in url.lower() or 'people' in url.lower():
                response = entry.get('response', {})
                content = response.get('content', {})
                text = content.get('text', '')
                
                import re
                # Look for people/viewers numbers
                number_match = re.search(r'"viewers":\s*(\d+)', text) or re.search(r'"people":\s*(\d+)', text)
                if number_match:
                    number = int(number_match.group(1))
                    timestamp = entry.get('time', '')
                    viewer_numbers.append({'number': number, 'time': timestamp, 'url': url})
        
        # Check for random-looking numbers
        if len(viewer_numbers) >= 3:
            numbers = [entry['number'] for entry in viewer_numbers]
            
            # Calculate variance
            if len(numbers) > 1:
                avg = sum(numbers) / len(numbers)
                variance = sum((x - avg) ** 2 for x in numbers) / len(numbers)
                
                # High variance suggests fake/random numbers
                if variance > avg * avg * 0.1:  # Lower threshold for better detection
                    findings.append({
                        'engine': 'BEHAVIORAL',
                        'type': 'fake_social_proof',
                        'severity': 'HIGH',
                        'source_text': f'Viewer numbers: {numbers}',
                        'evidence': {'numbers': numbers, 'variance': variance},
                        'remediation': 'Use real-time data or remove fake statistics',
                        'explanation': 'Hardcoded fake social proof detected - numbers appear to be randomly generated',
                        'severity_score': 20
                    })
        
        return findings
    
    def analyze_dom_changes(self, dom_changes: List[Dict]) -> Dict[str, Any]:
        """Analyze DOM mutations for behavioral patterns"""
        findings = []
        total_penalty = 0
        
        for change in dom_changes:
            change_type = change.get('type', '')
            
            if change_type == 'price_change':
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'dynamic_price_change',
                    'severity': 'HIGH',
                    'source_text': f"Price changed from {change.get('old_price')} to {change.get('new_price')}",
                    'evidence': change,
                    'remediation': 'Avoid dynamic price changes based on user behavior',
                    'explanation': 'Price changed dynamically, potentially based on user behavior',
                    'severity_score': 30
                })
                total_penalty += 30
                
            elif change_type == 'content_injection':
                findings.append({
                    'engine': 'BEHAVIORAL',
                    'type': 'content_injection',
                    'severity': 'MEDIUM',
                    'source_text': 'Content dynamically injected',
                    'evidence': change,
                    'remediation': 'Be transparent about dynamic content changes',
                    'explanation': 'Content was dynamically injected into the page',
                    'severity_score': 15
                })
                total_penalty += 15
        
        base_score = 100
        final_score = max(0, base_score - total_penalty)
        
        return {
            'findings': findings,
            'trust_score': final_score,
            'patterns_detected': len(findings),
            'analysis_type': 'behavioral_dom'
        }
