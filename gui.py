import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QTextEdit, QHBoxLayout, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class MiningThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, main_py, env):
        super().__init__()
        self.main_py = main_py
        self.env = env

    def run(self):
        try:
            process = subprocess.Popen([sys.executable, self.main_py], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=self.env)
            for line in process.stdout:
                self.log_signal.emit(line)
            process.wait()
            if process.returncode == 0:
                self.finished_signal.emit(True, 'Estrazione completata!')
            else:
                self.finished_signal.emit(False, 'Errore durante l\'estrazione.')
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class N26Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('N26 Data Mining GUI')
        self.setGeometry(100, 100, 600, 400)
        self.csv_path = os.getenv('CSV_TARGET_NAME', 'N26_History_With_Tags.csv')
        self.log_path = 'n26_mining.log'
        self.init_ui()
        self.mining_thread = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel('Pronto per lanciare il mining dei dati N26.')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Filtri
        filter_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat('yyyy-MM-dd')
        self.date_from.setDate(datetime(2020, 1, 1))
        filter_layout.addWidget(QLabel('Da:'))
        filter_layout.addWidget(self.date_from)
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat('yyyy-MM-dd')
        self.date_to.setDate(datetime.now())
        filter_layout.addWidget(QLabel('A:'))
        filter_layout.addWidget(self.date_to)
        self.beneficiary_filter = QLineEdit()
        self.beneficiary_filter.setPlaceholderText('Beneficiario')
        filter_layout.addWidget(self.beneficiary_filter)
        self.category_filter = QLineEdit()
        self.category_filter.setPlaceholderText('Categoria')
        filter_layout.addWidget(self.category_filter)
        layout.addLayout(filter_layout)

        # Pulsante report
        self.btn_report = QPushButton('Genera Report')
        self.btn_report.clicked.connect(self.show_report)
        layout.addWidget(self.btn_report)

        btn_layout = QHBoxLayout()
        self.btn_run = QPushButton('Avvia Mining')
        self.btn_run.clicked.connect(self.run_mining)
        btn_layout.addWidget(self.btn_run)

        self.btn_select_csv = QPushButton('Scegli file CSV output')
        self.btn_select_csv.clicked.connect(self.select_csv)
        btn_layout.addWidget(self.btn_select_csv)

        self.btn_open_csv = QPushButton('Apri CSV risultati')
        self.btn_open_csv.clicked.connect(self.open_csv)
        btn_layout.addWidget(self.btn_open_csv)

        self.btn_open_log = QPushButton('Apri log')
        self.btn_open_log.clicked.connect(self.open_log)
        btn_layout.addWidget(self.btn_open_log)

        layout.addLayout(btn_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def run_mining(self):
        self.status_label.setText('Estrazione in corso...')
        self.log_text.clear()
        self.repaint()
        env = os.environ.copy()
        env['CSV_TARGET_NAME'] = self.csv_path
        self.mining_thread = MiningThread('main.py', env)
        self.mining_thread.log_signal.connect(self.append_log)
        self.mining_thread.finished_signal.connect(self.mining_finished)
        self.mining_thread.start()

    def append_log(self, text):
        self.log_text.append(text)

    def mining_finished(self, success, message):
        if success:
            self.status_label.setText('Estrazione completata!')
            QMessageBox.information(self, 'Successo', message)
        else:
            self.status_label.setText('Errore durante l\'estrazione.')
            QMessageBox.critical(self, 'Errore', message)

    def select_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Scegli file CSV output', self.csv_path, 'CSV Files (*.csv)')
        if path:
            self.csv_path = path
            self.status_label.setText(f'File CSV selezionato: {self.csv_path}')

    def open_csv(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        os.system(f'xdg-open "{self.csv_path}"')

    def open_log(self):
        if not os.path.exists(self.log_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.log_path} non trovato!')
            return
        os.system(f'xdg-open "{self.log_path}"')

    def show_report(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        try:
            df = pd.read_csv(self.csv_path, na_filter=False)
            # Applica filtri
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            date_from = self.date_from.date().toPyDate()
            date_to = self.date_to.date().toPyDate()
            df = df[(df['Data'] >= pd.Timestamp(date_from)) & (df['Data'] <= pd.Timestamp(date_to))]
            if self.beneficiary_filter.text():
                df = df[df['Beneficiario'].str.contains(self.beneficiary_filter.text(), case=False, na=False)]
            if self.category_filter.text():
                df = df[df['Categoria'].str.contains(self.category_filter.text(), case=False, na=False)]
            if df.empty:
                QMessageBox.information(self, 'Report', 'Nessun dato trovato con i filtri selezionati.')
                return
            # Statistiche
            total = df['Importo'].astype(float).sum()
            by_cat = df.groupby('Categoria')['Importo'].astype(float).sum().sort_values(ascending=False)
            msg = f"Totale transazioni filtrate: {len(df)}\nTotale importi: {total:.2f}\n\nSpese per categoria:\n"
            for cat, val in by_cat.items():
                msg += f"{cat}: {val:.2f}\n"
            QMessageBox.information(self, 'Report', msg)
            # Mostra grafico
            plt.figure(figsize=(8,4))
            by_cat.plot(kind='bar')
            plt.title('Spese per categoria')
            plt.ylabel('Importo')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = N26Gui()
    gui.show()
    sys.exit(app.exec_())
