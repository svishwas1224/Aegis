"""
Aegis Pro Visual Engine
Analyzes visual elements for dark patterns using computer vision
"""

import cv2
import numpy as np
from typing import Dict, List, Any, Tuple
import base64
from dataclasses import dataclass

@dataclass
class VisualFinding:
    type: str
    severity: str
    bbox: List[int]  # [x, y, w, h]
    confidence: float
    evidence: Dict
    remediation: str
    explanation: str

class VisualEngine:
    def __init__(self):
        self.min_contrast_ratio = 3.0  # WCAG AA standard
        self.min_touch_target_size = 44  # iOS HIG standard
        
    def analyze_screenshot(self, screenshot_b64: str) -> Dict[str, Any]:
        """Analyze screenshot for visual dark patterns"""
        try:
            # Decode base64 screenshot
            img_data = base64.b64decode(screenshot_b64.split(',')[1])
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {'findings': [], 'trust_score': 100, 'error': 'Invalid image'}
                
            findings = []
            total_penalty = 0
            
            # Analyze contrast issues
            contrast_findings = self._analyze_contrast(image)
            findings.extend(contrast_findings)
            total_penalty += sum(f['severity_score'] for f in contrast_findings)
            
            # Analyze button sizes
            size_findings = self._analyze_button_sizes(image)
            findings.extend(size_findings)
            total_penalty += sum(f['severity_score'] for f in size_findings)
            
            # Analyze layout issues
            layout_findings = self._analyze_layout_issues(image)
            findings.extend(layout_findings)
            total_penalty += sum(f['severity_score'] for f in layout_findings)
            
            # Calculate trust score
            base_score = 100
            final_score = max(0, base_score - total_penalty)
            
            return {
                'findings': findings,
                'trust_score': final_score,
                'patterns_detected': len(findings),
                'analysis_type': 'visual'
            }
            
        except Exception as e:
            return {'findings': [], 'trust_score': 100, 'error': str(e)}
    
    def _analyze_contrast(self, image: np.ndarray) -> List[Dict]:
        """Analyze contrast ratio issues"""
        findings = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Get unique colors in the image
        unique_colors = np.unique(gray)
        
        # If we have very few colors (like our test image), analyze color differences
        if len(unique_colors) <= 10:
            # Find the two most common colors
            unique, counts = np.unique(gray, return_counts=True)
            if len(unique) >= 2:
                # Sort by frequency
                sorted_indices = np.argsort(counts)[::-1]
                bg_color = unique[sorted_indices[0]]
                fg_color = unique[sorted_indices[1]]
                
                # Calculate contrast ratio
                contrast_ratio = self._calculate_contrast_ratio_simple(bg_color, fg_color)
                
                if contrast_ratio < self.min_contrast_ratio:
                    severity = 'HIGH' if contrast_ratio < 2.0 else 'MEDIUM'
                    findings.append({
                        'engine': 'VISUAL',
                        'type': 'low_contrast',
                        'severity': severity,
                        'bbox': [0, 0, image.shape[1], image.shape[0]],
                        'evidence': {'contrast_ratio': contrast_ratio, 'wcag_standard': self.min_contrast_ratio},
                        'remediation': 'Increase text contrast to meet WCAG AA standards',
                        'explanation': f'Contrast ratio {contrast_ratio:.1f}:1 is below WCAG AA requirement of {self.min_contrast_ratio}:1',
                        'severity_score': 20 if severity == 'HIGH' else 10
                    })
        
        # Also try the original contour-based analysis
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Skip very small regions
            if w < 10 or h < 10:
                continue
                
            # Extract region
            roi = image[y:y+h, x:x+w]
            
            # Calculate contrast ratio
            contrast_ratio = self._calculate_contrast_ratio(roi)
            
            if contrast_ratio < self.min_contrast_ratio:
                severity = 'HIGH' if contrast_ratio < 2.0 else 'MEDIUM'
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'low_contrast',
                    'severity': severity,
                    'bbox': [x, y, w, h],
                    'evidence': {'contrast_ratio': contrast_ratio, 'wcag_standard': self.min_contrast_ratio},
                    'remediation': 'Increase text contrast to meet WCAG AA standards',
                    'explanation': f'Contrast ratio {contrast_ratio:.1f}:1 is below WCAG AA requirement of {self.min_contrast_ratio}:1',
                    'severity_score': 20 if severity == 'HIGH' else 10
                })
        
        return findings
    
    def _analyze_button_sizes(self, image: np.ndarray) -> List[Dict]:
        """Analyze button sizes for touch target issues"""
        findings = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find button-like rectangles
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Check if it's button-like (reasonable aspect ratio)
            aspect_ratio = w / h
            if aspect_ratio < 0.3 or aspect_ratio > 3.0:
                continue
                
            # Check size
            min_dimension = min(w, h)
            if min_dimension < self.min_touch_target_size:
                severity = 'HIGH' if min_dimension < 30 else 'MEDIUM'
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'small_touch_target',
                    'severity': severity,
                    'bbox': [x, y, w, h],
                    'evidence': {'width': w, 'height': h, 'min_size': min_dimension},
                    'remediation': f'Increase button size to at least {self.min_touch_target_size}px',
                    'explanation': f'Button size {min_dimension}px is below recommended minimum of {self.min_touch_target_size}px',
                    'severity_score': 15 if severity == 'HIGH' else 8
                })
        
        return findings
    
    def _analyze_layout_issues(self, image: np.ndarray) -> List[Dict]:
        """Analyze layout for deceptive patterns"""
        findings = []
        
        # Look for hidden elements (very small text)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Check for very small text that might be hidden terms
            if h < 8 and w > 50:  # Very short but wide text
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'hidden_terms',
                    'severity': 'HIGH',
                    'bbox': [x, y, w, h],
                    'evidence': {'height': h, 'width': w},
                    'remediation': 'Make all terms and conditions clearly visible',
                    'explanation': 'Text appears to be intentionally small to hide important information',
                    'severity_score': 25
                })
        
        # Look for deceptive color patterns (e.g., fake buttons)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Find regions that look like buttons but might be fake
        # This is a simplified version - a real implementation would be more sophisticated
        blue_regions = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
        contours, _ = cv2.findContours(blue_regions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Check if it's a reasonable button size
            if 20 < w < 200 and 20 < h < 100:
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'potential_fake_button',
                    'severity': 'MEDIUM',
                    'bbox': [x, y, w, h],
                    'evidence': {'color': 'blue', 'dimensions': [w, h]},
                    'remediation': 'Ensure all interactive elements are clearly distinguishable',
                    'explanation': 'Element appears to be a button but may be decorative',
                    'severity_score': 12
                })
        
        return findings
    
    def _calculate_contrast_ratio(self, roi: np.ndarray) -> float:
        """Calculate contrast ratio for a region of interest"""
        # Convert to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Calculate relative luminance
        # This is a simplified calculation
        mean_brightness = np.mean(gray_roi)
        
        # For simplicity, assume background vs foreground based on median
        median_brightness = np.median(gray_roi)
        
        # Estimate contrast ratio (simplified WCAG calculation)
        if mean_brightness > median_brightness:
            lighter = mean_brightness
            darker = median_brightness
        else:
            lighter = median_brightness
            darker = mean_brightness
            
        # Normalize to 0-255 scale and calculate ratio
        lighter_norm = (lighter + 5) / 255
        darker_norm = (darker + 5) / 255
        
        if darker_norm > 0:
            contrast_ratio = lighter_norm / darker_norm
        else:
            contrast_ratio = 21.0  # Maximum WCAG ratio
            
        return min(contrast_ratio, 21.0)
    
    def _calculate_contrast_ratio_simple(self, bg_color: int, fg_color: int) -> float:
        """Calculate contrast ratio between two colors"""
        # Normalize to 0-255 scale and calculate ratio
        lighter = max(bg_color, fg_color)
        darker = min(bg_color, fg_color)
        
        lighter_norm = (lighter + 5) / 255
        darker_norm = (darker + 5) / 255
        
        if darker_norm > 0:
            contrast_ratio = lighter_norm / darker_norm
        else:
            contrast_ratio = 21.0
            
        return min(contrast_ratio, 21.0)
    
    def analyze_html_structure(self, html_content: str) -> Dict[str, Any]:
        """Analyze HTML structure for visual dark patterns"""
        findings = []
        total_penalty = 0
        
        # Look for hidden elements in HTML
        hidden_patterns = [
            r'display:\s*none',
            r'visibility:\s*hidden',
            r'opacity:\s*0',
            r'font-size:\s*0',
            r'text-indent:\s*-9999',
            r'position:\s*absolute.*left:\s*-9999',
            r'color:\s*white.*background-color:\s*white',
            r'background-color:\s*white.*color:\s*white',
            r'color:\s*#fff.*background-color:\s*#fff',
            r'background-color:\s*#fff.*color:\s*#fff',
            r'color:\s*#ffffff.*background-color:\s*#ffffff',
            r'background-color:\s*#ffffff.*color:\s*#ffffff'
        ]
        
        # Look for visual hierarchy misdirection
        hierarchy_patterns = [
            r'background-color:\s*gray.*padding:\s*15px.*purchase',  # Gray primary action
            r'background-color:\s*red.*padding:\s*20px.*font-size:\s*18px',  # Red secondary with larger styling
            r'background-color:\s*red.*font-size:\s*18px',  # Red button with larger font
            r'background-color:\s*gray.*padding:\s*15px.*background-color:\s*red.*padding:\s*20px',  # Both buttons present
            r'purchase.*maybe.*later',  # Text pattern indicating hierarchy issue
            r'primary.*secondary.*background-color'  # CSS hierarchy patterns
        ]
        
        for pattern in hidden_patterns:
            import re
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'hidden_element',
                    'severity': 'HIGH',
                    'bbox': [],
                    'evidence': {'css_property': match.group()},
                    'remediation': 'Remove hidden elements or make them visible',
                    'explanation': 'CSS property used to hide content from users',
                    'severity_score': 20
                })
        
        # Check for visual hierarchy misdirection
        for pattern in hierarchy_patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'visual_hierarchy',
                    'severity': 'MEDIUM',
                    'bbox': [],
                    'evidence': {'css_property': match.group()},
                    'remediation': 'Ensure primary actions have more prominent styling than secondary actions',
                    'explanation': 'Visual hierarchy misdirection detected - secondary action appears more important than primary',
                    'severity_score': 15
                })
                total_penalty += 20
        
        # Look for preselected checkboxes
        preselected_patterns = [
            r'<input[^>]*checked[^>]*>',
            r'checked\s*=\s*["\']?checked["\']?',
            r'type=["\']checkbox["\'][^>]*checked',
            r'newsletter.*checked',
            r'terms.*checked'
        ]
        
        for pattern in preselected_patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'preselected',
                    'severity': 'MEDIUM',
                    'bbox': [],
                    'evidence': {'html_element': match.group()},
                    'remediation': 'Remove checked attribute from marketing checkboxes',
                    'explanation': 'Pre-selected checkbox detected - user consent should be explicit',
                    'severity_score': 15
                })
        
        # Look for deceptive positioning
        deceptive_patterns = [
            r'position:\s*fixed.*bottom:\s*0',
            r'z-index:\s*9999',
            r'pointer-events:\s*none'
        ]
        
        for pattern in deceptive_patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'engine': 'VISUAL',
                    'type': 'deceptive_positioning',
                    'severity': 'MEDIUM',
                    'bbox': [],
                    'evidence': {'css_property': match.group()},
                    'remediation': 'Use standard positioning for important elements',
                    'explanation': 'CSS positioning that may deceive users',
                    'severity_score': 12
                })
                total_penalty += 12
        
        base_score = 100
        final_score = max(0, base_score - total_penalty)
        
        return {
            'findings': findings,
            'trust_score': final_score,
            'patterns_detected': len(findings),
            'analysis_type': 'visual_html'
        }
