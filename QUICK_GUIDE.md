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

#### 🔍 **Filtri**
- **Data**: Filtra per periodo (da/a)
- **Beneficiario**: Cerca per nome beneficiario
- **Categoria**: Filtra per categoria di spesa

#### 📊 **Grafici**
- **Spese per categoria**: Grafico a barre delle categorie di spesa
- **Spese per mese**: Andamento temporale delle spese
- **Beneficiari**: Top 15 beneficiari per numero transazioni

#### 💾 **Esportazione**
- **Excel**: File .xlsx con tutti i dati filtrati
- **JSON**: Formato JSON per integrazione con altri sistemi
- **PDF**: Report stampabile in PDF
- **PNG**: Esportazione grafici come immagini

#### 🤖 **Automazioni**
- **Email**: Invio report automatico via email
- **Telegram**: Notifiche su Telegram
- **Stampa**: Stampa diretta su stampante locale
- **Esportazione programmata**: Backup automatico alle 23:59

#### 🔮 **Funzionalità Avanzate**
- **Ricerca full-text**: Cerca in tutte le descrizioni
- **Analisi predittiva**: Media mobile delle spese
- **Storico report**: Visualizza report generati in precedenza

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
