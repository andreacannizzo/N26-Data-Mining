#!/usr/bin/env python3
"""
N26 Data Mining - Advanced Analytics Dashboard GUI
Dashboard avanzato con KPI, goal tracking e benchmark
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

# Import del modulo analytics
try:
    from advanced_analytics import N26AdvancedAnalytics
except ImportError:
    print("⚠️ Modulo advanced_analytics non trovato")

class AnalyticsCanvas(FigureCanvas):
    """Canvas personalizzato per grafici analytics"""
    
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#2b2b2b')
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Styling matplotlib per tema scuro
        plt.style.use('dark_background')
        self.fig.patch.set_facecolor('#2b2b2b')

class GoalProgressWidget(QWidget):
    """Widget per visualizzare progress degli obiettivi"""
    
    def __init__(self, goal_name, target, actual, unit="€"):
        super().__init__()
        self.goal_name = goal_name
        self.target = target
        self.actual = actual
        self.unit = unit
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Nome goal
        name_label = QLabel(self.goal_name.replace('_', ' ').title())
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #34a853;")
        layout.addWidget(name_label)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_pct = min(100, (self.actual / self.target * 100) if self.target > 0 else 0)
        progress_bar.setValue(int(progress_pct))
        
        # Colore barra basato su progresso
        if progress_pct >= 100:
            color = "#34a853"  # Verde
        elif progress_pct >= 75:
            color = "#fbbc04"  # Giallo
        else:
            color = "#ea4335"  # Rosso
        
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #555;
                border-radius: 8px;
                text-align: center;
                background-color: #333;
                color: white;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(progress_bar)
        
        # Valori
        values_label = QLabel(f"{self.actual:.1f}{self.unit} / {self.target:.1f}{self.unit}")
        values_label.setStyleSheet("color: #ccc; font-size: 12px;")
        layout.addWidget(values_label)
        
        self.setLayout(layout)

class KPICard(QWidget):
    """Card per visualizzare singolo KPI"""
    
    def __init__(self, title, value, unit="", description="", trend=None):
        super().__init__()
        self.title = title
        self.value = value
        self.unit = unit
        self.description = description
        self.trend = trend
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            QWidget {
                background-color: #3c3c3c;
                border-radius: 10px;
                border: 1px solid #555;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Titolo
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: #34a853; font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Valore principale
        value_layout = QHBoxLayout()
        value_label = QLabel(f"{self.value:.1f}")
        value_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        value_layout.addWidget(value_label)
        
        if self.unit:
            unit_label = QLabel(self.unit)
            unit_label.setStyleSheet("color: #ccc; font-size: 14px;")
            value_layout.addWidget(unit_label)
        
        # Trend indicator
        if self.trend is not None:
            if self.trend > 0:
                trend_label = QLabel("↗")
                trend_label.setStyleSheet("color: #34a853; font-size: 16px;")
            elif self.trend < 0:
                trend_label = QLabel("↘")
                trend_label.setStyleSheet("color: #ea4335; font-size: 16px;")
            else:
                trend_label = QLabel("→")
                trend_label.setStyleSheet("color: #fbbc04; font-size: 16px;")
            value_layout.addWidget(trend_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)
        
        # Descrizione
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setStyleSheet("color: #999; font-size: 10px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        layout.addStretch()
        self.setLayout(layout)

class AdvancedAnalyticsDashboard(QMainWindow):
    """Dashboard principale per analytics avanzate"""
    
    def __init__(self, csv_path="N26_Data.csv"):
        super().__init__()
        self.csv_path = csv_path
        self.analytics = None
        self.report_data = {}
        self.init_ui()
        self.load_analytics()
    
    def init_ui(self):
        self.setWindowTitle("N26 Advanced Analytics Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        
        # Styling generale
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QPushButton {
                background-color: #34a853;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d8f47;
            }
            QLabel {
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #3c3c3c;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #34a853;
            }
        """)
        
        # Widget centrale con scroll
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Header
        header_layout = self.create_header()
        scroll_layout.addLayout(header_layout)
        
        # Financial Score Section
        score_section = self.create_score_section()
        scroll_layout.addWidget(score_section)
        
        # KPI Cards Grid
        kpi_section = self.create_kpi_section()
        scroll_layout.addWidget(kpi_section)
        
        # Goals Progress Section
        goals_section = self.create_goals_section()
        scroll_layout.addWidget(goals_section)
        
        # Benchmarks Section
        benchmarks_section = self.create_benchmarks_section()
        scroll_layout.addWidget(benchmarks_section)
        
        # Charts Section
        charts_section = self.create_charts_section()
        scroll_layout.addWidget(charts_section)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)
        
        # Status bar
        self.statusBar().showMessage("Ready - Carica dati per vedere analytics")
    
    def create_header(self):
        """Crea header con titolo e controlli"""
        layout = QHBoxLayout()
        
        # Titolo
        title = QLabel("📊 N26 Advanced Analytics Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #34a853; padding: 20px;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Pulsanti controllo
        refresh_btn = QPushButton("🔄 Aggiorna Dati")
        refresh_btn.clicked.connect(self.load_analytics)
        layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("💾 Esporta Report")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        
        goals_btn = QPushButton("🎯 Gestisci Obiettivi")
        goals_btn.clicked.connect(self.open_goals_dialog)
        layout.addWidget(goals_btn)
        
        return layout
    
    def create_score_section(self):
        """Crea sezione punteggio finanziario"""
        group = QGroupBox("🏆 Punteggio Finanziario")
        layout = QHBoxLayout()
        
        # Score circle (simulato con label)
        self.score_label = QLabel("--")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #34a853;
                border: 4px solid #34a853;
                border-radius: 60px;
                padding: 20px;
                min-width: 120px;
                min-height: 120px;
                background-color: #2b2b2b;
            }
        """)
        layout.addWidget(self.score_label)
        
        # Dettagli score
        details_layout = QVBoxLayout()
        self.score_level = QLabel("Livello: --")
        self.score_level.setStyleSheet("font-size: 18px; font-weight: bold; color: #34a853;")
        details_layout.addWidget(self.score_level)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setMaximumHeight(120)
        self.recommendations_text.setStyleSheet("""
            QTextEdit {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px;
                color: #ccc;
            }
        """)
        details_layout.addWidget(self.recommendations_text)
        
        layout.addLayout(details_layout)
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_kpi_section(self):
        """Crea sezione KPI cards"""
        group = QGroupBox("📈 Key Performance Indicators")
        layout = QGridLayout()
        
        # Placeholder per KPI cards
        self.kpi_cards = {}
        kpi_names = [
            ("Tasso Risparmio", "savings_rate", "%"),
            ("Spesa Mensile", "burn_rate", "€"),
            ("Saldo Netto", "saldo_netto", "€"),
            ("Volatilità", "volatilita_spese", "%"),
            ("Trend Spese", "trend_spese", "%"),
            ("Runway Mesi", "runway_months", "mesi")
        ]
        
        for i, (title, key, unit) in enumerate(kpi_names):
            card = KPICard(title, 0, unit, "Caricamento...")
            self.kpi_cards[key] = card
            layout.addWidget(card, i // 3, i % 3)
        
        group.setLayout(layout)
        return group
    
    def create_goals_section(self):
        """Crea sezione progress obiettivi"""
        group = QGroupBox("🎯 Progresso Obiettivi")
        self.goals_layout = QHBoxLayout()
        
        # Messaggio placeholder
        placeholder = QLabel("Carica dati per visualizzare progresso obiettivi")
        placeholder.setStyleSheet("color: #999; font-style: italic; padding: 20px;")
        self.goals_layout.addWidget(placeholder)
        
        group.setLayout(self.goals_layout)
        return group
    
    def create_benchmarks_section(self):
        """Crea sezione confronto benchmark"""
        group = QGroupBox("📊 Confronto con Benchmark Nazionali")
        layout = QVBoxLayout()
        
        self.benchmarks_table = QTableWidget()
        self.benchmarks_table.setColumnCount(5)
        self.benchmarks_table.setHorizontalHeaderLabels([
            "Metrica", "Tuo Valore", "Benchmark", "Differenza", "Status"
        ])
        self.benchmarks_table.setStyleSheet("""
            QTableWidget {
                background-color: #333;
                gridline-color: #555;
                color: white;
            }
            QHeaderView::section {
                background-color: #34a853;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(self.benchmarks_table)
        
        group.setLayout(layout)
        return group
    
    def create_charts_section(self):
        """Crea sezione grafici"""
        group = QGroupBox("📈 Grafici Analytics")
        layout = QHBoxLayout()
        
        # Canvas per grafici
        self.spending_chart = AnalyticsCanvas(self, width=6, height=4)
        layout.addWidget(self.spending_chart)
        
        self.trend_chart = AnalyticsCanvas(self, width=6, height=4)
        layout.addWidget(self.trend_chart)
        
        group.setLayout(layout)
        return group
    
    def load_analytics(self):
        """Carica dati analytics"""
        try:
            if not os.path.exists(self.csv_path):
                self.statusBar().showMessage(f"File {self.csv_path} non trovato")
                return
            
            self.analytics = N26AdvancedAnalytics(self.csv_path)
            self.report_data = self.analytics.generate_comprehensive_report()
            
            self.update_ui_with_data()
            self.statusBar().showMessage("Dati caricati con successo")
            
        except Exception as e:
            self.statusBar().showMessage(f"Errore caricamento: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile caricare analytics: {e}")
    
    def update_ui_with_data(self):
        """Aggiorna UI con i dati caricati"""
        if not self.report_data:
            return
        
        # Aggiorna score
        score_data = self.report_data.get('financial_score', {})
        score = score_data.get('total_score', 0)
        level = score_data.get('level', 'N/A')
        emoji = score_data.get('emoji', '')
        
        self.score_label.setText(f"{score:.0f}")
        self.score_level.setText(f"{emoji} {level}")
        
        # Aggiorna raccomandazioni
        recommendations = score_data.get('recommendations', [])
        self.recommendations_text.setText('\n'.join(f"• {rec}" for rec in recommendations))
        
        # Aggiorna KPI cards
        kpis = self.report_data.get('kpis', {})
        for key, card in self.kpi_cards.items():
            if key in kpis:
                value = kpis[key]
                # Aggiorna valore della card (questo richiederebbe modifica della classe KPICard)
                # Per ora aggiorniamo il tooltip
                card.setToolTip(f"{key}: {value}")
        
        # Aggiorna goals progress
        self.update_goals_progress()
        
        # Aggiorna benchmarks table
        self.update_benchmarks_table()
        
        # Aggiorna grafici
        self.update_charts()
    
    def update_goals_progress(self):
        """Aggiorna sezione progress obiettivi"""
        # Clear existing widgets
        for i in reversed(range(self.goals_layout.count())):
            self.goals_layout.itemAt(i).widget().setParent(None)
        
        goal_progress = self.report_data.get('goal_progress', {})
        
        if not goal_progress:
            placeholder = QLabel("Nessun obiettivo configurato")
            placeholder.setStyleSheet("color: #999; font-style: italic; padding: 20px;")
            self.goals_layout.addWidget(placeholder)
            return
        
        for goal_key, progress_data in goal_progress.items():
            if isinstance(progress_data, dict) and 'target' in progress_data:
                goal_widget = GoalProgressWidget(
                    goal_key,
                    progress_data['target'],
                    progress_data['actual']
                )
                self.goals_layout.addWidget(goal_widget)
    
    def update_benchmarks_table(self):
        """Aggiorna tabella benchmarks"""
        benchmarks = self.report_data.get('benchmarks', {})
        
        self.benchmarks_table.setRowCount(len(benchmarks))
        
        for row, (metric, data) in enumerate(benchmarks.items()):
            self.benchmarks_table.setItem(row, 0, QTableWidgetItem(metric.replace('_', ' ').title()))
            self.benchmarks_table.setItem(row, 1, QTableWidgetItem(f"{data['user_value']:.1f}"))
            self.benchmarks_table.setItem(row, 2, QTableWidgetItem(f"{data['benchmark']:.1f}"))
            self.benchmarks_table.setItem(row, 3, QTableWidgetItem(f"{data['difference']:.1f}"))
            
            # Status con colore
            status_item = QTableWidgetItem(data['status'].title())
            if data['status'] == 'above':
                status_item.setBackground(QColor('#ea4335'))
            elif data['status'] == 'below':
                status_item.setBackground(QColor('#34a853'))
            else:
                status_item.setBackground(QColor('#fbbc04'))
            
            self.benchmarks_table.setItem(row, 4, status_item)
    
    def update_charts(self):
        """Aggiorna grafici"""
        # Clear previous plots
        self.spending_chart.fig.clear()
        self.trend_chart.fig.clear()
        
        # Esempio grafico spending by category (richiede dati reali)
        ax1 = self.spending_chart.fig.add_subplot(111)
        ax1.set_title("Distribuzione Spese per Categoria", color='white')
        ax1.pie([30, 25, 20, 15, 10], labels=['Casa', 'Cibo', 'Trasporti', 'Svago', 'Altro'],
                autopct='%1.1f%%', startangle=90)
        
        # Esempio trend chart
        ax2 = self.trend_chart.fig.add_subplot(111)
        ax2.set_title("Trend Spese Mensili", color='white')
        months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu']
        spending = [1200, 1350, 1180, 1420, 1300, 1250]
        ax2.plot(months, spending, marker='o', color='#34a853', linewidth=2)
        ax2.set_ylabel('Spesa (€)', color='white')
        ax2.tick_params(colors='white')
        
        self.spending_chart.draw()
        self.trend_chart.draw()
    
    def open_goals_dialog(self):
        """Apre dialog per gestire obiettivi"""
        dialog = GoalsManagementDialog(self.analytics)
        if dialog.exec_() == QDialog.Accepted:
            self.load_analytics()  # Ricarica dopo modifica goals
    
    def export_report(self):
        """Esporta report analytics"""
        if not self.analytics:
            QMessageBox.warning(self, "Attenzione", "Carica prima i dati analytics")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Esporta Report Analytics",
            f"n26_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;CSV Files (*.csv);;Text Files (*.txt)"
        )
        
        if file_path:
            try:
                format_type = file_path.split('.')[-1]
                exported_file = self.analytics.export_report(format_type, file_path.rsplit('.', 1)[0])
                QMessageBox.information(self, "Successo", f"Report esportato: {exported_file}")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore esportazione: {e}")

class GoalsManagementDialog(QDialog):
    """Dialog per gestire obiettivi finanziari"""
    
    def __init__(self, analytics):
        super().__init__()
        self.analytics = analytics
        self.init_ui()
        self.load_current_goals()
    
    def init_ui(self):
        self.setWindowTitle("Gestione Obiettivi Finanziari")
        self.setModal(True)
        self.setGeometry(200, 200, 600, 500)
        
        layout = QVBoxLayout()
        
        # Titolo
        title = QLabel("🎯 Configura i tuoi Obiettivi Finanziari")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #34a853; padding: 10px;")
        layout.addWidget(title)
        
        # Form goals
        form_layout = QFormLayout()
        
        self.goals_inputs = {}
        goals_config = [
            ("savings_monthly", "Risparmio Mensile (€)", 300),
            ("emergency_fund", "Fondo Emergenza (€)", 5000),
            ("debt_reduction", "Riduzione Debiti Mensile (€)", 200),
            ("investment_monthly", "Investimenti Mensili (€)", 150),
            ("vacation_fund", "Fondo Vacanze (€)", 2000),
            ("max_dining_out", "Limite Ristoranti Mensile (€)", 200),
            ("max_shopping", "Limite Shopping Mensile (€)", 300)
        ]
        
        for key, label, default in goals_config:
            input_field = QDoubleSpinBox()
            input_field.setMaximum(999999)
            input_field.setValue(default)
            input_field.setStyleSheet("""
                QDoubleSpinBox {
                    background-color: #333;
                    border: 1px solid #555;
                    border-radius: 4px;
                    padding: 5px;
                    color: white;
                }
            """)
            
            form_layout.addRow(label, input_field)
            self.goals_inputs[key] = input_field
        
        layout.addLayout(form_layout)
        
        # Pulsanti
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Salva Obiettivi")
        save_btn.clicked.connect(self.save_goals)
        buttons_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset Default")
        reset_btn.clicked.connect(self.reset_to_defaults)
        buttons_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("❌ Annulla")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_current_goals(self):
        """Carica obiettivi attuali"""
        if self.analytics and hasattr(self.analytics, 'goals'):
            for key, input_field in self.goals_inputs.items():
                if key in self.analytics.goals:
                    input_field.setValue(self.analytics.goals[key])
    
    def save_goals(self):
        """Salva obiettivi modificati"""
        new_goals = {}
        for key, input_field in self.goals_inputs.items():
            new_goals[key] = input_field.value()
        
        if self.analytics:
            self.analytics.update_goals(new_goals)
            QMessageBox.information(self, "Successo", "Obiettivi salvati con successo!")
            self.accept()
    
    def reset_to_defaults(self):
        """Reset a valori default"""
        defaults = {
            "savings_monthly": 300,
            "emergency_fund": 5000,
            "debt_reduction": 200,
            "investment_monthly": 150,
            "vacation_fund": 2000,
            "max_dining_out": 200,
            "max_shopping": 300
        }
        
        for key, value in defaults.items():
            if key in self.goals_inputs:
                self.goals_inputs[key].setValue(value)

def main():
    """Funzione main per testing"""
    app = QApplication(sys.argv)
    
    # Applica tema scuro globale
    app.setStyle('Fusion')
    palette = app.palette()
    palette.setColor(palette.Window, QColor(43, 43, 43))
    palette.setColor(palette.WindowText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Carica dashboard
    dashboard = AdvancedAnalyticsDashboard()
    dashboard.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
