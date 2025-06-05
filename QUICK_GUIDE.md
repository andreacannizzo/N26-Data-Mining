# 📋 N26 Data Mining - Guida Rapida

## 🚀 Avvio Veloce

### ⚡ Setup Ultra-Rapido (3 comandi)
```bash
# 1. Configurazione iniziale
./setup.sh

# 2. Test sistema (opzionale)
./test_system.sh

# 3. Avvio GUI
./start_gui.sh
```

### 🔧 Primo Utilizzo Dettagliato
1. **Configura il file inputs.py**
   ```bash
   ./setup.sh
   # Poi modifica inputs.py con le tue credenziali N26
   ```

2. **Verifica sistema (opzionale)**
   ```bash
   python health_check.py    # Diagnostica completa
   ./test_system.sh          # Test rapido
   ```

3. **Avvia l'interfaccia grafica**
   ```bash
   ./start_gui.sh
   ```

### Utilizzo della GUI

#### 🏠 **Dashboard**
- Visualizza saldo, spese medie, numero transazioni
- Mostra categoria e beneficiario più frequenti
- Si aggiorna automaticamente quando carichi un CSV

#### 📊 **Advanced Analytics Dashboard** ⭐ NUOVO!
Accedi al dashboard avanzato tramite il pulsante blu "📊 Advanced Analytics Dashboard":

**🏆 Punteggio Finanziario**
- Score 0-100 basato su savings rate, goal achievement, spending control
- Livelli: Eccellente (80+), Buono (65+), Discreto (50+), Da migliorare (35+), Critico (<35)
- Raccomandazioni personalizzate per migliorare

**📈 KPI Finanziari**
- **Savings Rate**: Percentuale di reddito risparmiato
- **Burn Rate**: Spesa media mensile
- **Runway Months**: Mesi di autonomia finanziaria
- **Trend Spese**: Crescita/decrescita spese mensili
- **Volatilità**: Stabilità delle spese

**🎯 Goal Tracking**
- Imposta obiettivi di risparmio, riduzione debiti, limiti spesa
- Progress bar visuale per ogni obiettivo
- Notifiche quando superi i limiti

**📊 Benchmark Nazionali**
- Confronto con medie italiane per categoria di spesa
- Indicatori above/below/aligned rispetto ai benchmark
- Percentuali di differenza dettagliate

**💾 Export Avanzato**
- Report JSON, CSV, TXT con tutti i KPI
- Grafici analytics esportabili
- Storico goals e progress tracking

## ⚙️ **Configurazione**

### File di Configurazione
Modifica `config.ini` per personalizzare:
- Server SMTP per email
- Token Telegram per notifiche
- Formati di export predefiniti
- Livelli di logging

### Variabili d'Ambiente
```bash
export CSV_TARGET_NAME="N26_Data.csv"
export N26_TIMEOUT="30"
export N26_LANG="it_IT"
```

## 🛠️ **Risoluzione Problemi**

### GUI non si avvia
```bash
# Verifica dipendenze
python test_final.py

# Reinstalla ambiente virtuale
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Errori di esportazione
- **Excel**: Installa `openpyxl`
- **PDF**: Installa `fpdf2`
- **Email**: Configura server SMTP
- **Telegram**: Ottieni bot token

### File CSV non trovato
1. Esegui prima il mining: pulsante "🚀 Avvia Mining N26"
2. Oppure carica un CSV esistente: "Scegli file CSV input"

## 📞 **Supporto**

Per problemi o domande:
1. Controlla i log nell'area di testo della GUI
2. Verifica il file `n26_mining.log`
3. Usa il test rapido: `python test_quick.py`

## 🎯 **Tips & Tricks**

- Usa i filtri per analizzare periodi specifici
- Combina ricerca full-text con filtri per analisi dettagliate
- Configura le automazioni per report periodici
- Esporta grafici in PNG per presentazioni
- Stampa report per archivio fisico

### 📊 **Advanced Analytics Tips**
- **Imposta obiettivi realistici**: Inizia con target raggiungibili e aumenta gradualmente
- **Monitora il Financial Score**: Punta a raggiungere almeno 65 punti (livello "Buono")
- **Usa i benchmark**: Se sei sopra la media nazionale in una categoria, considera di ridurre
- **Analizza i trend**: Un trend positivo nelle spese indica aumento dei costi mensili
- **Volatilità bassa è meglio**: Spese stabili indicano migliore controllo finanziario
- **Export regolari**: Salva report mensili per tracking long-term
- **Goal adjustment**: Rivedi gli obiettivi ogni 3 mesi basandoti sui risultati

### 🚀 **Modalità di Avvio**
```bash
# GUI completa (include Advanced Analytics)
./start_gui.sh

# Solo Advanced Analytics Dashboard
./start_analytics.sh

# Test sistema completo  
python test_advanced_analytics.py
```
