"""
Aegis Pro Comprehensive Test Suite
Testing all 100 test cases across 8 phases
"""

import pytest
import sys
import os
import time
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.tri_engine_analyzer import TriEngineAnalyzer
from engines.linguistic_engine import LinguisticEngine
from engines.visual_engine import VisualEngine
from engines.behavioral_engine import BehavioralEngine

class TestPhase1_LinguisticSemantic:
    """Phase 1: Linguistic & Semantic (LLM/NLP) Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def test_TC01_confirm_shaming_detection(self):
        """TC-01: Detect "Confirm Shaming" in subscription pop-ups"""
        text = "No thanks, I hate saving money and don't want exclusive deals"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        confirm_shaming_found = any(
            f['type'] == 'confirm_shaming' and 'hate' in f.get('evidence', {}).get('pattern_matched', '')
            for f in result['findings']
        )
        assert confirm_shaming_found, f"Expected confirm shaming detection for: {text}"
        assert result['trust_score'] < 85
    
    def test_TC02_urgency_detection(self):
        """TC-02: Detect "Urgency" using time-sensitive keywords"""
        text = "Offer expires in 5 minutes! Limited time only!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        urgency_found = any(
            f['type'] == 'urgency' and 'expires in' in f.get('evidence', {}).get('pattern_matched', '')
            for f in result['findings']
        )
        assert urgency_found, f"Expected urgency detection for: {text}"
    
    def test_TC03_scarcity_detection(self):
        """TC-03: Detect "Scarcity" text patterns"""
        text = "Only 2 items left in stock. Almost gone!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        scarcity_found = any(
            f['type'] == 'scarcity' and 'only 2 items left' in f.get('evidence', {}).get('pattern_matched', '')
            for f in result['findings']
        )
        assert scarcity_found, f"Expected scarcity detection for: {text}"
    
    def test_TC04_social_proof_fabrications(self):
        """TC-04: Detect "Social Proof" fabrications"""
        text = "1,200 people are viewing this right now. Join them!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        social_proof_found = any(
            f['type'] == 'social_proof' and 'people are viewing' in f.get('evidence', {}).get('pattern_matched', '')
            for f in result['findings']
        )
        assert social_proof_found, f"Expected social proof detection for: {text}"
    
    def test_TC05_testimonial_pressure(self):
        """TC-05: Detect "Testimonial Pressure" (Fake reviews)"""
        text = "John D. says: 'This changed my life! 5 stars!' - Verified Purchase"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Check for testimonial patterns
        testimonial_found = any(
            f['type'] == 'testimonial_pressure' or 
            ('testimonial' in f.get('explanation', '').lower() and 'verified' in text.lower())
            for f in result['findings']
        )
        assert testimonial_found, f"Expected testimonial pressure detection for: {text}"
    
    def test_TC06_security_pressure(self):
        """TC-06: Detect "Security Pressure"""
        text = "Your PC is infected with 5 viruses! Download antivirus now!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        security_found = any(
            f['type'] == 'security_pressure' or 
            ('security' in f.get('explanation', '').lower() and 'infected' in text.lower())
            for f in result['findings']
        )
        assert security_found, f"Expected security pressure detection for: {text}"
    
    def test_TC07_friend_spam(self):
        """TC-07: Detect "Friend Spam"""
        text = "Invite 5 friends to unlock premium features. Share contacts now!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        friend_spam_found = any(
            f['type'] == 'friend_spam' or 
            ('social' in f.get('explanation', '').lower() and 'invite friends' in text.lower())
            for f in result['findings']
        )
        assert friend_spam_found, f"Expected friend spam detection for: {text}"
    
    def test_TC08_ambiguous_labeling(self):
        """TC-08: Detect "Ambiguous Labeling"""
        text = "Click Next to complete your purchase of $99.99"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<button>{text}</button>"
        )
        
        ambiguous_found = any(
            f['type'] == 'ambiguous_labeling' or 
            ('misdirection' in f.get('explanation', '').lower() and 'next' in text.lower() and 'purchase' in text.lower())
            for f in result['findings']
        )
        assert ambiguous_found, f"Expected ambiguous labeling detection for: {text}"
    
    def test_TC09_double_negatives(self):
        """TC-09: Check for "Double Negatives" in cookie settings"""
        text = "Don't not accept our cookies to continue"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Check for confusing language patterns
        confusing_found = any(
            'double' in f.get('explanation', '').lower() or 'negative' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert confusing_found, f"Expected detection of confusing double negative: {text}"
    
    def test_TC10_hidden_costs(self):
        """TC-10: Identify "Hidden Costs" mentions"""
        text = "*Processing fee of $3.99 applies to all orders. See footer for details."
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<footer><p>{text}</p></footer>"
        )
        
        hidden_costs_found = any(
            f['type'] == 'hidden_costs' or 
            ('cost' in f.get('explanation', '').lower() and 'fee' in text.lower())
            for f in result['findings']
        )
        assert hidden_costs_found, f"Expected hidden costs detection for: {text}"
    
    def test_TC11_bait_and_switch(self):
        """TC-11: Detect "Bait and Switch" wording"""
        text = "FREE iPhone! Just pay $99.99 shipping and handling"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        bait_switch_found = any(
            f['type'] == 'bait_and_switch' or 
            ('bait' in f.get('explanation', '').lower() or 'switch' in f.get('explanation', '').lower())
            for f in result['findings']
        )
        assert bait_switch_found, f"Expected bait and switch detection for: {text}"
    
    def test_TC12_non_english_strings(self):
        """TC-12: Test with Non-English strings"""
        text = "¡Oferta especial! Solo por tiempo limitado!"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Should detect urgency patterns even in Spanish
        urgency_found = any(
            f['type'] == 'urgency' or 'tiempo limitado' in f.get('evidence', {}).get('pattern_matched', '')
            for f in result['findings']
        )
        assert urgency_found, f"Expected detection of urgency in Spanish: {text}"
    
    def test_TC13_sarcastic_strings(self):
        """TC-13: Test with Sarcastic strings"""
        text = "Oh yeah, we TOTALLY won't spam you with 50 emails a day *wink wink*"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Should detect potential deception
        deception_found = any(
            f['type'] in ['confirm_shaming', 'misdirection'] or
            ('spam' in f.get('explanation', '').lower() and '50 emails' in text.lower())
            for f in result['findings']
        )
        assert deception_found, f"Expected detection of deceptive sarcastic text: {text}"
    
    def test_TC14_false_positive_low_stock(self):
        """TC-14: Verify False Positive: Legitimate "Low Stock" shouldn't be flagged"""
        text = "Low Stock: 3 items remaining - Genuine inventory update"
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Should have higher trust score for legitimate inventory
        assert result['trust_score'] >= 70, f"Legitimate low stock should have higher trust score: {result['trust_score']}"
    
    def test_TC15_false_positive_arrival_time(self):
        """TC-15: Verify False Positive: "Order arriving today" shouldn't be flagged"""
        text = "Your order is arriving today between 2-4 PM. Track your package."
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=f"<p>{text}</p>"
        )
        
        # Should have higher trust score for neutral shipping info
        assert result['trust_score'] >= 75, f"Neutral shipping info should have higher trust score: {result['trust_score']}"

class TestPhase2_VisualHeuristic:
    """Phase 2: Visual & Heuristic (OpenCV/Computer Vision) Testing"""
    
    def setup_method(self):
        self.engine = TriEngineAnalyzer()
    
    def create_test_image(self, width=400, height=300, bg_color=(255, 255, 255), elements=None):
        """Create a test image for visual analysis"""
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        if elements:
            for element in elements:
                if element['type'] == 'button':
                    draw.rectangle([element['x'], element['y'], element['x']+element['w'], element['y']+element['h']], 
                                 fill=element.get('fill', (200, 200, 200)))
                elif element['type'] == 'text':
                    draw.text([element['x'], element['y']], element['text'], fill=element.get('color', (0, 0, 0)))
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def test_TC16_low_contrast_buttons(self):
        """TC-16: Identify buttons with contrast ratio < 3:1"""
        # Create image with low contrast button
        img_b64 = self.create_test_image(
            elements=[{
                'type': 'button',
                'x': 50, 'y': 50, 'w': 100, 'h': 30,
                'fill': (240, 240, 240)  # Very light gray on white background
            }]
        )
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            screenshot_b64=img_b64
        )
        
        low_contrast_found = any(
            f['type'] == 'low_contrast' or 'contrast' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert low_contrast_found, "Expected detection of low contrast buttons"
    
    def test_TC17_hidden_exit(self):
        """TC-17: Detect "Hidden Exit" (X button same color as background)"""
        html_content = """
        <div style="background-color: white; padding: 20px;">
            <button style="background-color: white; color: white; border: none;">X</button>
            <p>Popup content</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        hidden_exit_found = any(
            f['type'] == 'hidden_element' and 'color: white' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert hidden_exit_found, "Expected detection of hidden exit button"
    
    def test_TC18_visual_hierarchy_misdirection(self):
        """TC-18: Detect "Visual Hierarchy Misdirection" """
        html_content = """
        <div>
            <button style="background-color: gray; padding: 15px;">Primary Action - Purchase</button>
            <button style="background-color: red; padding: 20px; font-size: 18px;">Secondary - Maybe Later</button>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        hierarchy_issue_found = any(
            f['type'] == 'visual_hierarchy' or 'misdirection' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert hierarchy_issue_found, "Expected detection of visual hierarchy misdirection"
    
    def test_TC19_false_hierarchy(self):
        """TC-19: Identify "False Hierarchy" (Checkboxes that look like buttons)"""
        html_content = """
        <div>
            <input type="checkbox" style="width: 100px; height: 40px; background: blue; border: none;">
            <label>Subscribe to newsletter</label>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        false_hierarchy_found = any(
            f['type'] == 'false_hierarchy' or 'checkbox' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert false_hierarchy_found, "Expected detection of false hierarchy"
    
    def test_TC20_trick_questions_layout(self):
        """TC-20: Detect "Trick Questions" (reversed Yes/No positions)"""
        html_content = """
        <div style="display: flex; flex-direction: row-reverse;">
            <button style="background: red;">Yes, I agree to pay</button>
            <button style="background: green;">No, I don't want to pay</button>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        trick_layout_found = any(
            f['type'] == 'trick_question' or 'reversed' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert trick_layout_found, "Expected detection of trick question layout"
    
    def test_TC21_nagging_overlays(self):
        """TC-21: Detect "Nagging" overlays covering > 50% screen"""
        html_content = """
        <div style="position: fixed; top: 0; left: 0; width: 80vw; height: 80vh; background: rgba(0,0,0,0.8); z-index: 9999;">
            <div style="color: white; text-align: center; margin-top: 40vh;">
                <h2>SUBSCRIBE NOW!</h2>
                <button>Close</button>
            </div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        nagging_found = any(
            f['type'] == 'nagging' or 'overlay' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert nagging_found, "Expected detection of nagging overlay"
    
    def test_TC22_fake_close_buttons(self):
        """TC-22: Detect "Fake Close" buttons that are ads"""
        html_content = """
        <div>
            <img src="close-button.png" alt="X" onclick="window.open('https://ads.example.com')" style="cursor: pointer;">
            <p>Don't want to miss our offers!</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        fake_close_found = any(
            f['type'] == 'fake_close' or 'ad' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert fake_close_found, "Expected detection of fake close button"
    
    def test_TC23_preselected_checkboxes(self):
        """TC-23: Identify "Pre-selected checkboxes" for marketing"""
        html_content = """
        <form>
            <input type="checkbox" name="newsletter" checked> Send me marketing emails
            <input type="checkbox" name="terms" checked> I agree to terms
        </form>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        preselected_found = any(
            f['type'] == 'preselected' or 'checked' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert preselected_found, "Expected detection of pre-selected checkboxes"
    
    def test_TC24_infinite_scroll_traps(self):
        """TC-24: Detect "Infinite Scroll" traps"""
        html_content = """
        <div>
            <script>
                window.addEventListener('scroll', function() {
                    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                        loadMoreContent();
                    }
                });
            </script>
            <div id="content">Content that keeps loading...</div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        infinite_scroll_found = any(
            f['type'] == 'infinite_scroll' or 'scroll' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert infinite_scroll_found, "Expected detection of infinite scroll trap"
    
    def test_TC25_disguised_ads(self):
        """TC-25: Identify "Disguised Ads" (ads that look like news)"""
        html_content = """
        <div class="news-article" style="border: 1px solid #ccc; padding: 10px;">
            <h3>Breaking: You Won't Believe This One Trick!</h3>
            <p>Sponsored content</p>
            <a href="https://spam.example.com">Read More</a>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        disguised_ad_found = any(
            f['type'] == 'disguised_ad' or 'sponsored' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert disguised_ad_found, "Expected detection of disguised ad"
    
    def test_TC26_tiny_font_disclaimers(self):
        """TC-26: Detect "Tiny Font" for critical legal disclaimers"""
        html_content = """
        <div>
            <h1>Buy Now!</h1>
            <p style="font-size: 6px; color: #999;">*By purchasing you agree to our 50-page terms and auto-renewal subscription</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        tiny_font_found = any(
            f['type'] == 'tiny_font' or 'font-size: 6px' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert tiny_font_found, "Expected detection of tiny font disclaimer"
    
    def test_TC27_color_coded_manipulation(self):
        """TC-27: Detect "Color-coded manipulation" """
        html_content = """
        <div>
            <button style="background-color: red; color: white;">Cancel Subscription</button>
            <button style="background-color: green; color: white;">Keep Premium</button>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        color_manipulation_found = any(
            f['type'] == 'color_manipulation' or 'red' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert color_manipulation_found, "Expected detection of color-coded manipulation"
    
    def test_TC28_hidden_unsubscribe(self):
        """TC-28: Detect "Hidden Unsubscribe" links"""
        html_content = """
        <div style="background-color: white;">
            <p style="color: white; font-size: 8px;">Unsubscribe here</p>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        hidden_unsubscribe_found = any(
            f['type'] == 'hidden_element' and 'unsubscribe' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert hidden_unsubscribe_found, "Expected detection of hidden unsubscribe link"
    
    def test_TC29_overlapping_elements(self):
        """TC-29: Detect "Overlapping Elements" that hide buttons"""
        html_content = """
        <div style="position: relative;">
            <button style="position: absolute; z-index: 1;">Decline</button>
            <div style="position: absolute; z-index: 2; background: white; width: 100px; height: 30px;"></div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        overlapping_found = any(
            f['type'] == 'overlapping_elements' or 'z-index' in str(f.get('evidence', {}))
            for f in result['findings']
        )
        assert overlapping_found, "Expected detection of overlapping elements"
    
    def test_TC30_popup_interference(self):
        """TC-30: Check for "Pop-up interference" (multiple layered pop-ups)"""
        html_content = """
        <div>
            <div style="position: fixed; z-index: 9998;">First popup</div>
            <div style="position: fixed; z-index: 9999;">Second popup</div>
            <div style="position: fixed; z-index: 10000;">Third popup</div>
        </div>
        """
        
        result = self.engine.analyze_comprehensive(
            url="https://example.com",
            html_content=html_content
        )
        
        popup_interference_found = any(
            f['type'] == 'popup_interference' or 'popup' in f.get('explanation', '').lower()
            for f in result['findings']
        )
        assert popup_interference_found, "Expected detection of popup interference"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
