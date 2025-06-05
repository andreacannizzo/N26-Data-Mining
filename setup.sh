#!/bin/bash
# N26 Data Mining - Script di Configurazione Iniziale

echo "🚀 N26 Data Mining - Setup Iniziale"
echo "=================================="

# Controllo se inputs.py esiste già
if [ -f "inputs.py" ]; then
    echo "⚠️  File inputs.py già esistente."
    read -p "Vuoi sovrascriverlo? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup annullato."
        exit 1
    fi
fi

# Copia il file di esempio
echo "📋 Copiando inputs_example.py -> inputs.py..."
cp inputs_example.py inputs.py

echo "✅ File inputs.py creato!"
echo ""
echo "📝 PROSSIMI PASSI:"
echo "1. Modifica il file inputs.py con le tue credenziali N26:"
echo "   nano inputs.py"
echo ""
echo "2. Controlla la salute del sistema:"
echo "   python health_check.py"
echo ""
echo "3. Avvia l'interfaccia grafica:"
echo "   ./start_gui.sh"
echo ""
echo "🔒 IMPORTANTE: Non condividere mai il file inputs.py!"
echo "   (È già incluso in .gitignore per sicurezza)"
echo ""
echo "📚 Per maggiori informazioni consulta:"
echo "   - README.md"
echo "   - QUICK_GUIDE.md"
echo ""
echo "🎉 Setup completato! Buon mining! 💰"
