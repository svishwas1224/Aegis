"""
Aegis Dark-Pattern Detector Tri-Engine Analyzer
Coordinates NLP + Computer Vision + Network Forensics engines
"""

from typing import Dict, List, Any
from .linguistic_engine import LinguisticEngine
from .visual_engine import VisualEngine
from .behavioral_engine import BehavioralEngine

class TriEngineAnalyzer:
    def __init__(self):
        self.linguistic_engine = LinguisticEngine()
        self.visual_engine = VisualEngine()
        self.behavioral_engine = BehavioralEngine()
    
    def analyze_comprehensive(self, url: str, html_content: str = None, 
                            screenshot_b64: str = None, har_data: Dict = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis using all three engines
        """
        all_findings = []
        engine_scores = {}
        engines_used = []
        
        # Linguistic Analysis
        if html_content:
            linguistic_result = self.linguistic_engine.analyze_text(html_content)
            all_findings.extend(linguistic_result['findings'])
            engine_scores['NLP'] = linguistic_result['trust_score']
            engines_used.append('NLP')
        
        # Visual Analysis
        visual_findings = []
        if screenshot_b64:
            visual_result = self.visual_engine.analyze_screenshot(screenshot_b64)
            visual_findings.extend(visual_result['findings'])
            engine_scores['VISUAL'] = visual_result['trust_score']
            engines_used.append('VISUAL')
        
        if html_content:
            visual_html_result = self.visual_engine.analyze_html_structure(html_content)
            visual_findings.extend(visual_html_result['findings'])
            if 'VISUAL' not in engine_scores:
                engine_scores['VISUAL'] = visual_html_result['trust_score']
                engines_used.append('VISUAL')
        
        # Combine visual findings
        all_findings.extend(visual_findings)
        
        # Behavioral Analysis
        if har_data:
            behavioral_result = self.behavioral_engine.analyze_har(har_data)
            all_findings.extend(behavioral_result['findings'])
            engine_scores['BEHAVIORAL'] = behavioral_result['trust_score']
            engines_used.append('BEHAVIORAL')
        
        # Calculate composite trust score with stricter penalties
        if engine_scores:
            # Weight the engines (can be adjusted based on importance)
            weights = {
                'NLP': 0.4,
                'VISUAL': 0.35,
                'BEHAVIORAL': 0.25
            }
            
            composite_score = 0
            total_weight = 0
            
            for engine, score in engine_scores.items():
                weight = weights.get(engine, 0.33)
                composite_score += score * weight
                total_weight += weight
            
            final_score = composite_score / total_weight if total_weight > 0 else 100
            
            # Apply additional penalties for multiple findings
            finding_penalty = min(len(all_findings) * 8, 40)  # 8 points per finding, max 40
            final_score = max(0, final_score - finding_penalty)
        else:
            final_score = 100
        
        # Determine risk level
        if final_score >= 75:
            risk_level = 'SAFE'
            status = 'SAFE'
        elif final_score >= 45:
            risk_level = 'CAUTION'
            status = 'SUSPICIOUS'
        else:
            risk_level = 'DANGER'
            status = 'UNSAFE'
        
        # Generate summary
        summary = self._generate_summary(all_findings, final_score, risk_level)
        
        return {
            'url': url,
            'trust_score': round(final_score, 1),
            'risk_level': risk_level,
            'status': status,
            'findings': all_findings,
            'patterns_found': len(all_findings),
            'engines_used': engines_used,
            'engine_scores': engine_scores,
            'summary': summary,
            'analysis_ms': None  # Would be populated with actual timing
        }
    
    def _generate_summary(self, findings: List[Dict], score: float, risk_level: str) -> str:
        """Generate human-readable summary of findings"""
        if not findings:
            return "No dark patterns detected. The page appears to follow ethical design practices."
        
        # Count findings by type
        finding_types = {}
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for finding in findings:
            finding_type = finding.get('type', 'unknown')
            finding_types[finding_type] = finding_types.get(finding_type, 0) + 1
            severity = finding.get('severity', 'MEDIUM')
            severity_counts[severity] += 1
        
        # Build summary
        summary_parts = []
        
        if severity_counts['HIGH'] > 0:
            summary_parts.append(f"{severity_counts['HIGH']} high-risk issues")
        if severity_counts['MEDIUM'] > 0:
            summary_parts.append(f"{severity_counts['MEDIUM']} medium-risk issues")
        if severity_counts['LOW'] > 0:
            summary_parts.append(f"{severity_counts['LOW']} low-risk issues")
        
        # Most common pattern types
        if finding_types:
            most_common = max(finding_types.items(), key=lambda x: x[1])
            summary_parts.append(f"most common: {most_common[0]}")
        
        summary = f"Detected {', '.join(summary_parts)}. "
        
        # Add risk-specific advice
        if risk_level == 'DANGER':
            summary += "This page shows strong signs of manipulative design. Exercise extreme caution."
        elif risk_level == 'CAUTION':
            summary += "Some concerning patterns detected. Review carefully before proceeding."
        else:
            summary += "Minor issues found but overall appears trustworthy."
        
        return summary
    
    def get_remediation_suggestions(self, findings):
        """Get prioritized remediation suggestions"""
        suggestions = []
        
        # Group by severity
        high_priority = [f for f in findings if f.get('severity') == 'HIGH']
        medium_priority = [f for f in findings if f.get('severity') == 'MEDIUM']
        low_priority = [f for f in findings if f.get('severity') == 'LOW']
        
        # Generate suggestions
        if high_priority:
            suggestions.append("URGENT: Address high-risk issues immediately:")
            for finding in high_priority[:3]:  # Top 3 high priority
                remediation = finding.get('remediation', 'Review and fix this issue')
                suggestions.append(f"  • {remediation}")
        
        if medium_priority:
            suggestions.append("Recommended improvements:")
            for finding in medium_priority[:3]:  # Top 3 medium priority
                remediation = finding.get('remediation', 'Consider improving this area')
                suggestions.append(f"  • {remediation}")
        
        if low_priority:
            suggestions.append("Minor enhancements:")
            for finding in low_priority[:2]:  # Top 2 low priority
                remediation = finding.get('remediation', 'Optional improvement')
                suggestions.append(f"  • {remediation}")
        
        return suggestions
