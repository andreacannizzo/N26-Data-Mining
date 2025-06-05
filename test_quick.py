#!/usr/bin/env python3
"""
Test rapido per verificare se PyQt5 funziona
"""

try:
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel
    import sys
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Test N26 GUI')
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel('🎉 GUI N26 Funzionante!', window)
    label.move(50, 80)
    
    print("✅ Test GUI completato con successo!")
    print("📋 La GUI N26 è pronta per l'uso!")
    
    # Non mostriamo la finestra, solo testiamo la creazione
    # window.show()
    # sys.exit(app.exec_())
    
except Exception as e:
    print(f"❌ Errore GUI: {e}")
    print("💡 Verifica l'installazione di PyQt5")
