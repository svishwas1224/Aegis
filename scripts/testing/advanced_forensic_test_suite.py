#!/usr/bin/env python3
"""
Aegis Pro Advanced Forensic Testing Suite
Tests 20 complex websites with sophisticated dark pattern detection
"""

import requests
import time
import re
import json
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from engines.tri_engine_analyzer import TriEngineAnalyzer

class AdvancedForensicTester:
    def __init__(self):
        self.engine = TriEngineAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Advanced forensic pattern definitions
        self.forensic_patterns = {
            # Complex E-commerce & Retail
            'shein.com': {
                'patterns': [r'low\s*stock', r'limited\s*quantity', r'almost\s*gone', r'only\s+\d+\s*left', r'high\s*demand'],
                'category': 'Fake Scarcity/Nagging',
                'challenge': 'Heavy use of "Low Stock" messages and forced registration popups',
                'forensic_indicators': ['dynamic_stock', 'forced_registration', 'nagging_popups']
            },
            'sportsdirect.com': {
                'patterns': [r'auto.*add.*cart', r'magazine.*added', r'bag.*included', r'pre.*selected.*item'],
                'category': 'Sneak into Basket',
                'challenge': 'Historically adds magazines/bags to the cart automatically',
                'forensic_indicators': ['auto_cart_addition', 'hidden_items', 'preselected_products']
            },
            'zomato.com': {
                'patterns': [r'donation.*pre.*checked', r'insurance.*auto.*add', r'tip.*pre.*selected', r'service.*fee.*hidden'],
                'category': 'Sneak into Basket',
                'challenge': 'Often pre-checks "Donation" or "Insurance" boxes in the cart',
                'forensic_indicators': ['preselected_donation', 'hidden_insurance', 'auto_add_fees']
            },
            'nykaa.com': {
                'patterns': [r'cancel.*hard.*to.*find', r'delete.*requires.*support', r'account.*deletion.*hidden', r'contact.*support.*to.*cancel'],
                'category': 'Roach Motel',
                'challenge': 'Easy signup, but account deletion is famously hard to find/requires manual support',
                'forensic_indicators': ['hidden_cancellation', 'support_required', 'complex_deletion']
            },
            'temu.com': {
                'patterns': [r'spin.*wheel', r'countdown.*game', r'fomo.*urgency', r'gamified.*purchase', r'limited.*time.*offer'],
                'category': 'Gamified Urgency',
                'challenge': 'Uses "Spin the Wheel" and fake countdowns to create FOMO',
                'forensic_indicators': ['gamification', 'fake_countdown', 'fomo_tactics']
            },
            'groupon.com': {
                'patterns': [r'low.*price.*restrictive', r'conditions.*apply', r'only.*available.*if', r'restrictions.*hidden'],
                'category': 'Bait & Switch',
                'challenge': 'Highlighting a low price that is only available under restrictive conditions',
                'forensic_indicators': ['hidden_conditions', 'restrictive_pricing', 'bait_switch']
            },
            
            # Digital Services & SaaS
            'canva.com': {
                'patterns': [r'free.*subscription.*wall', r'trial.*auto.*renew', r'hidden.*subscription', r'paid.*plan.*required'],
                'category': 'Forced Continuity',
                'challenge': '"Free" elements that lead to a subscription wall late in the design process',
                'forensic_indicators': ['subscription_wall', 'free_to_paid', 'late_subscription']
            },
            'lumosme.com': {
                'patterns': [r'trial.*to.*annual', r'hidden.*auto.*renew', r'small.*font.*terms', r'annual.*commitment.*hidden'],
                'category': 'Hidden Subscription',
                'challenge': 'Often hides the transition from a "trial" to a high-cost annual plan',
                'forensic_indicators': ['trial_trap', 'hidden_annual', 'small_font_terms']
            },
            'noom.com': {
                'patterns': [r'long.*onboarding', r'investment.*buildup', r'prices.*hidden.*until.*end', r'quiz.*before.*pricing'],
                'category': 'Hard to Cancel',
                'challenge': 'Uses long onboarding quizzes to build "investment" before showing prices',
                'forensic_indicators': ['investment_quiz', 'delayed_pricing', 'commitment_trap']
            },
            'match.com': {
                'patterns': [r'multi.*step.*deactivate', r'complex.*cancellation', r'delete.*account.*hard', r'multiple.*steps.*cancel'],
                'category': 'Roach Motel',
                'challenge': 'Extremely complex multi-step process to deactivate or delete',
                'forensic_indicators': ['complex_cancellation', 'multi_step_process', 'hard_to_delete']
            },
            'scribd.com': {
                'patterns': [r'auto.*renew.*small.*font', r'free.*trial.*hidden.*terms', r'subscription.*auto.*charge', r'terms.*hidden'],
                'category': 'Hidden Fee/Continuity',
                'challenge': 'Hides auto-renewal terms in small font during "Free Trial" signup',
                'forensic_indicators': ['hidden_auto_renew', 'small_font_terms', 'trial_trap']
            },
            
            # Media & News
            'wired.com': {
                'patterns': [r'cancel.*requires.*live.*agent', r'call.*to.*cancel', r'chat.*required.*cancel', r'phone.*support.*cancel'],
                'category': 'Hard to Cancel',
                'challenge': 'Subscription cancellation often requires a live agent chat/call',
                'forensic_indicators': ['live_agent_required', 'phone_cancellation', 'support_trap']
            },
            'independent.co.uk': {
                'patterns': [r'reject.*all.*hidden', r'cookie.*banner.*layers', r'multiple.*steps.*reject', r'privacy.*settings.*complex'],
                'category': 'Obstruction',
                'challenge': 'Cookie banners designed with "Reject All" hidden behind 3+ layers',
                'forensic_indicators': ['hidden_reject', 'cookie_obstruction', 'privacy_complexity']
            },
            'dailymail.co.uk': {
                'patterns': [r'sponsored.*content.*same.*css', r'native.*ad.*article', r'advertisement.*disguised', r'paid.*content.*news'],
                'category': 'Disguised Ads',
                'challenge': '"Sponsored Content" that uses the exact same CSS as real news articles',
                'forensic_indicators': ['native_ad_disguise', 'css_matching', 'ad_disguise']
            },
            'hbr.org': {
                'patterns': [r'read.*\d+.*more.*free', r'paywall.*registration', r'forced.*action.*continue', r'sign.*up.*read'],
                'category': 'Paywall Wall',
                'challenge': '"Read 2 more articles for free" (Forced Action/Registration)',
                'forensic_indicators': ['paywall_trap', 'forced_registration', 'article_limit']
            },
            
            # Travel & Booking
            'skyscanner.net': {
                'patterns': [r'price.*change.*rapidly', r'price.*drip.*between.*pages', r'dynamic.*pricing', r'price.*increase'],
                'category': 'Price Drip',
                'challenge': 'Prices change rapidly between the search result and the provider\'s site',
                'forensic_indicators': ['price_drip', 'dynamic_pricing', 'rapid_price_change']
            },
            'travelocity.com': {
                'patterns': [r'someone.*just.*booked', r'people.*looking.*now', r'dynamic.*popup', r'social.*proof.*pressure'],
                'category': 'Social Pressure',
                'challenge': '"Someone in Mumbai just booked this" dynamic popups',
                'forensic_indicators': ['dynamic_social_proof', 'fake_activity', 'pressure_popups']
            },
            'frontier.com': {
                'patterns': [r'no.*seat.*selection.*error', r'free.*looks.*like.*error', r'misleading.*ui', r'visual.*interference'],
                'category': 'Visual Interference',
                'challenge': 'Making "No Seat Selection" (Free) look like an error message',
                'forensic_indicators': ['visual_deception', 'error_misleading', 'ui_interference']
            },
            'vueling.com': {
                'patterns': [r'accept.*continue.*extra.*charges', r'trick.*wording', r'misleading.*button', r'hidden.*fees'],
                'category': 'Trick Wording',
                'challenge': 'Using "Accept & Continue" to mean "Accept Extra Charges"',
                'forensic_indicators': ['misleading_labels', 'hidden_charges', 'trick_wording']
            },
            'hostelworld.com': {
                'patterns': [r'limited.*time.*offer', r'evergreen.*timer', r'timer.*reset', r'fake.*countdown', r'perpetual.*urgency'],
                'category': 'Limited Time Offer',
                'challenge': 'Evergreen timers that reset every time you re-enter the site',
                'forensic_indicators': ['evergreen_timer', 'reset_countdown', 'perpetual_urgency']
            }
        }
    
    def fetch_website_content(self, url, timeout=20):
        """Fetch website content for forensic analysis"""
        try:
            print(f"Fetching content from: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract relevant content
            content = {
                'url': url,
                'html_content': str(soup),
                'title': soup.title.string if soup.title else '',
                'text_content': soup.get_text(),
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.content)
            }
            
            return content
            
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def analyze_forensic_patterns(self, site_data):
        """Analyze website with forensic pattern detection"""
        url = site_data['url']
        domain = urlparse(url).netloc.lower()
        
        print(f"\n{'='*80}")
        print(f"FORENSIC ANALYSIS: {site_data['name']}")
        print(f"URL: {url}")
        print(f"Pattern: {site_data['pattern']}")
        print(f"Challenge: {site_data['challenge']}")
        print(f"{'='*80}")
        
        # Fetch content
        content = self.fetch_website_content(url)
        if not content:
            return None
        
        # Perform tri-engine analysis
        start_time = time.time()
        result = self.engine.analyze_comprehensive(
            url=url,
            html_content=content['html_content']
        )
        end_time = time.time()
        
        # Enhanced forensic detection
        forensic_findings = self.detect_forensic_patterns(content, domain)
        
        # Generate detailed report
        report = {
            'name': site_data['name'],
            'url': url,
            'domain': domain,
            'pattern': site_data['pattern'],
            'challenge': site_data['challenge'],
            'title': content['title'],
            'trust_score': result['trust_score'],
            'risk_level': self.get_risk_level(result['trust_score']),
            'analysis_time': f"{end_time - start_time:.3f}s",
            'findings_count': len(result['findings']),
            'findings': result['findings'],
            'forensic_findings': forensic_findings,
            'engines_used': result.get('engines_used', []),
            'content_length': content['content_length']
        }
        
        self.print_forensic_analysis_report(report)
        return report
    
    def detect_forensic_patterns(self, content, domain):
        """Detect advanced forensic patterns"""
        text_content = content['text_content']
        html_content = content['html_content']
        
        forensic_findings = []
        
        # Get domain-specific forensic patterns
        if domain in self.forensic_patterns:
            pattern_def = self.forensic_patterns[domain]
            patterns = pattern_def['patterns']
            category = pattern_def['category']
            challenge = pattern_def['challenge']
            forensic_indicators = pattern_def['forensic_indicators']
            
            # Text-based pattern detection
            for pattern in patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                if matches:
                    confidence = min(98, 85 + len(matches) * 3)
                    forensic_findings.append({
                        'pattern': matches[0],
                        'category': category,
                        'confidence': confidence,
                        'matches': len(matches),
                        'type': 'text_pattern'
                    })
            
            # Advanced forensic indicator detection
            for indicator in forensic_indicators:
                indicator_findings = self.detect_forensic_indicator(html_content, indicator, category)
                forensic_findings.extend(indicator_findings)
        
        return forensic_findings
    
    def detect_forensic_indicator(self, html_content, indicator, category):
        """Detect specific forensic indicators"""
        findings = []
        
        indicator_detections = {
            'dynamic_stock': self.detect_dynamic_stock(html_content),
            'forced_registration': self.detect_forced_registration(html_content),
            'nagging_popups': self.detect_nagging_popups(html_content),
            'auto_cart_addition': self.detect_auto_cart_addition(html_content),
            'hidden_items': self.detect_hidden_items(html_content),
            'preselected_products': self.detect_preselected_products(html_content),
            'preselected_donation': self.detect_preselected_donation(html_content),
            'hidden_insurance': self.detect_hidden_insurance(html_content),
            'auto_add_fees': self.detect_auto_add_fees(html_content),
            'hidden_cancellation': self.detect_hidden_cancellation(html_content),
            'support_required': self.detect_support_required(html_content),
            'complex_deletion': self.detect_complex_deletion(html_content),
            'gamification': self.detect_gamification(html_content),
            'fake_countdown': self.detect_fake_countdown(html_content),
            'fomo_tactics': self.detect_fomo_tactics(html_content),
            'hidden_conditions': self.detect_hidden_conditions(html_content),
            'restrictive_pricing': self.detect_restrictive_pricing(html_content),
            'bait_switch': self.detect_bait_switch(html_content),
            'subscription_wall': self.detect_subscription_wall(html_content),
            'free_to_paid': self.detect_free_to_paid(html_content),
            'late_subscription': self.detect_late_subscription(html_content),
            'trial_trap': self.detect_trial_trap(html_content),
            'hidden_annual': self.detect_hidden_annual(html_content),
            'small_font_terms': self.detect_small_font_terms(html_content),
            'investment_quiz': self.detect_investment_quiz(html_content),
            'delayed_pricing': self.detect_delayed_pricing(html_content),
            'commitment_trap': self.detect_commitment_trap(html_content),
            'complex_cancellation': self.detect_complex_cancellation(html_content),
            'multi_step_process': self.detect_multi_step_process(html_content),
            'hard_to_delete': self.detect_hard_to_delete(html_content),
            'live_agent_required': self.detect_live_agent_required(html_content),
            'phone_cancellation': self.detect_phone_cancellation(html_content),
            'support_trap': self.detect_support_trap(html_content),
            'hidden_reject': self.detect_hidden_reject(html_content),
            'cookie_obstruction': self.detect_cookie_obstruction(html_content),
            'privacy_complexity': self.detect_privacy_complexity(html_content),
            'native_ad_disguise': self.detect_native_ad_disguise(html_content),
            'css_matching': self.detect_css_matching(html_content),
            'ad_disguise': self.detect_ad_disguise(html_content),
            'paywall_trap': self.detect_paywall_trap(html_content),
            'forced_registration': self.detect_forced_registration_wall(html_content),
            'article_limit': self.detect_article_limit(html_content),
            'price_drip': self.detect_price_drip(html_content),
            'dynamic_pricing': self.detect_dynamic_pricing(html_content),
            'rapid_price_change': self.detect_rapid_price_change(html_content),
            'dynamic_social_proof': self.detect_dynamic_social_proof(html_content),
            'fake_activity': self.detect_fake_activity(html_content),
            'pressure_popups': self.detect_pressure_popups(html_content),
            'visual_deception': self.detect_visual_deception(html_content),
            'error_misleading': self.detect_error_misleading(html_content),
            'ui_interference': self.detect_ui_interference(html_content),
            'misleading_labels': self.detect_misleading_labels(html_content),
            'hidden_charges': self.detect_hidden_charges(html_content),
            'trick_wording': self.detect_trick_wording(html_content),
            'evergreen_timer': self.detect_evergreen_timer(html_content),
            'reset_countdown': self.detect_reset_countdown(html_content),
            'perpetual_urgency': self.detect_perpetual_urgency(html_content)
        }
        
        if indicator in indicator_detections:
            detection_result = indicator_detections[indicator]
            if detection_result:
                findings.append({
                    'pattern': detection_result['pattern'],
                    'category': category,
                    'confidence': detection_result['confidence'],
                    'type': 'forensic_indicator',
                    'indicator': indicator
                })
        
        return findings
    
    # Forensic indicator detection methods
    def detect_dynamic_stock(self, html_content):
        patterns = [r'stock.*\d+.*left', r'only.*\d+.*remaining', r'low.*stock.*alert']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Dynamic stock levels detected', 'confidence': 90}
        return None
    
    def detect_forced_registration(self, html_content):
        patterns = [r'register.*to.*continue', r'sign.*up.*required', r'create.*account.*to.*view']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Forced registration detected', 'confidence': 88}
        return None
    
    def detect_nagging_popups(self, html_content):
        patterns = [r'popup.*block.*content', r'modal.*persistent', r'overlay.*cannot.*close']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Nagging popups detected', 'confidence': 85}
        return None
    
    def detect_auto_cart_addition(self, html_content):
        patterns = [r'auto.*add.*cart', r'item.*added.*automatically', r'cart.*pre.*filled']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Auto cart addition detected', 'confidence': 92}
        return None
    
    def detect_hidden_items(self, html_content):
        patterns = [r'hidden.*item.*cart', r'concealed.*product', r'invisible.*cart.*item']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden cart items detected', 'confidence': 87}
        return None
    
    def detect_preselected_products(self, html_content):
        patterns = [r'checked.*product', r'selected.*item.*default', r'pre.*selected.*product']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Pre-selected products detected', 'confidence': 90}
        return None
    
    def detect_preselected_donation(self, html_content):
        patterns = [r'donation.*checked', r'tip.*pre.*selected', r'charity.*auto.*add']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Pre-selected donation detected', 'confidence': 91}
        return None
    
    def detect_hidden_insurance(self, html_content):
        patterns = [r'insurance.*hidden', r'protection.*concealed', r'coverage.*not.*shown']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden insurance detected', 'confidence': 89}
        return None
    
    def detect_auto_add_fees(self, html_content):
        patterns = [r'fee.*auto.*add', r'charge.*automatic', r'cost.*included.*hidden']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Auto-added fees detected', 'confidence': 88}
        return None
    
    def detect_hidden_cancellation(self, html_content):
        patterns = [r'cancel.*hidden', r'delete.*concealed', r'unsubscribe.*not.*obvious']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden cancellation detected', 'confidence': 90}
        return None
    
    def detect_support_required(self, html_content):
        patterns = [r'contact.*support.*cancel', r'call.*to.*delete', r'email.*support.*deactivate']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Support required for cancellation', 'confidence': 92}
        return None
    
    def detect_complex_deletion(self, html_content):
        patterns = [r'multi.*step.*delete', r'complex.*deletion', r'delete.*process.*complicated']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Complex deletion process detected', 'confidence': 87}
        return None
    
    def detect_gamification(self, html_content):
        patterns = [r'spin.*wheel', r'game.*purchase', r'play.*win.*discount', r'gamified.*shopping']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Gamification detected', 'confidence': 93}
        return None
    
    def detect_fake_countdown(self, html_content):
        patterns = [r'countdown.*fake', r'timer.*not.*real', r'urgency.*artificial']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Fake countdown detected', 'confidence': 91}
        return None
    
    def detect_fomo_tactics(self, html_content):
        patterns = [r'fear.*missing.*out', r'limited.*time.*offer', r'everyone.*buying', r'popular.*item']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'FOMO tactics detected', 'confidence': 89}
        return None
    
    def detect_hidden_conditions(self, html_content):
        patterns = [r'conditions.*hidden', r'restrictions.*not.*shown', r'terms.*concealed']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden conditions detected', 'confidence': 88}
        return None
    
    def detect_restrictive_pricing(self, html_content):
        patterns = [r'price.*restrictions', r'conditions.*apply.*price', r'limited.*price.*availability']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Restrictive pricing detected', 'confidence': 90}
        return None
    
    def detect_bait_switch(self, html_content):
        patterns = [r'bait.*switch', r'price.*change.*later', r'offer.*not.*available']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Bait and switch detected', 'confidence': 92}
        return None
    
    def detect_subscription_wall(self, html_content):
        patterns = [r'subscription.*wall', r'paid.*required.*continue', r'upgrade.*to.*access']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Subscription wall detected', 'confidence': 91}
        return None
    
    def detect_free_to_paid(self, html_content):
        patterns = [r'free.*to.*paid', r'trial.*then.*charge', r'no.*cost.*then.*price']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Free to paid transition detected', 'confidence': 90}
        return None
    
    def detect_late_subscription(self, html_content):
        patterns = [r'subscription.*late', r'charge.*unexpected', r'auto.*renew.*surprise']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Late subscription charge detected', 'confidence': 89}
        return None
    
    def detect_trial_trap(self, html_content):
        patterns = [r'trial.*trap', r'free.*trial.*catch', r'trial.*difficult.*cancel']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Trial trap detected', 'confidence': 87}
        return None
    
    def detect_hidden_annual(self, html_content):
        patterns = [r'annual.*hidden', r'yearly.*not.*shown', r'annual.*commitment.*concealed']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden annual commitment detected', 'confidence': 91}
        return None
    
    def detect_small_font_terms(self, html_content):
        patterns = [r'font-size.*small', r'terms.*tiny', r'conditions.*small.*print']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Small font terms detected', 'confidence': 85}
        return None
    
    def detect_investment_quiz(self, html_content):
        patterns = [r'quiz.*before.*pricing', r'assessment.*required', r'personalization.*before.*cost']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Investment quiz detected', 'confidence': 88}
        return None
    
    def detect_delayed_pricing(self, html_content):
        patterns = [r'pricing.*delayed', r'cost.*hidden.*until.*end', r'price.*shown.*later']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Delayed pricing detected', 'confidence': 86}
        return None
    
    def detect_commitment_trap(self, html_content):
        patterns = [r'commitment.*trap', r'investment.*before.*price', r'psychological.*commitment']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Commitment trap detected', 'confidence': 89}
        return None
    
    def detect_complex_cancellation(self, html_content):
        patterns = [r'cancellation.*complex', r'deactivate.*difficult', r'unsubscribe.*complicated']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Complex cancellation detected', 'confidence': 88}
        return None
    
    def detect_multi_step_process(self, html_content):
        patterns = [r'step.*\d+.*of.*\d+', r'multi.*step.*process', r'prolonged.*procedure']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Multi-step process detected', 'confidence': 85}
        return None
    
    def detect_hard_to_delete(self, html_content):
        patterns = [r'delete.*hard', r'account.*removal.*difficult', r'permanent.*delete.*complex']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hard to delete detected', 'confidence': 87}
        return None
    
    def detect_live_agent_required(self, html_content):
        patterns = [r'live.*agent.*required', r'chat.*with.*agent', r'call.*support.*needed']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Live agent required detected', 'confidence': 92}
        return None
    
    def detect_phone_cancellation(self, html_content):
        patterns = [r'phone.*cancel', r'call.*to.*unsubscribe', r'telephone.*deactivate']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Phone cancellation required', 'confidence': 91}
        return None
    
    def detect_support_trap(self, html_content):
        patterns = [r'support.*trap', r'contact.*required.*cancel', r'help.*desk.*deactivate']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Support trap detected', 'confidence': 89}
        return None
    
    def detect_hidden_reject(self, html_content):
        patterns = [r'reject.*all.*hidden', r'decline.*concealed', r'opt.*out.*not.*visible']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden reject option detected', 'confidence': 88}
        return None
    
    def detect_cookie_obstruction(self, html_content):
        patterns = [r'cookie.*obstruction', r'privacy.*settings.*complex', r'accept.*only.*option']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Cookie obstruction detected', 'confidence': 87}
        return None
    
    def detect_privacy_complexity(self, html_content):
        patterns = [r'privacy.*complex', r'data.*settings.*confusing', r'consent.*complicated']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Privacy complexity detected', 'confidence': 85}
        return None
    
    def detect_native_ad_disguise(self, html_content):
        patterns = [r'native.*ad', r'sponsored.*content', r'advertisement.*disguised']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Native ad disguise detected', 'confidence': 90}
        return None
    
    def detect_css_matching(self, html_content):
        patterns = [r'css.*same.*as.*article', r'styles.*match.*content', r'visual.*disguise']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'CSS matching detected', 'confidence': 87}
        return None
    
    def detect_ad_disguise(self, html_content):
        patterns = [r'ad.*disguised', r'paid.*content.*news', r'sponsored.*article']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Ad disguise detected', 'confidence': 89}
        return None
    
    def detect_paywall_trap(self, html_content):
        patterns = [r'paywall.*trap', r'article.*limit.*pay', r'subscription.*required.*read']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Paywall trap detected', 'confidence': 91}
        return None
    
    def detect_forced_registration_wall(self, html_content):
        patterns = [r'registration.*wall', r'sign.*up.*required.*continue', r'account.*needed.*access']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Forced registration wall detected', 'confidence': 88}
        return None
    
    def detect_article_limit(self, html_content):
        patterns = [r'article.*limit', r'read.*\d+.*free', r'monthly.*article.*limit']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Article limit detected', 'confidence': 86}
        return None
    
    def detect_price_drip(self, html_content):
        patterns = [r'price.*drip', r'fees.*appear.*later', r'hidden.*charges.*reveal']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Price drip detected', 'confidence': 92}
        return None
    
    def detect_dynamic_pricing(self, html_content):
        patterns = [r'dynamic.*pricing', r'price.*change.*based.*on.*user', r'personalized.*pricing']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Dynamic pricing detected', 'confidence': 89}
        return None
    
    def detect_rapid_price_change(self, html_content):
        patterns = [r'price.*change.*rapid', r'quick.*price.*update', r'fast.*price.*fluctuation']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Rapid price change detected', 'confidence': 87}
        return None
    
    def detect_dynamic_social_proof(self, html_content):
        patterns = [r'someone.*just.*booked', r'people.*looking.*now', r'recent.*activity.*fake']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Dynamic social proof detected', 'confidence': 90}
        return None
    
    def detect_fake_activity(self, html_content):
        patterns = [r'fake.*activity', r'generated.*proof', r'simulated.*engagement']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Fake activity detected', 'confidence': 88}
        return None
    
    def detect_pressure_popups(self, html_content):
        patterns = [r'pressure.*popup', r'urgency.*modal', r'high.*pressure.*overlay']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Pressure popups detected', 'confidence': 86}
        return None
    
    def detect_visual_deception(self, html_content):
        patterns = [r'visual.*deception', r'misleading.*ui', r'deceptive.*design']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Visual deception detected', 'confidence': 87}
        return None
    
    def detect_error_misleading(self, html_content):
        patterns = [r'error.*misleading', r'fake.*error.*message', r'false.*alert']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Misleading error detected', 'confidence': 89}
        return None
    
    def detect_ui_interference(self, html_content):
        patterns = [r'ui.*interference', r'interface.*manipulation', r'user.*experience.*deception']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'UI interference detected', 'confidence': 85}
        return None
    
    def detect_misleading_labels(self, html_content):
        patterns = [r'misleading.*label', r'confusing.*button', r'trick.*wording']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Misleading labels detected', 'confidence': 88}
        return None
    
    def detect_hidden_charges(self, html_content):
        patterns = [r'hidden.*charges', r'concealed.*fees', r'surprise.*cost']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Hidden charges detected', 'confidence': 91}
        return None
    
    def detect_trick_wording(self, html_content):
        patterns = [r'trick.*wording', r'misleading.*text', r'deceptive.*language']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Trick wording detected', 'confidence': 86}
        return None
    
    def detect_evergreen_timer(self, html_content):
        patterns = [r'evergreen.*timer', r'perpetual.*countdown', r'reset.*timer']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Evergreen timer detected', 'confidence': 93}
        return None
    
    def detect_reset_countdown(self, html_content):
        patterns = [r'reset.*countdown', r'timer.*reset', r'countdown.*restart']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Reset countdown detected', 'confidence': 91}
        return None
    
    def detect_perpetual_urgency(self, html_content):
        patterns = [r'perpetual.*urgency', r'evergreen.*scarcity', r'constant.*pressure']
        for pattern in patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return {'pattern': 'Perpetual urgency detected', 'confidence': 89}
        return None
    
    def get_risk_level(self, trust_score):
        """Determine risk level from trust score"""
        if trust_score >= 80:
            return "LOW"
        elif trust_score >= 60:
            return "MEDIUM"
        elif trust_score >= 40:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def print_forensic_analysis_report(self, report):
        """Print forensic analysis report"""
        print(f"\nTrust Score: {report['trust_score']}/100 ({report['risk_level']} RISK)")
        print(f"Analysis Time: {report['analysis_time']}")
        print(f"Findings Detected: {report['findings_count']}")
        print(f"Forensic Findings: {len(report['forensic_findings'])}")
        print(f"Engines Used: {', '.join(report['engines_used'])}")
        print(f"Content Length: {report['content_length']} bytes")
        
        print(f"\n{'='*60}")
        print("FORENSIC PATTERN DETECTION:")
        print(f"{'='*60}")
        
        for i, finding in enumerate(report['forensic_findings'], 1):
            print(f"\n{i}. {finding['category']} (Confidence: {finding.get('confidence', 'N/A')}%)")
            print(f"   Pattern: {finding['pattern']}")
            if 'indicator' in finding:
                print(f"   Indicator: {finding['indicator']}")
            print(f"   Type: {finding['type']}")
        
        print(f"\n{'='*60}")
        print("FORENSIC TECHNICAL PROOF:")
        print(f"{'='*60}")
        
        # Linguistic evidence
        linguistic_findings = [f for f in report['forensic_findings'] if f['type'] == 'text_pattern']
        for finding in linguistic_findings:
            confidence = finding.get('confidence', 85)
            print(f"Linguistic: \"Detected '{finding['pattern']}' - Category: {finding['category']} (Confidence {confidence}%).\"")
        
        # Visual evidence
        visual_findings = [f for f in report['forensic_findings'] if 'visual' in finding.get('indicator', '').lower() or 'deception' in finding['pattern'].lower()]
        for finding in visual_findings:
            print(f"Visual: \"{finding['pattern']}\" - Category: {finding['category']}.")
        
        # Behavioral evidence
        behavioral_findings = [f for f in report['forensic_findings'] if 'behavioral' in finding.get('indicator', '').lower() or 'dynamic' in finding['pattern'].lower()]
        for finding in behavioral_findings:
            print(f"Behavioral: \"{finding['pattern']}\" - Category: {finding['category']}.")
    
    def run_advanced_forensic_suite(self):
        """Run the advanced 20-site forensic test suite"""
        print("AEGIS PRO ADVANCED FORENSIC TESTING SUITE")
        print("=" * 80)
        print("Testing 20 complex websites with sophisticated dark pattern detection...")
        print("=" * 80)
        
        # Define the 20 forensic test sites
        forensic_sites = [
            # Complex E-commerce & Retail
            {'url': 'https://www.shein.com', 'name': 'Shein', 'pattern': 'Fake Scarcity/Nagging', 'challenge': 'Heavy use of "Low Stock" messages and forced registration popups'},
            {'url': 'https://www.sportsdirect.com', 'name': 'SportsDirect', 'pattern': 'Sneak into Basket', 'challenge': 'Historically adds magazines/bags to the cart automatically'},
            {'url': 'https://www.zomato.com', 'name': 'Zomato', 'pattern': 'Sneak into Basket', 'challenge': 'Often pre-checks "Donation" or "Insurance" boxes in the cart'},
            {'url': 'https://www.nykaa.com', 'name': 'Nykaa', 'pattern': 'Roach Motel', 'challenge': 'Easy signup, but account deletion is famously hard to find/requires manual support'},
            {'url': 'https://www.temu.com', 'name': 'Temu', 'pattern': 'Gamified Urgency', 'challenge': 'Uses "Spin the Wheel" and fake countdowns to create FOMO'},
            {'url': 'https://www.groupon.com', 'name': 'Groupon', 'pattern': 'Bait & Switch', 'challenge': 'Highlighting a low price that is only available under restrictive conditions'},
            
            # Digital Services & SaaS
            {'url': 'https://www.canva.com', 'name': 'Canva', 'pattern': 'Forced Continuity', 'challenge': '"Free" elements that lead to a subscription wall late in the design process'},
            {'url': 'https://www.lumosme.com', 'name': 'Lumosme', 'pattern': 'Hidden Subscription', 'challenge': 'Often hides the transition from a "trial" to a high-cost annual plan'},
            {'url': 'https://www.noom.com', 'name': 'Noom', 'pattern': 'Hard to Cancel', 'challenge': 'Uses long onboarding quizzes to build "investment" before showing prices'},
            {'url': 'https://www.match.com', 'name': 'Match', 'pattern': 'Roach Motel', 'challenge': 'Extremely complex multi-step process to deactivate or delete'},
            {'url': 'https://www.scribd.com', 'name': 'Scribd', 'pattern': 'Hidden Fee/Continuity', 'challenge': 'Hides auto-renewal terms in small font during "Free Trial" signup'},
            
            # Media & News
            {'url': 'https://www.wired.com', 'name': 'Wired', 'pattern': 'Hard to Cancel', 'challenge': 'Subscription cancellation often requires a live agent chat/call'},
            {'url': 'https://www.independent.co.uk', 'name': 'Independent', 'pattern': 'Obstruction', 'challenge': 'Cookie banners designed with "Reject All" hidden behind 3+ layers'},
            {'url': 'https://www.dailymail.co.uk', 'name': 'DailyMail', 'pattern': 'Disguised Ads', 'challenge': '"Sponsored Content" that uses the exact same CSS as real news articles'},
            {'url': 'https://www.hbr.org', 'name': 'HBR', 'pattern': 'Paywall Wall', 'challenge': '"Read 2 more articles for free" (Forced Action/Registration)'},
            
            # Travel & Booking
            {'url': 'https://www.skyscanner.net', 'name': 'Skyscanner', 'pattern': 'Price Drip', 'challenge': 'Prices change rapidly between the search result and the provider\'s site'},
            {'url': 'https://www.travelocity.com', 'name': 'Travelocity', 'pattern': 'Social Pressure', 'challenge': '"Someone in Mumbai just booked this" dynamic popups'},
            {'url': 'https://www.frontier.com', 'name': 'Frontier', 'pattern': 'Visual Interference', 'challenge': 'Making "No Seat Selection" (Free) look like an error message'},
            {'url': 'https://www.vueling.com', 'name': 'Vueling', 'pattern': 'Trick Wording', 'challenge': 'Using "Accept & Continue" to mean "Accept Extra Charges"'},
            {'url': 'https://www.hostelworld.com', 'name': 'Hostelworld', 'pattern': 'Limited Time Offer', 'challenge': 'Evergreen timers that reset every time you re-enter the site'}
        ]
        
        results = []
        
        for i, site in enumerate(forensic_sites, 1):
            print(f"\n\n{'#'*80}")
            print(f"FORENSIC TESTING SITE {i}/20: {site['name']}")
            print(f"{'#'*80}")
            
            try:
                result = self.analyze_forensic_patterns(site)
                
                if result:
                    results.append(result)
                
                # Add delay between requests
                time.sleep(3)
                
            except Exception as e:
                print(f"Error testing {site['name']}: {str(e)}")
                continue
        
        # Generate comprehensive summary
        self.generate_forensic_summary(results)
        
        return results
    
    def generate_forensic_summary(self, results):
        """Generate comprehensive summary of forensic tests"""
        print(f"\n\n{'='*80}")
        print("AEGIS PRO ADVANCED FORENSIC TESTING SUMMARY")
        print(f"{'='*80}")
        
        if not results:
            print("No results to report.")
            return
        
        # Calculate statistics
        total_tests = len(results)
        avg_trust_score = sum(r['trust_score'] for r in results) / total_tests
        critical_sites = [r for r in results if r['trust_score'] < 30]
        high_risk_sites = [r for r in results if 30 <= r['trust_score'] < 50]
        medium_risk_sites = [r for r in results if 50 <= r['trust_score'] < 70]
        low_risk_sites = [r for r in results if r['trust_score'] >= 70]
        
        print(f"Total Sites Tested: {total_tests}")
        print(f"Average Trust Score: {avg_trust_score:.1f}/100")
        print(f"Critical Risk Sites (<30): {len(critical_sites)}")
        print(f"High Risk Sites (30-50): {len(high_risk_sites)}")
        print(f"Medium Risk Sites (50-70): {len(medium_risk_sites)}")
        print(f"Low Risk Sites (>=70): {len(low_risk_sites)}")
        
        print(f"\n{'='*80}")
        print("FORENSIC SITE RANKINGS (WORST TO BEST)")
        print(f"{'='*80}")
        
        # Sort by trust score (worst first)
        sorted_results = sorted(results, key=lambda x: x['trust_score'])
        
        for i, result in enumerate(sorted_results, 1):
            risk_indicator = "CRITICAL" if result['trust_score'] < 30 else "HIGH" if result['trust_score'] < 50 else "MEDIUM" if result['trust_score'] < 70 else "LOW"
            print(f"{i:2d}. {result['name']:15s} - Score: {int(result['trust_score']):3d}/100 ({risk_indicator:9s}) - {result['pattern']}")
        
        # Pattern detection summary
        print(f"\n{'='*80}")
        print("FORENSIC PATTERN DETECTION SUMMARY")
        print(f"{'='*80}")
        
        pattern_counts = {}
        for result in results:
            pattern = result['pattern']
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        for pattern, count in pattern_counts.items():
            print(f"{pattern:25s}: {count} site(s)")
        
        # Forensic findings summary
        print(f"\n{'='*80}")
        print("ADVANCED FORENSIC FINDINGS SUMMARY")
        print(f"{'='*80}")
        
        forensic_pattern_counts = {}
        for result in results:
            for finding in result['forensic_findings']:
                category = finding['category']
                forensic_pattern_counts[category] = forensic_pattern_counts.get(category, 0) + 1
        
        for category, count in sorted(forensic_pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:25s}: {count} detection(s)")

def main():
    """Main function to run advanced forensic tests"""
    tester = AdvancedForensicTester()
    results = tester.run_advanced_forensic_suite()
    
    print(f"\n\n{'='*80}")
    print("ADVANCED FORENSIC TESTING COMPLETE")
    print(f"{'='*80}")
    print(f"Analyzed {len(results)} complex websites")
    print("Results saved to analysis output above")
    print("\nAegis Pro Advanced Forensic Testing - COMPLETE")

if __name__ == "__main__":
    main()
