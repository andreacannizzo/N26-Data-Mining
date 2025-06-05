#!/usr/bin/env python3
"""
N26 Data Mining - Health Check
Verifica lo stato del sistema e delle dipendenze
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica versione Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  Raccomandato Python 3.8+")
        return False
    return True

def check_virtual_env():
    """Verifica ambiente virtuale"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Ambiente virtuale: presente")
        return True
    else:
        print("❌ Ambiente virtuale: mancante")
        print("💡 Esegui: python -m venv venv")
        return False

def check_files():
    """Verifica file principali"""
    required_files = [
        "main.py",
        "definitions.py", 
        "gui.py",
        "requirements.txt",
        "inputs_example.py"
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}: presente")
        else:
            print(f"❌ {file}: mancante")
            all_good = False
    
    return all_good

def check_dependencies():
    """Verifica dipendenze Python"""
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "import PyQt5, pandas, matplotlib, selenium; print('✅ Dipendenze principali: OK')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print("❌ Dipendenze principali: mancanti")
            print("💡 Esegui: pip install -r requirements.txt")
            return False
    except Exception:
        print("❌ Impossibile verificare dipendenze")
        return False

def check_display():
    """Verifica supporto GUI"""
    display = os.environ.get('DISPLAY')
    if display:
        print(f"✅ Display: {display}")
        return True
    else:
        print("⚠️  DISPLAY non impostato - GUI potrebbe non funzionare")
        print("💡 Per test headless: QT_QPA_PLATFORM=offscreen")
        return False

def check_chrome():
    """Verifica presenza Chrome/Chromium"""
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser", 
        "/usr/bin/chromium",
        "/snap/bin/chromium"
    ]
    
    for path in chrome_paths:
        if Path(path).exists():
            print(f"✅ Browser: {path}")
            return True
    
    print("⚠️  Chrome/Chromium non trovato")
    print("💡 Installa: sudo apt install chromium-browser")
    return False

def run_health_check():
    """Esegue controllo completo"""
    print("🏥 N26 Data Mining - Health Check")
    print("=" * 50)
    
    checks = [
        ("Versione Python", check_python_version),
        ("Ambiente virtuale", check_virtual_env),
        ("File principali", check_files), 
        ("Dipendenze Python", check_dependencies),
        ("Supporto GUI", check_display),
        ("Browser", check_chrome)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("🎉 SISTEMA PRONTO!")
        print("✅ Tutte le verifiche sono passate")
        print("\n🚀 Puoi avviare la GUI con: ./start_gui.sh")
    else:
        failed = sum(1 for r in results if not r)
        print(f"⚠️  {failed} verifiche fallite")
        print("🔧 Risolvi i problemi segnalati sopra")
    
    print("=" * 50)

if __name__ == "__main__":
    run_health_check()
