#!/bin/bash
# Script di avvio per N26 Data Mining GUI

echo "🚀 Avvio N26 Data Mining GUI..."

# Controllo se esiste inputs.py
if [ ! -f "inputs.py" ]; then
    echo "⚠️  File inputs.py non trovato!"
    echo "💡 Esegui prima: ./setup.sh"
    exit 1
fi

# Controllo se esiste l'ambiente virtuale
if [ ! -d "venv" ]; then
    echo "📦 Creazione ambiente virtuale..."
    python3 -m venv venv
fi

# Attivazione ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

# Installazione dipendenze se necessario
echo "📋 Verifica dipendenze..."
pip install -r requirements.txt > /dev/null 2>&1

# Avvio GUI
echo "🖥️  Avvio interfaccia grafica..."
python gui.py
