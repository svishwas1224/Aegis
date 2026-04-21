#!/usr/bin/env python3
"""
Aegis Dark-Pattern Detector - Project Name Update Script
Updates all references from "Aegis Pro" to "Aegis Dark-Pattern Detector"
"""

import os
import re
from pathlib import Path

def update_file_content(file_path, old_name, new_name):
    """Update content in a file with new project name"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace various forms of the old name
        replacements = [
            (f"Aegis Pro", new_name),
            (f"AEGIS PRO", new_name.upper()),
            (f"aegis-pro", new_name.lower().replace(' ', '-')),
            (f"AegisPro", new_name.replace(' ', '')),
            (f"aegis_pro", new_name.lower().replace(' ', '_')),
        ]
        
        updated_content = content
        for old_text, new_text in replacements:
            updated_content = updated_content.replace(old_text, new_text)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def update_filename(directory, old_pattern, new_pattern):
    """Update filenames in directory"""
    try:
        for file_path in Path(directory).rglob(f"*{old_pattern}*"):
            new_path = file_path.name.replace(old_pattern, new_pattern)
            new_full_path = file_path.parent / new_path
            if file_path != new_full_path:
                file_path.rename(new_full_path)
                print(f"Renamed: {file_path} -> {new_path}")
    except Exception as e:
        print(f"Error renaming files in {directory}: {e}")

def main():
    """Main update function"""
    print("=== AEGIS DARK-PATTERN DETECTOR - PROJECT NAME UPDATE ===\n")
    
    old_name = "Aegis Pro"
    new_name = "Aegis Dark-Pattern Detector"
    
    # Files to update
    files_to_update = [
        "documentation/project/AEGIS_PRO_PROJECT_DOCUMENTATION.md",
        "documentation/project/AEGIS_PRO_STATUS.md",
        "documentation/project/UI_UX_IMPROVEMENT_REPORT.md",
        "documentation/reports/ENHANCED_REAL_WORLD_REPORT.md",
        "documentation/deployment/PROJECT_CLEANUP_SUMMARY.md",
        "documentation/deployment/404_ERROR_FIX_REPORT.md",
        "documentation/README.md",
        "documentation/ORGANIZATION_SUMMARY.md",
        "documentation/FINAL_PROJECT_STATUS.md",
        "documentation/DOCUMENTATION_EXPLANATION.md",
        "engines/tri_engine_analyzer.py",
        "trust_pipeline/pipeline.py",
        "frontend/src/App.jsx",
        "frontend/src/index.html",
    ]
    
    print("Updating file contents...")
    updated_count = 0
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_file_content(file_path, old_name, new_name):
                updated_count += 1
    
    print(f"\nUpdated {updated_count} files")
    
    # Update filenames if needed
    print("\nChecking for filename updates...")
    update_filename("documentation/project", "AEGIS_PRO", "AEGIS_DARK-PATTERN_DETECTOR")
    
    # Update package.json files
    print("\nUpdating package.json files...")
    package_files = [
        "package.json",
        "frontend/package.json"
    ]
    
    for package_file in package_files:
        if os.path.exists(package_file):
            update_file_content(package_file, "Aegis Pro", new_name)
            update_file_content(package_file, "AEGIS_PRO", "AEGIS_DARK-PATTERN_DETECTOR")
    
    print(f"\n=== UPDATE COMPLETE ===")
    print(f"Project name updated from '{old_name}' to '{new_name}'")
    print("Please review changes and test the application")

if __name__ == "__main__":
    main()
