#!/usr/bin/env python3
"""
Simple test script to verify system functionality
"""

print("🔍 Quick System Check")
print("=" * 30)

# Test 1: Basic Python
print("✅ Python is working")

# Test 2: Basic imports
try:
    import os
    import sys
    print("✅ Basic modules work")
except Exception as e:
    print(f"❌ Basic modules error: {e}")

# Test 3: Check if our main files exist
import os
files_to_check = [
    'advanced_analytics.py',
    'analytics_dashboard.py', 
    'gui.py',
    'final_validation.py'
]

print("\n📁 File Check:")
for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} missing")

# Test 4: Virtual environment check
if os.path.exists('venv_n26'):
    print("✅ Virtual environment exists")
else:
    print("❌ Virtual environment missing")

print("\n🎯 Basic checks complete!")
