"""
Aegis Pro Linguistic Engine
Analyzes text content for dark patterns using NLP techniques
"""

import re
import spacy
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
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
            
        # Dark pattern patterns
        self.patterns = {
            'confirm_shaming': [
                r'no thanks,? i (don\'t|do not|hate) want to.*',
                r'no thanks,? i hate.*',
                r'cancel.*and lose.*benefits?',
                r'stay.*and get.*discount',
                r'are you sure you want to miss out',
                r'don\'t leave.*empty handed'
            ],
            'urgency': [
                r'only \d+ left',
                r'limited time',
                r'ends in.*hours?',
                r'expires in.*minutes?',
                r'expires in.*hours?',
                r'flash sale',
                r'almost gone',
                r'last chance',
                r'expires soon'
            ],
            'scarcity': [
                r'high demand',
                r'\d+ people are viewing',
                r'only \d+ items left',
                r'just sold',
                r'back in stock',
                r'limited stock',
                r'flying off the shelves',
                r'almost gone'
            ],
            'social_proof': [
                r'\d+ people bought',
                r'\d+ people are viewing',
                r'join \d+ customers',
                r'most popular',
                r'trending now',
                r'bestseller',
                r'join \d+ satisfied customers'
            ],
            'misdirection': [
                r'continue.*without.*saving',
                r'skip.*and.*pay.*more',
                r'not now.*maybe later',
                r'remind me later',
                r'click next.*purchase',
                r'next.*complete.*purchase'
            ],
            'forced_action': [
                r'accept.*to continue',
                r'agree.*to proceed',
                r'sign up.*required'
            ],
            'security_pressure': [
                r'your (pc|computer) is infected',
                r'virus detected',
                r'download.*antivirus',
                r'security alert',
                r'malware detected'
            ],
            'friend_spam': [
                r'invite.*friends.*unlock',
                r'share.*contacts.*now',
                r'invite \d+ friends',
                r'refer.*friends.*premium'
            ],
            'testimonial_pressure': [
                r'verified purchase',
                r'\d+ stars',
                r'changed my life',
                r'says.*5 stars',
                r'customer review'
            ],
            'hidden_costs': [
                r'processing fee',
                r'shipping.*handling',
                r'\$\d+\.\d+.*fee',
                r'applies to all orders'
            ],
            'bait_and_switch': [
                r'free.*\$\d+\.\d+',
                r'just pay.*shipping',
                r'free.*but.*cost',
                r'free.*handling'
            ],
            'ambiguous_labeling': [
                r'next.*purchase',
                r'continue.*pay',
                r'skip.*later.*cost'
            ]
        }
        
        self.severity_keywords = {
            'HIGH': ['immediately', 'urgent', 'critical', 'final', 'last chance'],
            'MEDIUM': ['limited', 'only', 'special', 'exclusive'],
            'LOW': ['popular', 'recommended', 'suggested']
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text for dark patterns"""
        if not text:
            return {'findings': [], 'trust_score': 100}
            
        findings = []
        total_penalty = 0
        
        # Pattern matching
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    severity = self._determine_severity(match.group())
                    remediation = self._get_remediation(pattern_type, match.group())
                    explanation = self._get_explanation(pattern_type)
                    
                    finding = DarkPatternMatch(
                        type=pattern_type,
                        severity=severity,
                        source_text=match.group(),
                        confidence=0.8,
                        remediation=remediation,
                        explanation=explanation
                    )
                    
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
            'forced_action': 'Continue'
        }
        return remediations.get(pattern_type, 'Neutral alternative')
    
    def _get_explanation(self, pattern_type: str) -> str:
        """Get explanation of the dark pattern"""
        explanations = {
            'confirm_shaming': 'Uses guilt to discourage users from declining',
            'urgency': 'Creates artificial time pressure to force quick decisions',
            'scarcity': 'Implies limited availability to increase demand',
            'social_proof': 'Uses social influence to validate purchasing decisions',
            'misdirection': 'Directs attention away from important options',
            'forced_action': 'Requires users to take unwanted actions'
        }
        return explanations.get(pattern_type, 'Dark pattern detected')
    
    def _get_penalty(self, severity: str) -> int:
        """Get penalty points based on severity"""
        penalties = {'HIGH': 25, 'MEDIUM': 15, 'LOW': 8}
        return penalties.get(severity, 10)
    
    def _analyze_with_spacy(self, doc) -> List[Dict]:
        """Additional analysis using spaCy"""
        findings = []
        
        # Look for manipulative language patterns
        manipulative_words = ['guarantee', 'promise', 'never', 'always', 'instantly', 'magically']
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
