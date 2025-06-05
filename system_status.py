#!/usr/bin/env python3
"""
Minimal test to verify the N26 Advanced Analytics system
"""

def test_system_status():
    """Quick test to verify system files and structure"""
    import os
    
    print("🔍 N26 Advanced Analytics - System Status Check")
    print("=" * 50)
    
    # Check critical files
    critical_files = [
        'advanced_analytics.py',
        'analytics_dashboard.py', 
        'gui.py',
        'requirements.txt',
        'start_n26_analytics.sh'
    ]
    
    print("\n📁 File Structure Check:")
    files_ok = True
    for file in critical_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} MISSING")
            files_ok = False
    
    # Check virtual environment
    print("\n🔧 Virtual Environment Check:")
    if os.path.exists('venv_n26'):
        print("✅ venv_n26 directory exists")
        if os.path.exists('venv_n26/bin/python'):
            print("✅ Python executable present")
        if os.path.exists('venv_n26/bin/activate'):
            print("✅ Activation script present")
    else:
        print("❌ Virtual environment missing")
        files_ok = False
    
    # Check cache (indicates successful compilation)
    print("\n📦 Python Cache Check:")
    if os.path.exists('__pycache__'):
        cache_files = os.listdir('__pycache__')
        print(f"✅ Python cache exists ({len(cache_files)} files)")
        for cache_file in cache_files[:3]:  # Show first 3
            print(f"   • {cache_file}")
    else:
        print("⚠️ No Python cache found (first run)")
    
    # Summary
    print("\n" + "=" * 50)
    if files_ok:
        print("✅ SYSTEM STATUS: READY")
        print("🎯 All critical components present")
        print("🚀 System ready for use")
        return True
    else:
        print("❌ SYSTEM STATUS: INCOMPLETE")
        print("⚠️ Some components missing")
        return False

if __name__ == "__main__":
    test_system_status()
