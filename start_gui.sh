#!/bin/bash
# Script di avvio per N26 Data Mining GUI

# Controllo se esiste l'ambiente virtuale
if [ ! -d "venv" ]; then
    echo "Creazione ambiente virtuale..."
    python3 -m venv venv
fi

# Attivazione ambiente virtuale
source venv/bin/activate

# Installazione dipendenze se necessario
pip install -r requirements.txt

# Avvio GUI
echo "Avvio interfaccia grafica N26 Data Mining..."
python gui.py
