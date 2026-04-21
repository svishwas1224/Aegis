#!/usr/bin/env python3
"""
Aegis Pro Project Cleanup Script
Removes unnecessary files and folders while preserving essential functionality
"""

import os
import shutil
import glob

def cleanup_project():
    """Clean up unnecessary files and folders"""
    
    print("=== AEGIS PRO PROJECT CLEANUP ===\n")
    
    # Files and folders to remove
    cleanup_items = {
        # Debug files (no longer needed after development)
        "debug/": "Development debug scripts",
        
        # Duplicate frontend pages (keep enhanced versions)
        "frontend/src/pages/ClientHome.jsx": "Replaced by EnhancedClientHome.jsx",
        "frontend/src/pages/ClientHome.css": "Replaced by EnhancedClientHome.css", 
        "frontend/src/pages/AdminDashboard.jsx": "Replaced by EnhancedAdminDashboard.jsx",
        "frontend/src/pages/AdminDashboard.css": "Replaced by EnhancedAdminDashboard.css",
        
        # Large temporary files
        "frontend/project_code.txt": "Large temporary file (41MB)",
        
        # Build artifacts (can be regenerated)
        "frontend/dist/": "Build artifacts (can be regenerated)",
        "frontend/node_modules/": "Node modules (can be reinstalled)",
        
        # Cache files
        ".pytest_cache/": "Python test cache",
        "__pycache__/": "Python bytecode cache",
        
        # Temporary scripts
        "organize_files.py": "One-time organization script",
        
        # Duplicate reports (keep consolidated ones)
        "reports/testing/COMPREHENSIVE_TESTING_REPORT.md": "Superseded by main report",
        "reports/testing/FINAL_TESTING_REPORT.md": "Superseded by main report",
        
        # Old testing scripts (keep only essential ones)
        "scripts/testing/test_backend.py": "Basic backend test",
        "scripts/testing/test_system.py": "Basic system test", 
        "scripts/testing/test_extension_functionality.py": "Extension test",
    }
    
    # Files to keep (essential)
    essential_files = [
        "app.py",                    # Main backend server
        "requirements.txt",           # Python dependencies
        ".env",                      # Environment variables
        "package.json",              # Node dependencies
        "vite.config.js",           # Frontend build config
        ".gitignore",                # Git ignore rules
        "Procfile",                  # Deployment config
        "engines/",                  # Core detection engines
        "data/",                     # Data files
        "trust_pipeline/",           # Trust scoring system
        "aegis_extension/",          # Chrome extension
        "frontend/src/",             # Frontend source code
        "frontend/src/pages/EnhancedClientHome.jsx",
        "frontend/src/pages/EnhancedClientHome.css",
        "frontend/src/pages/EnhancedAdminDashboard.jsx", 
        "frontend/src/pages/EnhancedAdminDashboard.css",
        "frontend/src/pages/LandingPage.jsx",
        "frontend/src/pages/Landing.css",
        "frontend/src/pages/Analyze.jsx",
        "frontend/src/pages/Analyze.css",
        "frontend/src/pages/AuthPage.jsx",
        "frontend/src/pages/Auth.css",
        "frontend/src/pages/AdminLogin.jsx",
        "frontend/src/pages/AdminLogin.css",
        "frontend/src/pages/Dashboard.jsx",
        "frontend/src/pages/Dashboard.css",
        "frontend/src/pages/WebScraper.jsx",
        "frontend/src/pages/WebScraper.css",
        "scripts/",                  # Essential scripts
        "tests/",                    # Test suite
        "docs/",                     # Documentation
        "reports/",                   # Reports (keep organized structure)
        "AEGIS_PRO_STATUS.md",       # Current status
        "UI_UX_IMPROVEMENT_REPORT.md", # Enhancement report
    ]
    
    # Remove unnecessary items
    removed_count = 0
    space_saved = 0
    
    for item, reason in cleanup_items.items():
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    # Calculate directory size
                    size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                             for dirpath, dirnames, filenames in os.walk(item) 
                             for filename in filenames)
                    shutil.rmtree(item)
                    print(f"Removed directory: {item} ({size/1024/1024:.1f}MB) - {reason}")
                    space_saved += size
                else:
                    size = os.path.getsize(item)
                    os.remove(item)
                    print(f"Removed file: {item} ({size/1024/1024:.1f}MB) - {reason}")
                    space_saved += size
                removed_count += 1
            except Exception as e:
                print(f"Error removing {item}: {e}")
        else:
            print(f"Already removed: {item}")
    
    # Clean up Python cache files
    cache_files = glob.glob("**/__pycache__", recursive=True) + glob.glob("**/*.pyc", recursive=True)
    for cache_file in cache_files:
        try:
            if os.path.isdir(cache_file):
                shutil.rmtree(cache_file)
            else:
                os.remove(cache_file)
            removed_count += 1
        except Exception as e:
            print(f"Error removing cache {cache_file}: {e}")
    
    print(f"\n=== CLEANUP SUMMARY ===")
    print(f"Items removed: {removed_count}")
    print(f"Space saved: {space_saved/1024/1024:.1f}MB")
    print(f"Essential files preserved: {len(essential_files)}")
    
    # Verify essential files exist
    print(f"\n=== VERIFYING ESSENTIAL FILES ===")
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"Missing: {file_path}")
        else:
            print(f"Present: {file_path}")
    
    if missing_files:
        print(f"\nWARNING: {len(missing_files)} essential files missing!")
    else:
        print(f"\nAll essential files present!")
    
    print(f"\n=== CLEANUP COMPLETE ===")
    print("Project is now optimized and ready for deployment!")

if __name__ == "__main__":
    cleanup_project()
