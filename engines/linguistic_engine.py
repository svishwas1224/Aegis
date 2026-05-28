"""
Aegis Pro Linguistic Engine
Analyzes text content for dark patterns using NLP techniques
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class DarkPatternMatch:
    type: str
    severity: str
    source_text: str
    confidence: float
    remediation: str
    explanation: str

class LinguisticEngine:
    def __init__(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Load trained ML model
        self.ml_model = None
        try:
            import pickle
            import os
            model_path = os.path.join(os.path.dirname(__file__), "..", "data", "dark_pattern_model.pkl")
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.ml_model = pickle.load(f)
                print("✅ Trained ML model loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load ML model: {e}")
            
        # Comprehensive Dark Pattern Patterns (from Dark Patterns.org, ACM, and real-world sites)
        self.patterns = {
            'confirm_shaming': [
                r'no thanks,? i (don\'t|do not|hate) want to.*',
                r'no thanks,? i hate.*',
                r'cancel.*and lose.*benefits?',
                r'stay.*and get.*discount',
                r'are you sure you want to miss out',
                r'don\'t leave.*empty handed',
                r'refuse.*\$\d+ savings',
                r'decline.*missing out',
                r'are you sure.*you want.*give up',
                r'keep.*your.*discount.*decline.*lose it'
            ],
            'urgency': [
                r'only \d+ (item|items|left)',
                r'limited time',
                r'ends in.*(hour|hours|minute|minutes|second|seconds)?',
                r'expires in.*(hour|hours|minute|minutes|second|seconds)?',
                r'flash sale',
                r'almost gone',
                r'last chance',
                r'expires soon',
                r'final hours',
                r'ending soon',
                r'once.*gone.*gone',
                r'hurry.*ends',
                r'offer.*ends.*today',
                r'today only',
                r'deal of the day'
            ],
            'scarcity': [
                r'high demand',
                r'\d+ people are viewing',
                r'only \d+ (item|items) left',
                r'just sold',
                r'back in stock',
                r'limited stock',
                r'flying off the shelves',
                r'almost gone',
                r'limited edition',
                r'exclusive release',
                r'only available today',
                r'in high demand',
                r'popular right now',
                r'selling fast',
                r'limited quantity',
                r'backorder.*soon',
                r'out of stock.*soon'
            ],
            'social_proof': [
                r'\d+ people bought',
                r'\d+ people are viewing',
                r'join \d+ customers',
                r'most popular',
                r'trending now',
                r'bestseller',
                r'join \d+ satisfied customers',
                r'\d+ people bought this',
                r'others are buying',
                r'\d+ in your area',
                r'\d+ people viewing right now',
                r'popular item',
                r'best seller'
            ],
            'misdirection': [
                r'continue.*without.*saving',
                r'skip.*and.*pay.*more',
                r'not now.*maybe later',
                r'remind me later',
                r'click next.*purchase',
                r'next.*complete.*purchase',
                r'keep.*purchase',
                r'don\'t.*keep.*discount',
                r'primary.*secondary.*button'
            ],
            'forced_action': [
                r'accept.*to continue',
                r'agree.*to proceed',
                r'sign up.*required',
                r'must.*sign up.*proceed',
                r'you must.*to.*continue',
                r'accept all.*cookies',
                r'subscribe.*to unlock',
                r'create account.*to continue',
                r'login.*to access'
            ],
            'security_pressure': [
                r'your (pc|computer|device|account) is infected',
                r'virus detected',
                r'download.*antivirus',
                r'security alert',
                r'malware detected',
                r'your.*account.*will be deleted',
                r'urgent.*security.*notice',
                r'warning.*your.*data'
            ],
            'friend_spam': [
                r'invite.*friends.*unlock',
                r'share.*contacts.*now',
                r'invite \d+ friends',
                r'refer.*friends.*premium',
                r'share.*to.*unlock',
                r'refer.*a friend',
                r'get.*reward.*for referring'
            ],
            'testimonial_pressure': [
                r'verified purchase',
                r'\d+ stars',
                r'changed my life',
                r'says.*5 stars',
                r'customer review',
                r'don\'t just take my word for it',
                r'as seen on tv',
                r'celebrity endorsed'
            ],
            'hidden_costs': [
                r'processing fee',
                r'shipping.*handling',
                r'\$\d+\.\d+.*fee',
                r'applies to all orders',
                r'additional fees',
                r'extra charges',
                r'handling fee',
                r'administrative fee',
                r'service charge',
                r'tax.*not included',
                r'shipping.*calculated at checkout',
                r'fees.*not shown'
            ],
            'bait_and_switch': [
                r'free.*\$\d+\.\d+',
                r'just pay.*shipping',
                r'free.*but.*cost',
                r'free.*handling',
                r'try.*only.*shipping',
                r'free.*after.*first month',
                r'free.*trial.*but then.*charge',
                r'similar item',
                r'you might also like'
            ],
            'ambiguous_labeling': [
                r'next.*purchase',
                r'continue.*pay',
                r'skip.*later.*cost',
                r'maybe.*next time',
                r'later.*costs',
                r'fine print',
                r'terms.*apply',
                r'restrictions.*apply'
            ],
            'subscription_traps': [
                r'auto.*renew',
                r'automatic.*renewal',
                r'renew.*automatically',
                r'unsubscribe.*difficult',
                r'cancel.*subscription.*call',
                r'you will.*charged.*automatically',
                r'continue.*subscription.*unless.*cancel',
                r'auto renew',
                r'subscription continues',
                r'membership renews',
                r'cancel.*in person',
                r'cancel.*by mail'
            ],
            'false_free_trials': [
                r'free trial.*credit card',
                r'free.*but.*billed',
                r'credit card.*required.*free',
                r'trial.*will.*charge you',
                r'no credit card needed.*just kidding',
                r'today only free'
            ],
            'countdown_manipulation': [
                r'countdown',
                r'timer.*ends',
                r'hurry.*ends in',
                r'offer.*ends in',
                r'sale.*ends in'
            ],
            'price_comparison_manipulation': [
                r'compare at.*\$\d+',
                r'was.*\$\d+.*now.*\$\d+',
                r'list price.*\$\d+',
                r'original price.*\$\d+',
                r'save.*\$\d+',
                r'savings.*\$\d+',
                r'you save.*\$\d+',
                r'marked down.*from'
            ],
            'cookie_walls': [
                r'accept all cookies',
                r'accept cookies to continue',
                r'you must accept cookies',
                r'cookies.*required for access'
            ],
            'fake_reviews': [
                r'5 stars',
                r'best review',
                r'perfect',
                r'\'excellent\'',
                r'verified.*purchase'
            ],
            'privacy_zuckering': [
                r'we share your data with',
                r'we collect.*personal information',
                r'we use your data to',
                r'we may sell your information'
            ],
            'sneak_into_basket': [
                r'added to cart automatically',
                r'we added this to your cart',
                r'added this to your cart',
                r'frequently bought together',
                r'customers also bought',
                r'added to your basket',
                r'automatically added',
                r'we added',
                r'added to cart'
            ],
            'disguised_ads': [
                r'sponsored content',
                r'promoted',
                r'advertisement',
                r'paid partnership',
                r'you might like'
            ],
            'hard_to_cancel': [
                r'cancel.*by phone only',
                r'call to cancel',
                r'cancel.*in writing',
                r'cancel.*during business hours only',
                r'submit.*cancellation request'
            ],
            'pre_selected_options': [
                r'pre selected',
                r'we\'ve chosen for you',
                r'recommended option',
                r'popular choice',
                r'checked by default',
                r'selected automatically'
            ],
            'trick_question': [
                r'check this box to not receive',
                r'uncheck this box if you don\'t want',
                r'opt out by checking',
                r'deselect to opt out'
            ]
        }
        
        self.severity_keywords = {
            'HIGH': ['immediately', 'urgent', 'critical', 'final', 'last chance', 'infected', 'will be deleted', 'warning', 'auto renew', 'must accept', 'credit card required', 'automatically', 'added to your cart', 'must accept cookies'],
            'MEDIUM': ['limited', 'only', 'special', 'exclusive', 'bestseller', 'popular', 'trending', 'just sold', 'frequently bought together', 'customers also bought'],
            'LOW': ['recommended', 'suggested', 'might like', 'you might also like']
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text for dark patterns"""
        if not text:
            return {'findings': [], 'trust_score': 100}
            
        findings = []
        seen_patterns = set()
        total_penalty = 0
        
        # Pattern matching
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Deduplicate findings
                    finding_key = (pattern_type,)
                    if finding_key in seen_patterns:
                        continue
                    seen_patterns.add(finding_key)
                    
                    severity = self._determine_severity(match.group())
                    remediation = self._get_remediation(pattern_type, match.group())
                    explanation = self._get_explanation(pattern_type)
                    
                    findings.append({
                        'engine': 'NLP',
                        'type': pattern_type,
                        'severity': severity,
                        'source_text': match.group(),
                        'evidence': {'pattern_matched': pattern, 'position': match.span()},
                        'remediation': remediation,
                        'explanation': explanation
                    })
                    
                    total_penalty += self._get_penalty(severity)
        
        # ML model prediction
        if self.ml_model:
            try:
                prediction = self.ml_model.predict([text])[0]
                prediction_proba = self.ml_model.predict_proba([text])[0] if hasattr(self.ml_model, 'predict_proba') else None
                
                if prediction == 1:  # ML model detects dark pattern
                    confidence = prediction_proba[1] if prediction_proba is not None else 0.7
                    finding_key = ('ml_dark_pattern',)
                    if finding_key not in seen_patterns:
                        seen_patterns.add(finding_key)
                        severity = 'MEDIUM' if confidence < 0.8 else 'HIGH'
                        findings.append({
                            'engine': 'NLP',
                            'type': 'ml_detected_dark_pattern',
                            'severity': severity,
                            'source_text': text[:100],
                            'evidence': {'ml_confidence': confidence},
                            'remediation': 'Review content carefully for manipulative patterns',
                            'explanation': f'ML model detected potential dark pattern with {confidence*100:.1f}% confidence'
                        })
                        total_penalty += self._get_penalty(severity)
            except Exception as e:
                print(f"Warning: ML model prediction failed: {e}")
        
        # spaCy analysis for additional context
        if self.nlp:
            doc = self.nlp(text)
            findings.extend(self._analyze_with_spacy(doc))
        
        # Calculate trust score
        base_score = 100
        final_score = max(0, base_score - total_penalty)
        
        return {
            'findings': findings,
            'trust_score': final_score,
            'patterns_detected': len(findings),
            'analysis_type': 'linguistic'
        }
    
    def _determine_severity(self, text: str) -> str:
        """Determine severity based on keywords"""
        text_lower = text.lower()
        for severity, keywords in self.severity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return severity
        return 'MEDIUM'
    
    def _get_remediation(self, pattern_type: str, original_text: str) -> str:
        """Get neutral replacement for dark pattern"""
        remediations = {
            'confirm_shaming': 'No thanks, I prefer not to receive updates',
            'urgency': 'Limited time offer available',
            'scarcity': 'Popular item with limited availability',
            'social_proof': 'Customer favorite',
            'misdirection': 'Continue to next step',
            'forced_action': 'Continue',
            'security_pressure': 'Remain calm and verify independently',
            'friend_spam': 'Share if you genuinely enjoy the product',
            'testimonial_pressure': 'Read reviews if available',
            'hidden_costs': 'Check full price before purchasing',
            'bait_and_switch': 'Verify actual cost and details',
            'ambiguous_labeling': 'Read terms carefully',
            'subscription_traps': 'Check auto-renewal and cancellation policies',
            'false_free_trials': 'Read fine print about trial period and charges',
            'countdown_manipulation': 'Note the actual deadline',
            'price_comparison_manipulation': 'Research actual market prices',
            'cookie_walls': 'Check cookie settings and preferences',
            'fake_reviews': 'Look for detailed and mixed reviews',
            'privacy_zuckering': 'Read privacy policy carefully',
            'sneak_into_basket': 'Review your cart before checkout',
            'disguised_ads': 'Look for sponsored content disclosures',
            'hard_to_cancel': 'Check cancellation policy before subscribing',
            'pre_selected_options': 'Review all options before confirming',
            'trick_question': 'Read options carefully'
        }
        return remediations.get(pattern_type, 'Neutral alternative')
    
    def _get_explanation(self, pattern_type: str) -> str:
        """Get explanation of the dark pattern"""
        explanations = {
            'confirm_shaming': 'Uses guilt or negative language to discourage users from declining an offer',
            'urgency': 'Creates artificial time pressure to force quick, uninformed decisions',
            'scarcity': 'Implies limited availability (often fake) to create FOMO and increase demand',
            'social_proof': 'Uses social influence or inflated statistics to validate purchasing decisions',
            'misdirection': 'Directs attention away from important or costly options',
            'forced_action': 'Requires users to take unwanted actions to proceed',
            'security_pressure': 'Creates fear or urgency around security to manipulate behavior',
            'friend_spam': 'Encourages users to spam friends for rewards',
            'testimonial_pressure': 'Uses exaggerated testimonials to build trust',
            'hidden_costs': 'Hides additional fees or charges until the final checkout step',
            'bait_and_switch': 'Offers something desirable to attract users, then substitutes with something else',
            'ambiguous_labeling': 'Uses confusing or unclear labels to mislead users',
            'subscription_traps': 'Makes it easy to sign up but hard to unsubscribe, with automatic renewals',
            'false_free_trials': 'Offers "free" trials that require credit cards and auto-renew at full price',
            'countdown_manipulation': 'Uses fake or misleading countdown timers to create urgency',
            'price_comparison_manipulation': 'Inflates original prices to make discounts seem better',
            'cookie_walls': 'Blocks content access unless all cookies are accepted',
            'fake_reviews': 'Uses fake or purchased reviews to build credibility',
            'privacy_zuckering': 'Hides or buries important privacy information',
            'sneak_into_basket': 'Automatically adds items to cart without user consent',
            'disguised_ads': 'Makes ads look like organic content',
            'hard_to_cancel': 'Makes cancellation unnecessarily difficult',
            'pre_selected_options': 'Pre-selects options that benefit the company, not the user',
            'trick_question': 'Uses confusing wording to trick users into selecting unwanted options'
        }
        return explanations.get(pattern_type, 'Dark pattern detected')
    
    def _get_penalty(self, severity: str) -> int:
        """Get penalty points based on severity"""
        penalties = {'HIGH': 30, 'MEDIUM': 20, 'LOW': 10}
        return penalties.get(severity, 15)
    
    def _analyze_with_spacy(self, doc) -> List[Dict]:
        """Additional analysis using spaCy"""
        findings = []
        
        # Look for manipulative language patterns
        manipulative_words = ['guarantee', 'promise', 'never', 'always', 'instantly', 'magically', '100%', 'perfect', 'miracle']
        for token in doc:
            if token.text.lower() in manipulative_words:
                findings.append({
                    'engine': 'NLP',
                    'type': 'manipulative_language',
                    'severity': 'MEDIUM',
                    'source_text': token.text,
                    'evidence': {'pos': token.pos_, 'lemma': token.lemma_},
                    'remediation': 'Consider using more measured language',
                    'explanation': 'Uses absolute terms that may mislead users'
                })
        
        return findings
