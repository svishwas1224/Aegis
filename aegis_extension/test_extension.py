#!/usr/bin/env python3
"""
Test script to verify Aegis Pro Chrome Extension functionality
"""

import json
import os
import subprocess
import sys

def check_extension_files():
    """Check if all required extension files exist"""
    required_files = [
        'manifest.json',
        'src/background.js',
        'src/content.js',
        'src/ghost-writer.js',
        'src/popup/popup.html',
        'src/popup/popup.js',
        'src/panel/panel.html',
        'public/icons/icon16.png',
        'public/icons/icon32.png',
        'public/icons/icon48.png',
        'public/icons/icon128.png'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    
    print("All required files present!")
    return True

def validate_manifest():
    """Validate manifest.json structure"""
    try:
        with open('manifest.json', 'r') as f:
            manifest = json.load(f)
        
        required_keys = ['manifest_version', 'name', 'version', 'permissions']
        for key in required_keys:
            if key not in manifest:
                print(f"Missing manifest key: {key}")
                return False
        
        print("Manifest validation passed!")
        return True
    except Exception as e:
        print(f"Manifest validation failed: {e}")
        return False

def check_permissions():
    """Check if permissions are appropriate"""
    try:
        with open('manifest.json', 'r') as f:
            manifest = json.load(f)
        
        permissions = manifest.get('permissions', [])
        required_permissions = ['activeTab', 'scripting', 'storage']
        
        for perm in required_permissions:
            if perm not in permissions:
                print(f"Missing required permission: {perm}")
                return False
        
        print("Permissions check passed!")
        return True
    except Exception as e:
        print(f"Permissions check failed: {e}")
        return False

def create_test_page():
    """Create a test HTML page with dark patterns"""
    test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Aegis Pro Test Page</title>
</head>
<body>
    <h1>Test Dark Patterns</h1>
    
    <!-- Confirm Shaming -->
    <button onclick="alert('No thanks, I hate saving money!')">Decline Offer</button>
    
    <!-- Urgency -->
    <p>Limited time offer! Only 2 items left!</p>
    
    <!-- Hidden Exit -->
    <div style="background-color: white;">
        <button style="background-color: white; color: white;">X Close</button>
    </div>
    
    <!-- Pre-selected -->
    <form>
        <input type="checkbox" name="newsletter" checked> Subscribe to newsletter
    </form>
    
    <script>
        console.log('Aegis Pro Test Page Loaded');
    </script>
</body>
</html>
    """
    
    with open('test_page.html', 'w') as f:
        f.write(test_html)
    
    print("Test page created: test_page.html")

def main():
    """Run all extension tests"""
    print("=== Aegis Pro Extension Test Suite ===\n")
    
    tests = [
        ("File Check", check_extension_files),
        ("Manifest Validation", validate_manifest),
        ("Permissions Check", check_permissions),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"{test_name} FAILED!")
    
    print(f"\n=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("Extension is ready for deployment!")
        create_test_page()
    else:
        print("Fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
