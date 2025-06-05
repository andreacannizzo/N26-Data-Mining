#!/usr/bin/env python3
"""
Test finale per verificare che tutti i moduli della GUI siano installati correttamente
"""

import sys
import os

def test_imports():
    """Test di importazione di tutti i moduli necessari"""
    modules_to_test = [
        ('PyQt5.QtWidgets', 'QApplication'),
        ('PyQt5.QtCore', 'Qt'),
        ('PyQt5.QtGui', 'QFont'),
        ('pandas', 'DataFrame'),
        ('matplotlib.pyplot', 'figure'),
        ('seaborn', None),
        ('openpyxl', None),
        ('fpdf2', 'FPDF'),
        ('reportlab.pdfgen', 'canvas'),
        ('requests', 'get'),
        ('schedule', None),
        ('selenium', 'webdriver')
    ]
    
    print("🧪 Test di importazione moduli GUI...")
    print("=" * 50)
    
    failed_imports = []
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name] if class_name else [])
            if class_name:
                getattr(module, class_name)
            print(f"✅ {module_name} - OK")
        except ImportError as e:
            print(f"❌ {module_name} - ERRORE: {e}")
            failed_imports.append(module_name)
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name} - ERRORE: {e}")
            failed_imports.append(f"{module_name}.{class_name}")
    
    print("=" * 50)
    
    if failed_imports:
        print(f"❌ {len(failed_imports)} moduli non trovati:")
        for module in failed_imports:
            print(f"   - {module}")
        print("\n💡 Installa i moduli mancanti con:")
        print("   pip install " + " ".join(failed_imports))
        return False
    else:
        print("✅ Tutti i moduli sono installati correttamente!")
        return True

def test_gui_basic():
    """Test basilare della GUI senza aprire finestre"""
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✅ QApplication creata con successo")
        return True
    except Exception as e:
        print(f"❌ Errore creazione QApplication: {e}")
        return False

def main():
    print("🚀 N26 Data Mining - Test Finale GUI")
    print("=" * 50)
    
    # Test importazioni
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    
    # Test GUI basilare
    if imports_ok:
        gui_ok = test_gui_basic()
        
        if gui_ok:
            print("\n🎉 SUCCESSO! La GUI è pronta per l'uso!")
            print("\n📋 Per avviare l'interfaccia grafica:")
            print("   ./start_gui.sh")
            print("   oppure")
            print("   python gui.py")
        else:
            print("\n⚠️  Problemi con l'inizializzazione GUI")
    else:
        print("\n❌ Installa prima tutti i moduli richiesti")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
