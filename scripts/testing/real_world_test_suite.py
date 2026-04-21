#!/usr/bin/env python3
"""
Aegis Pro Real-World Live Testing Suite
Tests Aegis Pro against genuine dark pattern websites
"""

import requests
import time
import json
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from engines.tri_engine_analyzer import TriEngineAnalyzer

class RealWorldTester:
    def __init__(self):
        self.engine = TriEngineAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_website_content(self, url, timeout=10):
        """Fetch website content for analysis"""
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
                'headers': dict(response.headers)
            }
            
            return content
            
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def analyze_website(self, url, expected_patterns=None):
        """Analyze a website for dark patterns"""
        print(f"\n{'='*60}")
        print(f"ANALYZING: {url}")
        print(f"{'='*60}")
        
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
        
        # Generate detailed report
        report = {
            'url': url,
            'title': content['title'],
            'trust_score': result['trust_score'],
            'risk_level': self.get_risk_level(result['trust_score']),
            'analysis_time': f"{end_time - start_time:.3f}s",
            'findings_count': len(result['findings']),
            'findings': result['findings'],
            'engines_used': result.get('engines_used', []),
            'expected_patterns': expected_patterns or []
        }
        
        self.print_analysis_report(report)
        return report
    
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
    
    def print_analysis_report(self, report):
        """Print detailed analysis report"""
        print(f"\nTrust Score: {report['trust_score']}/100 ({report['risk_level']} RISK)")
        print(f"Analysis Time: {report['analysis_time']}")
        print(f"Findings Detected: {report['findings_count']}")
        print(f"Engines Used: {', '.join(report['engines_used'])}")
        
        if report['expected_patterns']:
            print(f"Expected Patterns: {', '.join(report['expected_patterns'])}")
        
        print(f"\n{'='*60}")
        print("DETAILED FINDINGS:")
        print(f"{'='*60}")
        
        for i, finding in enumerate(report['findings'], 1):
            print(f"\n{i}. {finding['type'].upper()} ({finding['severity']})")
            print(f"   Engine: {finding['engine']}")
            print(f"   Explanation: {finding['explanation']}")
            print(f"   Remediation: {finding['remediation']}")
            
            if 'source_text' in finding:
                source_text = finding['source_text']
                if len(source_text) > 100:
                    source_text = source_text[:100] + "..."
                print(f"   Evidence: {source_text}")
            
            if 'evidence' in finding:
                evidence = finding['evidence']
                if isinstance(evidence, dict):
                    evidence_str = ", ".join([f"{k}: {v}" for k, v in evidence.items()])
                    print(f"   Technical Evidence: {evidence_str}")
        
        # Technical proof output
        self.print_technical_proof(report)
    
    def print_technical_proof(self, report):
        """Print technical proof evidence"""
        print(f"\n{'='*60}")
        print("TECHNICAL PROOF EVIDENCE:")
        print(f"{'='*60}")
        
        linguistic_findings = [f for f in report['findings'] if f['engine'] == 'NLP']
        visual_findings = [f for f in report['findings'] if f['engine'] == 'VISUAL']
        behavioral_findings = [f for f in report['findings'] if f['engine'] == 'BEHAVIORAL']
        
        if linguistic_findings:
            print("\nLinguistic Engine Evidence:")
            for finding in linguistic_findings:
                confidence = self.calculate_confidence(finding)
                print(f"  Linguistic: \"Detected '{self.extract_pattern(finding)}' - Category: {finding['type']} (Confidence {confidence}%).\"")
        
        if visual_findings:
            print("\nVisual Engine Evidence:")
            for finding in visual_findings:
                print(f"  Visual: \"{finding['explanation']}\" - Category: {finding['type']}.")
        
        if behavioral_findings:
            print("\nBehavioral Engine Evidence:")
            for finding in behavioral_findings:
                print(f"  Behavioral: \"{finding['explanation']}\" - Category: {finding['type']}.")
    
    def calculate_confidence(self, finding):
        """Calculate confidence score for a finding"""
        # Simple confidence calculation based on severity and pattern strength
        base_confidence = 85
        
        if finding['severity'] == 'HIGH':
            base_confidence += 10
        elif finding['severity'] == 'CRITICAL':
            base_confidence += 15
        
        # Add confidence based on pattern specificity
        if 'source_text' in finding and len(finding['source_text']) > 50:
            base_confidence += 5
        
        return min(99, base_confidence)
    
    def extract_pattern(self, finding):
        """Extract the specific pattern detected"""
        if 'source_text' in finding:
            text = finding['source_text']
            # Extract key pattern (first 50 chars)
            return text[:50] + "..." if len(text) > 50 else text
        return finding['type']
    
    def run_comprehensive_test_suite(self):
        """Run the complete real-world test suite"""
        print("AEGIS PRO REAL-WORLD LIVE TESTING SUITE")
        print("=" * 60)
        print("Testing against genuine dark pattern websites...")
        print("=" * 60)
        
        # Real-world test cases
        test_cases = [
            # Main real-world sites
            {
                'url': 'https://www.ryanair.com',
                'name': 'Ryanair',
                'expected_patterns': ['hidden_costs', 'sneaking']
            },
            {
                'url': 'https://www.booking.com',
                'name': 'Booking.com',
                'expected_patterns': ['urgency', 'scarcity', 'social_proof']
            },
            {
                'url': 'https://www.agoda.com',
                'name': 'Agoda',
                'expected_patterns': ['social_proof', 'pressure']
            },
            {
                'url': 'https://www.namecheap.com',
                'name': 'Namecheap',
                'expected_patterns': ['preselected']
            },
            {
                'url': 'https://www.amazon.com',
                'name': 'Amazon',
                'expected_patterns': ['roach_motel', 'cancellation']
            },
            {
                'url': 'https://www.wsj.com',
                'name': 'WSJ',
                'expected_patterns': ['forced_continuity']
            },
            {
                'url': 'https://www.adobe.com',
                'name': 'Adobe',
                'expected_patterns': ['hidden_subscription']
            },
            
            # Forensic test URLs
            {
                'url': 'https://www.thredup.com',
                'name': 'Thredup',
                'expected_patterns': ['confirm_shaming', 'exit_intent']
            },
            {
                'url': 'https://www.shutterfly.com',
                'name': 'Shutterfly',
                'expected_patterns': ['fake_countdown', 'urgency']
            },
            {
                'url': 'https://www.hellofresh.com',
                'name': 'HelloFresh',
                'expected_patterns': ['forced_action', 'wall']
            },
            
            # Control sites (should be safe)
            {
                'url': 'https://www.gov.uk',
                'name': 'GOV.UK (Control)',
                'expected_patterns': []
            },
            {
                'url': 'https://www.wikipedia.org',
                'name': 'Wikipedia (Control)',
                'expected_patterns': []
            },
            {
                'url': 'https://www.expedia.com',
                'name': 'Expedia (Deceptive Control)',
                'expected_patterns': ['scarcity', 'pressure']
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            print(f"\n\n{'#'*80}")
            print(f"TESTING: {test_case['name']}")
            print(f"URL: {test_case['url']}")
            print(f"Expected Patterns: {', '.join(test_case['expected_patterns']) if test_case['expected_patterns'] else 'None'}")
            print(f"{'#'*80}")
            
            try:
                result = self.analyze_website(
                    test_case['url'], 
                    test_case['expected_patterns']
                )
                
                if result:
                    result['name'] = test_case['name']
                    result['expected_patterns'] = test_case['expected_patterns']
                    results.append(result)
                
                # Add delay between requests to be respectful
                time.sleep(2)
                
            except Exception as e:
                print(f"Error testing {test_case['name']}: {str(e)}")
                continue
        
        # Generate summary report
        self.generate_summary_report(results)
        
        return results
    
    def generate_summary_report(self, results):
        """Generate summary report of all tests"""
        print(f"\n\n{'='*80}")
        print("AEGIS PRO REAL-WORLD TESTING SUMMARY")
        print(f"{'='*80}")
        
        if not results:
            print("No results to report.")
            return
        
        # Calculate statistics
        total_tests = len(results)
        avg_trust_score = sum(r['trust_score'] for r in results) / total_tests
        high_risk_sites = [r for r in results if r['trust_score'] < 50]
        medium_risk_sites = [r for r in results if 50 <= r['trust_score'] < 70]
        low_risk_sites = [r for r in results if r['trust_score'] >= 70]
        
        print(f"Total Sites Tested: {total_tests}")
        print(f"Average Trust Score: {avg_trust_score:.1f}/100")
        print(f"High Risk Sites (<50): {len(high_risk_sites)}")
        print(f"Medium Risk Sites (50-70): {len(medium_risk_sites)}")
        print(f"Low Risk Sites (>=70): {len(low_risk_sites)}")
        
        print(f"\n{'='*80}")
        print("SITE RANKINGS (WORST TO BEST)")
        print(f"{'='*80}")
        
        # Sort by trust score (worst first)
        sorted_results = sorted(results, key=lambda x: x['trust_score'])
        
        for i, result in enumerate(sorted_results, 1):
            risk_indicator = "DANGEROUS" if result['trust_score'] < 30 else "HIGH" if result['trust_score'] < 50 else "MEDIUM" if result['trust_score'] < 70 else "LOW"
            print(f"{i:2d}. {result['name']:20s} - Score: {int(result['trust_score']):3d}/100 ({risk_indicator:9s})")
        
        # Pattern detection summary
        print(f"\n{'='*80}")
        print("PATTERN DETECTION SUMMARY")
        print(f"{'='*80}")
        
        pattern_counts = {}
        for result in results:
            for finding in result['findings']:
                pattern_type = finding['type']
                pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        # Sort by frequency
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        
        for pattern, count in sorted_patterns:
            print(f"{pattern:25s}: {count} occurrences")
        
        # Control site verification
        print(f"\n{'='*80}")
        print("CONTROL SITE VERIFICATION")
        print(f"{'='*80}")
        
        control_sites = [r for r in results if 'Control' in r['name']]
        for site in control_sites:
            expected_safe = 'GOV.UK' in site['name'] or 'Wikipedia' in site['name']
            actual_safe = site['trust_score'] >= 70
            
            status = "CORRECT" if expected_safe == actual_safe else "INCORRECT"
            print(f"{site['name']:20s} - Score: {site['trust_score']:3d}/100 - Expected Safe: {expected_safe} - Actual Safe: {actual_safe} - {status}")

def main():
    """Main function to run the real-world test suite"""
    tester = RealWorldTester()
    results = tester.run_comprehensive_test_suite()
    
    print(f"\n\n{'='*80}")
    print("TESTING COMPLETE")
    print(f"{'='*80}")
    print(f"Analyzed {len(results)} real-world websites")
    print("Results saved to analysis output above")
    print("\nAegis Pro Real-World Testing Suite - COMPLETE")

if __name__ == "__main__":
    main()
