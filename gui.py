import sys
sys.excepthook = lambda t, v, tb: print(f"EXCEPTION: {t.__name__}: {v}")
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QTextEdit, QHBoxLayout, QLineEdit, QDateEdit, QComboBox, QCheckBox, QDialog, QFormLayout, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QFrame
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import tempfile
import shutil
import os
import smtplib
from email.message import EmailMessage
import schedule
import threading
import time as pytime

try:
    import openpyxl
except ImportError:
    openpyxl = None
try:
    from fpdf2 import FPDF
except ImportError:
    FPDF = None

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
        self.setGeometry(100, 100, 900, 650)
        self.setWindowIcon(QIcon(':/icons/n26.png') if hasattr(QIcon, 'fromTheme') else QIcon())
        self.setStyleSheet(self.get_stylesheet())
        self.csv_path = os.getenv('CSV_TARGET_NAME', 'N26_History_With_Tags.csv')
        self.log_path = 'n26_mining.log'
        self.init_ui()
        self.mining_thread = None

    def get_stylesheet(self):
        # Palette N26: verde #34a853, nero #222, bianco #fff, grigio #444
        return """
        QWidget {
            background-color: #222;
            color: #fff;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 15px;
        }
        QLabel#HeaderLabel {
            font-size: 32px;
            font-weight: bold;
            color: #34a853;
            letter-spacing: 2px;
        }
        QLabel#DashboardLabel {
            font-size: 18px;
            color: #fff;
            background: #333;
            border-radius: 10px;
            padding: 10px 20px;
        }
        QPushButton {
            background-color: #34a853;
            color: #fff;
            border: none;
            border-radius: 18px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: 600;
            margin: 4px;
        }
        QPushButton:hover {
            background-color: #46bdc6;
            color: #222;
        }
        QLineEdit, QDateEdit, QComboBox {
            background: #444;
            color: #fff;
            border-radius: 10px;
            padding: 6px 12px;
            border: 1px solid #34a853;
        }
        QTextEdit {
            background: #181818;
            color: #fff;
            border-radius: 10px;
            font-size: 14px;
        }
        QFrame {
            background: #333;
            border-radius: 12px;
        }
        QScrollBar:vertical {
            background: #222;
            width: 12px;
            margin: 16px 0 16px 0;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: #34a853;
            min-height: 20px;
            border-radius: 6px;
        }
        """

    def init_ui(self):
        main_layout = QVBoxLayout()
        # Header con logo e titolo
        header = QHBoxLayout()
        logo = QLabel()
        pix = QPixmap(64, 64)
        pix.fill(QColor('#34a853'))
        logo.setPixmap(pix)
        header.addWidget(logo)
        title = QLabel('N26 Data Mining')
        title.setObjectName('HeaderLabel')
        header.addWidget(title)
        header.addStretch()
        main_layout.addLayout(header)
        # Separatore
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet('background:#34a853; min-height:2px;')
        main_layout.addWidget(sep)
        # Dashboard
        self.dashboard_label = QLabel('Saldo: -- | Spese medie: -- | Transazioni: -- | Top categoria: -- | Top beneficiario: --')
        self.dashboard_label.setObjectName('DashboardLabel')
        self.dashboard_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.dashboard_label)

        # Status label per messaggi
        self.status_label = QLabel('Pronto')
        self.status_label.setStyleSheet('color: #34a853; font-size: 14px; padding: 5px;')
        main_layout.addWidget(self.status_label)

        # Selettore tipo grafico
        self.graph_selector = QComboBox()
        self.graph_selector.addItems([
            'Spese per categoria',
            'Spese per mese',
            'Transazioni per beneficiario'
        ])
        main_layout.addWidget(self.graph_selector)
        self.btn_show_graph = QPushButton('Mostra grafico')
        self.btn_show_graph.clicked.connect(self.show_selected_graph)
        main_layout.addWidget(self.btn_show_graph)

        # Filtri
        filter_layout = QHBoxLayout()
        self.input_select = QPushButton('Scegli file CSV input')
        self.input_select.clicked.connect(self.select_input_csv)
        filter_layout.addWidget(self.input_select)
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
        main_layout.addLayout(filter_layout)

        # Pulsanti esportazione e storico report
        export_layout = QHBoxLayout()
        self.btn_export_excel = QPushButton('Esporta in Excel')
        self.btn_export_excel.clicked.connect(self.export_excel)
        export_layout.addWidget(self.btn_export_excel)
        self.btn_export_json = QPushButton('Esporta in JSON')
        self.btn_export_json.clicked.connect(self.export_json)
        export_layout.addWidget(self.btn_export_json)
        self.btn_export_pdf = QPushButton('Esporta in PDF')
        self.btn_export_pdf.clicked.connect(self.export_pdf)
        export_layout.addWidget(self.btn_export_pdf)
        self.btn_report_history = QPushButton('Storico Report')
        self.btn_report_history.clicked.connect(self.show_report_history)
        export_layout.addWidget(self.btn_report_history)
        main_layout.addLayout(export_layout)

        # Pulsante principale per avviare il mining
        self.btn_start_mining = QPushButton('🚀 Avvia Mining N26')
        self.btn_start_mining.setStyleSheet("""
            QPushButton {
                background-color: #34a853;
                color: #fff;
                border: none;
                border-radius: 20px;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #46bdc6;
                color: #222;
            }
        """)
        self.btn_start_mining.clicked.connect(self.run_mining)
        main_layout.addWidget(self.btn_start_mining)

        # Pulsante report
        self.btn_report = QPushButton('Genera Report')
        self.btn_report.clicked.connect(self.show_report)
        main_layout.addWidget(self.btn_report)

        # Advanced Analytics Dashboard - NUOVO!
        self.btn_advanced_analytics = QPushButton('📊 Advanced Analytics Dashboard')
        self.btn_advanced_analytics.setStyleSheet("""
            QPushButton {
                background-color: #4285f4;
                color: #fff;
                border: none;
                border-radius: 15px;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
        """)
        self.btn_advanced_analytics.clicked.connect(self.open_advanced_analytics)
        main_layout.addWidget(self.btn_advanced_analytics)

        # Impostazioni avanzate
        self.btn_settings = QPushButton('Impostazioni avanzate')
        self.btn_settings.clicked.connect(self.show_settings)
        main_layout.addWidget(self.btn_settings)

        # Pulsanti aggiuntivi
        extra_layout = QHBoxLayout()
        self.btn_export_graph = QPushButton('Esporta grafico')
        self.btn_export_graph.clicked.connect(self.export_graph)
        extra_layout.addWidget(self.btn_export_graph)
        self.btn_print = QPushButton('Stampa report/grafico')
        self.btn_print.clicked.connect(self.print_report)
        extra_layout.addWidget(self.btn_print)
        self.btn_send_email = QPushButton('Invia report via Email')
        self.btn_send_email.clicked.connect(self.send_email_report)
        extra_layout.addWidget(self.btn_send_email)
        self.btn_send_telegram = QPushButton('Invia report via Telegram')
        self.btn_send_telegram.clicked.connect(self.send_telegram_report)
        extra_layout.addWidget(self.btn_send_telegram)
        self.btn_predict = QPushButton('Analisi predittiva')
        self.btn_predict.clicked.connect(self.show_prediction)
        extra_layout.addWidget(self.btn_predict)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Ricerca full-text...')
        self.search_box.textChanged.connect(self.full_text_search)
        extra_layout.addWidget(self.search_box)
        main_layout.addLayout(extra_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        self.setLayout(main_layout)
        self.schedule_export()

    def select_input_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Scegli file CSV input', self.csv_path, 'CSV Files (*.csv)')
        if path:
            self.csv_path = path
            self.status_label.setText(f'File CSV di input selezionato: {self.csv_path}')
            self.update_dashboard()

    def update_dashboard(self):
        if not os.path.exists(self.csv_path):
            self.dashboard_label.setText('Saldo: -- | Spese medie: -- | Transazioni: -- | Top categoria: -- | Top beneficiario: --')
            return
        try:
            df = pd.read_csv(self.csv_path, na_filter=False)
            if df.empty:
                self.dashboard_label.setText('Saldo: -- | Spese medie: -- | Transazioni: 0 | Top categoria: -- | Top beneficiario: --')
                return
            saldo = df['Importo'].astype(float).sum()
            spese_medie = df['Importo'].astype(float).mean()
            transazioni = len(df)
            top_cat = df['Categoria'].mode()[0] if 'Categoria' in df and not df['Categoria'].isnull().all() else '--'
            top_ben = df['Beneficiario'].mode()[0] if 'Beneficiario' in df and not df['Beneficiario'].isnull().all() else '--'
            self.dashboard_label.setText(f'Saldo: {saldo:.2f} | Spese medie: {spese_medie:.2f} | Transazioni: {transazioni} | Top categoria: {top_cat} | Top beneficiario: {top_ben}')
        except Exception:
            self.dashboard_label.setText('Saldo: -- | Spese medie: -- | Transazioni: -- | Top categoria: -- | Top beneficiario: --')

    def export_excel(self):
        if openpyxl is None:
            QMessageBox.warning(self, 'Dipendenza mancante', 'Installa openpyxl per esportare in Excel.')
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Salva come Excel', 'report.xlsx', 'Excel Files (*.xlsx)')
        if path:
            try:
                df = self.get_filtered_df()
                df.to_excel(path, index=False)
                QMessageBox.information(self, 'Esportazione', f'File Excel salvato: {path}')
            except Exception as e:
                QMessageBox.critical(self, 'Errore', str(e))

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Salva come JSON', 'report.json', 'JSON Files (*.json)')
        if path:
            try:
                df = self.get_filtered_df()
                df.to_json(path, orient='records', force_ascii=False)
                QMessageBox.information(self, 'Esportazione', f'File JSON salvato: {path}')
            except Exception as e:
                QMessageBox.critical(self, 'Errore', str(e))

    def export_pdf(self):
        if FPDF is None:
            QMessageBox.warning(self, 'Dipendenza mancante', 'Installa fpdf per esportare in PDF.')
            return
        path, _ = QFileDialog.getSaveFileName(self, 'Salva come PDF', 'report.pdf', 'PDF Files (*.pdf)')
        if path:
            try:
                df = self.get_filtered_df()
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, 'Report Transazioni N26', ln=True, align='C')
                pdf.set_font('Arial', '', 10)
                for i, row in df.iterrows():
                    pdf.cell(0, 8, str(row.to_dict()), ln=True)
                pdf.output(path)
                QMessageBox.information(self, 'Esportazione', f'File PDF salvato: {path}')
            except Exception as e:
                QMessageBox.critical(self, 'Errore', str(e))

    def show_report_history(self):
        # Mostra i report generati (salvati in una cartella temporanea)
        history_dir = os.path.join(tempfile.gettempdir(), 'n26_report_history')
        if not os.path.exists(history_dir):
            QMessageBox.information(self, 'Storico', 'Nessun report precedente trovato.')
            return
        files = os.listdir(history_dir)
        if not files:
            QMessageBox.information(self, 'Storico', 'Nessun report precedente trovato.')
            return
        msg = 'Report generati:\n' + '\n'.join(files)
        QMessageBox.information(self, 'Storico Report', msg)

    def show_settings(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Impostazioni avanzate')
        form = QFormLayout(dlg)
        self.timeout_input = QLineEdit()
        self.timeout_input.setText(os.getenv('N26_TIMEOUT', '10'))
        form.addRow('Timeout (s):', self.timeout_input)
        self.lang_input = QLineEdit()
        self.lang_input.setText(os.getenv('N26_LANG', 'it_IT'))
        form.addRow('Lingua:', self.lang_input)
        self.datefmt_input = QLineEdit()
        self.datefmt_input.setText(os.getenv('N26_DATEFMT', '%Y-%m-%d'))
        form.addRow('Formato data:', self.datefmt_input)
        btn_save = QPushButton('Salva')
        btn_save.clicked.connect(lambda: self.save_settings(dlg))
        form.addRow(btn_save)
        dlg.setLayout(form)
        dlg.exec_()

    def save_settings(self, dlg):
        os.environ['N26_TIMEOUT'] = self.timeout_input.text()
        os.environ['N26_LANG'] = self.lang_input.text()
        os.environ['N26_DATEFMT'] = self.datefmt_input.text()
        QMessageBox.information(self, 'Impostazioni', 'Impostazioni salvate (valide solo per questa sessione).')
        dlg.accept()

    def get_filtered_df(self):
        if not os.path.exists(self.csv_path):
            raise Exception('File CSV non trovato!')
        df = pd.read_csv(self.csv_path, na_filter=False)
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()
        df = df[(df['Data'] >= pd.Timestamp(date_from)) & (df['Data'] <= pd.Timestamp(date_to))]
        if self.beneficiary_filter.text():
            df = df[df['Beneficiario'].str.contains(self.beneficiary_filter.text(), case=False, na=False)]
        if self.category_filter.text():
            df = df[df['Categoria'].str.contains(self.category_filter.text(), case=False, na=False)]
        return df

    def show_report(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        try:
            df = self.get_filtered_df()
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
            # Mostra grafico interattivo
            plt.figure(figsize=(8,4))
            by_cat.plot(kind='bar')
            plt.title('Spese per categoria')
            plt.ylabel('Importo')
            plt.tight_layout()
            plt.show()
            # Salva report in storico
            history_dir = os.path.join(tempfile.gettempdir(), 'n26_report_history')
            os.makedirs(history_dir, exist_ok=True)
            report_file = os.path.join(history_dir, f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
            with open(report_file, 'w') as f:
                f.write(msg)
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

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
        # Notifica popup
        QMessageBox.information(self, 'Mining', 'Estrazione avviata!')

    def append_log(self, text):
        self.log_text.append(text)

    def mining_finished(self, success, message):
        if success:
            self.status_label.setText('Estrazione completata!')
            QMessageBox.information(self, 'Successo', message)
            self.update_dashboard()
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

    def show_selected_graph(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        try:
            df = self.get_filtered_df()
            if df.empty:
                QMessageBox.information(self, 'Grafico', 'Nessun dato trovato con i filtri selezionati.')
                return
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,4))
            graph_type = self.graph_selector.currentText()
            if graph_type == 'Spese per categoria':
                by_cat = df.groupby('Categoria')['Importo'].astype(float).sum().sort_values(ascending=False)
                by_cat.plot(kind='bar', color='skyblue')
                plt.title('Spese per categoria')
                plt.ylabel('Importo')
            elif graph_type == 'Spese per mese':
                df['Mese'] = df['Data'].dt.to_period('M')
                by_month = df.groupby('Mese')['Importo'].astype(float).sum()
                by_month.plot(kind='line', marker='o', color='green')
                plt.title('Spese per mese')
                plt.ylabel('Importo')
                plt.xlabel('Mese')
            elif graph_type == 'Transazioni per beneficiario':
                by_ben = df['Beneficiario'].value_counts().head(15)
                by_ben.plot(kind='bar', color='orange')
                plt.title('Transazioni per beneficiario (top 15)')
                plt.ylabel('Numero transazioni')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def export_graph(self):
        import matplotlib.pyplot as plt
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        df = self.get_filtered_df()
        if df.empty:
            QMessageBox.information(self, 'Grafico', 'Nessun dato trovato con i filtri selezionati.')
            return
        graph_type = self.graph_selector.currentText()
        plt.figure(figsize=(8,4))
        if graph_type == 'Spese per categoria':
            by_cat = df.groupby('Categoria')['Importo'].astype(float).sum().sort_values(ascending=False)
            by_cat.plot(kind='bar', color='skyblue')
            plt.title('Spese per categoria')
            plt.ylabel('Importo')
        elif graph_type == 'Spese per mese':
            df['Mese'] = df['Data'].dt.to_period('M')
            by_month = df.groupby('Mese')['Importo'].astype(float).sum()
            by_month.plot(kind='line', marker='o', color='green')
            plt.title('Spese per mese')
            plt.ylabel('Importo')
            plt.xlabel('Mese')
        elif graph_type == 'Transazioni per beneficiario':
            by_ben = df['Beneficiario'].value_counts().head(15)
            by_ben.plot(kind='bar', color='orange')
            plt.title('Transazioni per beneficiario (top 15)')
            plt.ylabel('Numero transazioni')
        plt.tight_layout()
        path, _ = QFileDialog.getSaveFileName(self, 'Salva grafico', 'grafico.png', 'PNG Files (*.png);;PDF Files (*.pdf)')
        if path:
            if path.endswith('.pdf'):
                plt.savefig(path, format='pdf')
            else:
                plt.savefig(path, format='png')
            QMessageBox.information(self, 'Esportazione', f'Grafico salvato: {path}')
        plt.close()

    def print_report(self):
        # Stampa il report corrente (testuale o grafico)
        import subprocess
        path = os.path.join(tempfile.gettempdir(), 'n26_print_report.txt')
        try:
            df = self.get_filtered_df()
            msg = df.to_string()
            with open(path, 'w') as f:
                f.write(msg)
            subprocess.run(['lpr', path])
            QMessageBox.information(self, 'Stampa', 'Report inviato alla stampante.')
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def send_email_report(self):
        # Invia il report via email (richiede configurazione SMTP)
        email, ok = QInputDialog.getText(self, 'Invia Email', 'Inserisci indirizzo email destinatario:')
        if not ok or not email:
            return
        try:
            df = self.get_filtered_df()
            msg = EmailMessage()
            msg['Subject'] = 'Report N26'
            msg['From'] = 'your@email.com'
            msg['To'] = email
            msg.set_content(df.to_string())
            with smtplib.SMTP('localhost') as s:
                s.send_message(msg)
            QMessageBox.information(self, 'Email', 'Email inviata! (Verifica configurazione SMTP locale)')
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def send_telegram_report(self):
        # Invia il report via Telegram (richiede bot token e chat_id)
        token, ok1 = QInputDialog.getText(self, 'Telegram', 'Inserisci il token del bot:')
        chat_id, ok2 = QInputDialog.getText(self, 'Telegram', 'Inserisci il chat_id:')
        if not (ok1 and ok2 and token and chat_id):
            return
        try:
            import requests
            df = self.get_filtered_df()
            text = df.to_string()
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = {'chat_id': chat_id, 'text': text}
            requests.post(url, data=data)
            QMessageBox.information(self, 'Telegram', 'Report inviato su Telegram!')
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def show_prediction(self):
        # Analisi predittiva semplice: media mobile delle spese
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, 'Attenzione', f'File {self.csv_path} non trovato!')
            return
        try:
            df = self.get_filtered_df()
            if df.empty:
                QMessageBox.information(self, 'Predizione', 'Nessun dato trovato con i filtri selezionati.')
                return
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df = df.sort_values('Data')
            df['Importo'] = df['Importo'].astype(float)
            df['media_mobile'] = df['Importo'].rolling(window=3, min_periods=1).mean()
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,4))
            plt.plot(df['Data'], df['Importo'], label='Importo')
            plt.plot(df['Data'], df['media_mobile'], label='Media mobile', linestyle='--')
            plt.title('Previsione spese (media mobile)')
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def open_advanced_analytics(self):
        """Apre dashboard Advanced Analytics"""
        try:
            # Import del modulo analytics dashboard
            from analytics_dashboard import AdvancedAnalyticsDashboard
            
            # Verifica se esiste file CSV
            if not os.path.exists(self.csv_path):
                reply = QMessageBox.question(
                    self, 
                    'File CSV mancante', 
                    f'Il file {self.csv_path} non esiste.\n\nVuoi prima eseguire il mining N26 per generare i dati?',
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.run_mining()
                    return
                else:
                    return
            
            # Apri dashboard avanzato
            self.analytics_dashboard = AdvancedAnalyticsDashboard(self.csv_path)
            self.analytics_dashboard.show()
            
            self.status_label.setText('🚀 Advanced Analytics Dashboard aperto!')
            
        except ImportError:
            QMessageBox.critical(
                self, 
                'Modulo non trovato', 
                'Modulo Advanced Analytics non trovato.\nAssicurati che analytics_dashboard.py sia presente nella directory.'
            )
        except Exception as e:
            QMessageBox.critical(self, 'Errore', f'Impossibile aprire Advanced Analytics: {e}')

    def full_text_search(self):
        # Ricerca full-text su tutte le colonne
        text = self.search_box.text().lower()
        if not text:
            return
        try:
            df = pd.read_csv(self.csv_path, na_filter=False)
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(text).any(), axis=1)
            filtered = df[mask]
            msg = filtered.to_string() if not filtered.empty else 'Nessun risultato.'
            QMessageBox.information(self, 'Risultati ricerca', msg)
        except Exception as e:
            QMessageBox.critical(self, 'Errore', str(e))

    def schedule_export(self):
        # Esportazione automatica programmata ogni giorno alle 23:59
        def job():
            try:
                df = self.get_filtered_df()
                now = datetime.now().strftime('%Y%m%d_%H%M')
                path = os.path.join(tempfile.gettempdir(), f'n26_export_{now}.csv')
                df.to_csv(path, index=False)
            except Exception:
                pass
        schedule.every().day.at('23:59').do(job)
        def run_schedule():
            while True:
                schedule.run_pending()
                pytime.sleep(60)
        t = threading.Thread(target=run_schedule, daemon=True)
        t.start()
