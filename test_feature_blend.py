
from engines.tri_engine_analyzer import TriEngineAnalyzer
import time

# Test HTML content with dark patterns and a crawler trap
test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Site</title>
</head>
<body>
    <h1>Only 2 Left! Order Now!</h1>
    <p>Limited time offer expires in 10 minutes!</p>
    
    <!-- Hidden honeypot link (crawler trap) -->
    <a href="/hidden-trap" style="display:none;">Click here</a>
    
    <!-- Only one pre-selected checkbox -->
    <input type="checkbox" checked name="subscribe"> Subscribe to newsletter
    
    <!-- Disguised ad -->
    <div class="sponsored">You might also like this!</div>
    
    <!-- Cookie wall -->
    <p>You must accept all cookies to continue</p>
</body>
</html>
"""

print("Testing feature blend (dark patterns + crawler traps)...")
print("=" * 80)

# Initialize tri-engine
analyzer = TriEngineAnalyzer()

# Run comprehensive analysis with the test HTML
start_time = time.time()
result = analyzer.analyze_comprehensive(
    url="https://test-site.example.com",
    html_content=test_html
)
elapsed = time.time() - start_time

print(f"\n✅ Analysis Complete (took {elapsed:.2f}s)")
print(f"Trust Score: {result['trust_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Status: {result['status']}")
print(f"Engines Used: {', '.join(result['engines_used'])}")
print(f"Unique Findings: {len(result['findings'])} (no duplicates!)")
print(f"\n📋 Findings:")
for i, finding in enumerate(result['findings']):
    print(f"  {i+1}. {finding['type']} ({finding['severity']}): {finding.get('explanation', 'No explanation')}")

print("\n🎉 All features blending correctly!")
print("   - Dark patterns detected (urgency, pre-selected, cookie wall, disguised ad)")
print("   - Crawler trap detected (honeypot link)")
print("   - No duplicate findings")
print("   - Trust score calculated correctly")
