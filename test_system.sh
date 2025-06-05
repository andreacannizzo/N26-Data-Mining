#!/bin/bash
# N26 Data Mining - Test Completo di Funzionamento

echo "🧪 N26 Data Mining - Test Completo"
echo "=================================="

# Controllo file essenziali
echo "📋 Controllo file essenziali..."
essential_files=("main.py" "definitions.py" "gui.py" "requirements.txt" "inputs_example.py")
missing_files=()

for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MANCANTE!"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ File mancanti trovati. Setup incompleto."
    exit 1
fi

# Controllo configurazione
echo ""
echo "⚙️ Controllo configurazione..."
if [ -f "inputs.py" ]; then
    echo "  ✅ inputs.py configurato"
else
    echo "  ⚠️  inputs.py non trovato"
    echo "  💡 Esegui: ./setup.sh"
fi

# Controllo ambiente virtuale
echo ""
echo "🐍 Controllo ambiente virtuale..."
if [ -d "venv" ]; then
    echo "  ✅ Ambiente virtuale presente"
    
    # Test import moduli critici
    echo "  🔍 Test import moduli..."
    source venv/bin/activate
    python -c "
import sys
modules = ['PyQt5', 'pandas', 'matplotlib', 'selenium']
failed = []
for module in modules:
    try:
        __import__(module)
        print(f'    ✅ {module}')
    except ImportError:
        print(f'    ❌ {module} - MANCANTE!')
        failed.append(module)

if failed:
    print(f'  ❌ {len(failed)} moduli mancanti')
    sys.exit(1)
else:
    print('  ✅ Tutti i moduli critici sono installati')
"
    module_test_result=$?
else
    echo "  ❌ Ambiente virtuale mancante"
    echo "  💡 Verrà creato al prossimo avvio"
    module_test_result=1
fi

# Test sintassi file Python
echo ""
echo "🔍 Test sintassi Python..."
python_files=("main.py" "definitions.py" "gui.py" "version.py" "health_check.py")
syntax_errors=0

for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        if python -m py_compile "$file" 2>/dev/null; then
            echo "  ✅ $file - sintassi OK"
        else
            echo "  ❌ $file - ERRORI SINTASSI!"
            syntax_errors=$((syntax_errors + 1))
        fi
    fi
done

# Risultato finale
echo ""
echo "📊 RISULTATO TEST:"
echo "=================="

if [ ${#missing_files[@]} -eq 0 ] && [ $module_test_result -eq 0 ] && [ $syntax_errors -eq 0 ]; then
    echo "🎉 TUTTI I TEST SUPERATI!"
    echo "✅ Il sistema è pronto per l'uso"
    echo ""
    echo "🚀 Per iniziare:"
    echo "   ./start_gui.sh"
    echo ""
    echo "📚 Per aiuto:"
    echo "   cat QUICK_GUIDE.md"
    exit 0
else
    echo "⚠️  ALCUNI TEST FALLITI:"
    [ ${#missing_files[@]} -gt 0 ] && echo "   📄 File mancanti: ${#missing_files[@]}"
    [ $module_test_result -ne 0 ] && echo "   🐍 Moduli Python: problemi rilevati"
    [ $syntax_errors -gt 0 ] && echo "   🔍 Errori sintassi: $syntax_errors file"
    echo ""
    echo "🔧 Soluzioni:"
    echo "   ./setup.sh        # Setup configurazione"
    echo "   ./start_gui.sh     # Installa dipendenze"
    echo "   python health_check.py  # Diagnostica dettagliata"
    exit 1
fi
