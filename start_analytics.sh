#!/bin/bash
# Advanced Analytics Dashboard Launcher
# Script per avviare il dashboard analytics avanzato

echo "🚀 N26 Advanced Analytics Dashboard Launcher"
echo "============================================="

# Controlla se siamo nella directory corretta
if [ ! -f "analytics_dashboard.py" ]; then
    echo "❌ Errore: analytics_dashboard.py non trovato!"
    echo "   Assicurati di essere nella directory N26-Data-Mining"
    exit 1
fi

# Attiva ambiente virtuale se esiste
if [ -d "venv" ]; then
    echo "🔧 Attivazione ambiente virtuale..."
    source venv/bin/activate
else
    echo "⚠️  Ambiente virtuale non trovato - usando Python di sistema"
fi

# Controlla dipendenze critiche
echo "🔍 Controllo dipendenze..."
python3 -c "
import sys
modules = ['PyQt5', 'pandas', 'matplotlib', 'sklearn', 'plotly']
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        missing.append(module)
        print(f'❌ {module} - MANCANTE')

if missing:
    print(f'\\n⚠️  Dipendenze mancanti: {missing}')
    print('   Esegui: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('\\n✅ Tutte le dipendenze sono installate')
"

if [ $? -ne 0 ]; then
    echo ""
    echo "🔧 Installazione dipendenze mancanti..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Errore installazione dipendenze"
        exit 1
    fi
fi

# Controlla file CSV dati
CSV_FILE="N26_Data.csv"
if [ ! -f "$CSV_FILE" ]; then
    echo ""
    echo "⚠️  File CSV dati non trovato: $CSV_FILE"
    echo "   Opzioni:"
    echo "   1. Esegui prima il mining: python main.py"
    echo "   2. Usa la GUI principale: ./start_gui.sh"
    echo "   3. Procedi comunque (dashboard con dati demo)"
    echo ""
    read -p "Vuoi procedere comunque? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operazione annullata"
        exit 1
    fi
fi

# Test rapido moduli analytics
echo "🧪 Test moduli analytics..."
python3 -c "
try:
    from advanced_analytics import N26AdvancedAnalytics
    from analytics_dashboard import AdvancedAnalyticsDashboard
    print('✅ Moduli analytics caricati correttamente')
except Exception as e:
    print(f'❌ Errore caricamento moduli: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Errore nei moduli analytics"
    exit 1
fi

echo ""
echo "🚀 Avvio Advanced Analytics Dashboard..."
echo "   - Dashboard KPI finanziari"
echo "   - Goal tracking avanzato"
echo "   - Benchmark comparativi"
echo "   - Grafici interattivi"
echo ""

# Avvia dashboard
python3 analytics_dashboard.py

echo ""
echo "👋 Dashboard chiuso"
