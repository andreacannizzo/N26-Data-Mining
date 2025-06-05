# N26 Data Mining - File di Configurazione
# 
# ISTRUZIONI IMPORTANTI:
# 1. Copia questo file come 'inputs.py': cp inputs_example.py inputs.py
# 2. Modifica i valori sottostanti con le tue credenziali N26
# 3. NON condividere mai il file inputs.py (è in .gitignore per sicurezza)
#
# ATTENZIONE: Mantieni sempre le credenziali al sicuro!

# Le tue credenziali N26
username = "YOUR_USERNAME"  # Il tuo username/email N26
password = "YOUR_PASSWORD"  # La tua password N26

# Configurazioni opzionali (possono essere lasciate così)
timeout_seconds = 30        # Timeout per 2FA
max_retries = 3            # Numero massimo di tentativi
headless_mode = False      # True per esecuzione senza GUI browser

# File di output (personalizzabili)
csv_output_file = "N26_Data.csv"
labels_file = "labels_example.csv"

# Note per l'uso:
# - Assicurati di avere il 2FA attivo su N26
# - Accetta la richiesta 2FA entro il timeout impostato
# - Il browser si aprirà automaticamente per l'autenticazione