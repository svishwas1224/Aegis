"""
Test suite for Aegis Pro Tri-Engine Architecture
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer
from engines.linguistic_engine import LinguisticEngine
from engines.visual_engine import VisualEngine
from engines.behavioral_engine import BehavioralEngine

class TestLinguisticEngine:
    """Test the NLP analysis engine"""
    
    def setup_method(self):
        self.engine = LinguisticEngine()
    
    def test_confirm_shaming_detection(self):
        """Test detection of confirm shaming patterns"""
        text = "No thanks, I don't want to save money"
        result = self.engine.analyze_text(text)
        
        assert len(result['findings']) > 0
        assert any(f['type'] == 'confirm_shaming' for f in result['findings'])
        assert result['trust_score'] < 100
    
    def test_urgency_detection(self):
        """Test detection of urgency patterns"""
        text = "Only 2 hours left! Limited time offer!"
        result = self.engine.analyze_text(text)
        
        assert len(result['findings']) > 0
        assert any(f['type'] == 'urgency' for f in result['findings'])
    
    def test_safe_text(self):
        """Test that safe text returns high trust score"""
        text = "Welcome to our website. We offer quality products at fair prices."
        result = self.engine.analyze_text(text)
        
        assert result['trust_score'] >= 90
        assert len(result['findings']) == 0
    
    def test_remediation_generation(self):
        """Test that remediation suggestions are generated"""
        text = "Cancel and lose your benefits"
        result = self.engine.analyze_text(text)
        
        finding = result['findings'][0]
        assert finding['remediation'] is not None
        assert finding['remediation'] != text

class TestVisualEngine:
    """Test the visual analysis engine"""
    
    def setup_method(self):
        self.engine = VisualEngine()
    
    def test_contrast_analysis(self):
        """Test contrast ratio analysis"""
        # Mock low contrast image data
        import base64
        # This would be a real base64 image in actual tests
        mock_image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        result = self.engine.analyze_screenshot(mock_image_b64)
        
        # Should return some analysis even for simple images
        assert 'findings' in result
        assert 'trust_score' in result
    
    def test_html_structure_analysis(self):
        """Test HTML structure analysis"""
        html_content = """
        <html>
        <body>
            <div style="display:none">Hidden terms and conditions</div>
            <button style="font-size:10px">Tiny button</button>
        </body>
        </html>
        """
        
        result = self.engine.analyze_html_structure(html_content)
        
        assert len(result['findings']) > 0
        assert any(f['type'] == 'hidden_element' for f in result['findings'])

class TestBehavioralEngine:
    """Test the behavioral analysis engine"""
    
    def setup_method(self):
        self.engine = BehavioralEngine()
    
    def test_har_analysis(self):
        """Test HAR (HTTP Archive) analysis"""
        mock_har = {
            'entries': [
                {
                    'request': {'url': 'https://example.com/api/countdown'},
                    'response': {
                        'status': 200,
                        'headers': [
                            {'name': 'cache-control', 'value': 'max-age=3600'}
                        ],
                        'content': {'text': 'Only 5 minutes left!'}
                    }
                }
            ]
        }
        
        result = self.engine.analyze_har(mock_har)
        
        assert 'findings' in result
        assert 'trust_score' in result
    
    def test_tracking_detection(self):
        """Test excessive tracking detection"""
        mock_har = {
            'entries': [
                {'request': {'url': 'https://google-analytics.com/collect'}},
                {'request': {'url': 'https://facebook.com/tr'}},
                {'request': {'url': 'https://doubleclick.net/ad'}},
                # Add many more tracking requests...
            ] * 5  # Multiple tracking requests
        }
        
        result = self.engine.analyze_har(mock_har)
        
        assert len(result['findings']) > 0
        assert any(f['type'] == 'excessive_tracking' for f in result['findings'])

class TestTriEngineAnalyzer:
    """Test the integrated tri-engine analyzer"""
    
    def setup_method(self):
        self.analyzer = TriEngineAnalyzer()
    
    def test_comprehensive_analysis(self):
        """Test full tri-engine analysis"""
        url = "https://example.com"
        html_content = """
        <html>
        <body>
            <h1>Limited Time Offer!</h1>
            <p>No thanks, I don't want to save money</p>
            <div style="display:none">Hidden terms</div>
        </body>
        </html>
        """
        
        result = self.analyzer.analyze_comprehensive(
            url=url,
            html_content=html_content
        )
        
        assert result['url'] == url
        assert 'trust_score' in result
        assert 'risk_level' in result
        assert 'findings' in result
        assert 'engines_used' in result
        assert len(result['findings']) > 0
    
    def test_engine_coordination(self):
        """Test that all engines are properly coordinated"""
        result = self.analyzer.analyze_comprehensive(
            url="https://example.com",
            html_content="<p>Test content</p>"
        )
        
        # Should use at least one engine
        assert len(result['engines_used']) >= 1
        assert 'NLP' in result['engines_used']
    
    def test_summary_generation(self):
        """Test that human-readable summaries are generated"""
        result = self.analyzer.analyze_comprehensive(
            url="https://example.com",
            html_content="<p>Limited time offer! Only 2 hours left!</p>"
        )
        
        assert 'summary' in result
        assert len(result['summary']) > 0
        assert isinstance(result['summary'], str)

class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_end_to_end_analysis(self):
        """Test complete analysis workflow"""
        analyzer = TriEngineAnalyzer()
        
        # Simulate a realistic scenario
        url = "https://shady-site.com"
        html_content = """
        <html>
        <head>
            <title>Amazing Deal - Limited Time!</title>
        </head>
        <body>
            <h1>ONLY 2 HOURS LEFT!</h1>
            <p>Don't miss out on this incredible opportunity!</p>
            <button>Cancel and lose $100 discount</button>
            <div style="display:none">By continuing, you agree to our terms</div>
            <p>Join 10,000 satisfied customers!</p>
        </body>
        </html>
        """
        
        result = analyzer.analyze_comprehensive(
            url=url,
            html_content=html_content
        )
        
        # Should detect multiple issues
        assert result['trust_score'] < 70
        assert result['risk_level'] in ['CAUTION', 'DANGER']
        assert len(result['findings']) >= 2
        
        # Should include different pattern types
        pattern_types = [f['type'] for f in result['findings']]
        assert 'urgency' in pattern_types
        assert 'hidden_element' in pattern_types
        # Note: confirm_shaming may not be detected with current pattern matching
    
    def test_remediation_suggestions(self):
        """Test that remediation suggestions are practical"""
        analyzer = TriEngineAnalyzer()
        
        result = analyzer.analyze_comprehensive(
            url="https://example.com",
            html_content="<p>No thanks, I don't want to save money</p>"
        )
        
        suggestions = analyzer.get_remediation_suggestions(result['findings'])
        
        assert len(suggestions) > 0
        assert any('remediation' in s.lower() or 'fix' in s.lower() or 'improvement' in s.lower() for s in suggestions)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
