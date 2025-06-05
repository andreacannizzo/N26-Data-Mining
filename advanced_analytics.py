#!/usr/bin/env python3
"""
N26 Data Mining - Advanced Analytics Dashboard with KPIs
Metriche finanziarie avanzate, goal tracking e benchmark comparativi
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class N26AdvancedAnalytics:
    """Sistema di analytics avanzate con KPI finanziari professionali"""
    
    def __init__(self, csv_path: str, goals_path: str = "financial_goals.json"):
        self.csv_path = csv_path
        self.goals_path = goals_path
        self.df = None
        self.goals = {}
        self.load_data()
        self.load_goals()
        
        # Benchmark nazionali italiani (dati esempio realistici)
        self.national_benchmarks = {
            'savings_rate': 8.2,  # % del reddito risparmiato
            'housing_ratio': 25.0,  # % reddito per casa
            'food_ratio': 15.0,  # % reddito per cibo
            'transport_ratio': 12.0,  # % reddito trasporti
            'entertainment_ratio': 8.0,  # % reddito intrattenimento
            'avg_monthly_spending': 1450.0,  # Spesa media mensile
            'debt_service_ratio': 30.0  # % reddito per debiti
        }
    
    def load_data(self):
        """Carica e preprocessa i dati finanziari"""
        try:
            if os.path.exists(self.csv_path):
                self.df = pd.read_csv(self.csv_path)
                self.df['Data'] = pd.to_datetime(self.df['Data'])
                self.df['Importo'] = pd.to_numeric(self.df['Importo'], errors='coerce')
                self.df = self.df.dropna()
                
                # Separazione entrate e uscite
                self.df['Tipo'] = self.df['Importo'].apply(lambda x: 'Entrata' if x > 0 else 'Uscita')
                self.df['Importo_Assoluto'] = self.df['Importo'].abs()
                
                print(f"✅ Caricati {len(self.df)} records finanziari")
            else:
                print(f"⚠️ File {self.csv_path} non trovato")
        except Exception as e:
            print(f"❌ Errore caricamento dati: {e}")
    
    def load_goals(self):
        """Carica obiettivi finanziari salvati"""
        try:
            if os.path.exists(self.goals_path):
                with open(self.goals_path, 'r') as f:
                    self.goals = json.load(f)
            else:
                self.goals = self.create_default_goals()
                self.save_goals()
        except Exception as e:
            print(f"⚠️ Errore caricamento goals: {e}")
            self.goals = self.create_default_goals()
    
    def save_goals(self):
        """Salva obiettivi finanziari"""
        try:
            with open(self.goals_path, 'w') as f:
                json.dump(self.goals, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Errore salvataggio goals: {e}")
    
    def create_default_goals(self) -> Dict:
        """Crea obiettivi finanziari di default"""
        return {
            'savings_monthly': 300.0,
            'emergency_fund': 5000.0,
            'debt_reduction': 200.0,
            'investment_monthly': 150.0,
            'vacation_fund': 2000.0,
            'max_dining_out': 200.0,
            'max_shopping': 300.0,
            'created_date': datetime.now().isoformat()
        }
    
    def calculate_kpis(self) -> Dict:
        """Calcola KPI finanziari avanzati"""
        if self.df is None or self.df.empty:
            return {}
        
        # Periodo di analisi (ultimo anno)
        end_date = self.df['Data'].max()
        start_date = end_date - timedelta(days=365)
        df_year = self.df[self.df['Data'] >= start_date].copy()
        
        # Separazione entrate/uscite
        income = df_year[df_year['Importo'] > 0]['Importo'].sum()
        expenses = abs(df_year[df_year['Importo'] < 0]['Importo'].sum())
        
        # KPI principali
        kpis = {
            'periodo_analisi': f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}",
            'reddito_totale': round(income, 2),
            'spese_totali': round(expenses, 2),
            'saldo_netto': round(income - expenses, 2),
            'savings_rate': round((income - expenses) / income * 100, 2) if income > 0 else 0,
            'burn_rate': round(expenses / 12, 2),  # Spesa media mensile
            'runway_months': round(income / (expenses / 12), 1) if expenses > 0 else float('inf')
        }
        
        # KPI avanzati per categoria
        category_analysis = self.analyze_spending_by_category(df_year, income)
        kpis.update(category_analysis)
        
        # Trend analysis
        trend_analysis = self.calculate_trends(df_year)
        kpis.update(trend_analysis)
        
        return kpis
    
    def analyze_spending_by_category(self, df: pd.DataFrame, total_income: float) -> Dict:
        """Analizza spese per categoria con ratios"""
        expenses_by_cat = abs(df[df['Importo'] < 0].groupby('Categoria')['Importo'].sum())
        
        category_ratios = {}
        for category, amount in expenses_by_cat.items():
            ratio = (amount / total_income * 100) if total_income > 0 else 0
            category_ratios[f'{category.lower()}_ratio'] = round(ratio, 2)
            category_ratios[f'{category.lower()}_amount'] = round(amount, 2)
        
        return category_ratios
    
    def calculate_trends(self, df: pd.DataFrame) -> Dict:
        """Calcola trend di crescita/decrescita"""
        # Spese mensili
        monthly_expenses = df[df['Importo'] < 0].groupby(
            df['Data'].dt.to_period('M')
        )['Importo'].sum().abs()
        
        if len(monthly_expenses) < 2:
            return {'trend_spese': 0, 'volatilita_spese': 0}
        
        # Calcolo trend (variazione percentuale media)
        pct_changes = monthly_expenses.pct_change().dropna()
        avg_growth = pct_changes.mean() * 100
        volatility = pct_changes.std() * 100
        
        return {
            'trend_spese': round(avg_growth, 2),
            'volatilita_spese': round(volatility, 2),
            'mesi_analizzati': len(monthly_expenses)
        }
    
    def calculate_goal_progress(self) -> Dict:
        """Calcola progresso verso gli obiettivi finanziari"""
        if self.df is None or self.df.empty:
            return {}
        
        # Ultimo mese di dati
        last_month = self.df['Data'].max().replace(day=1)
        month_data = self.df[
            (self.df['Data'] >= last_month) & 
            (self.df['Data'] < last_month + timedelta(days=32))
        ]
        
        progress = {}
        
        # Savings goal
        monthly_savings = month_data[month_data['Importo'] > 0]['Importo'].sum() - \
                         abs(month_data[month_data['Importo'] < 0]['Importo'].sum())
        
        if 'savings_monthly' in self.goals:
            progress['savings_progress'] = {
                'target': self.goals['savings_monthly'],
                'actual': round(monthly_savings, 2),
                'progress_pct': round((monthly_savings / self.goals['savings_monthly']) * 100, 2),
                'status': 'achieved' if monthly_savings >= self.goals['savings_monthly'] else 'in_progress'
            }
        
        # Spending limits per category
        for goal_key, goal_value in self.goals.items():
            if goal_key.startswith('max_'):
                category = goal_key.replace('max_', '').replace('_', ' ').title()
                spent = abs(month_data[
                    (month_data['Importo'] < 0) & 
                    (month_data['Categoria'].str.contains(category, case=False, na=False))
                ]['Importo'].sum())
                
                progress[f'{goal_key}_progress'] = {
                    'target': goal_value,
                    'actual': round(spent, 2),
                    'remaining': round(goal_value - spent, 2),
                    'progress_pct': round((spent / goal_value) * 100, 2),
                    'status': 'exceeded' if spent > goal_value else 'on_track'
                }
        
        return progress
    
    def compare_with_benchmarks(self, kpis: Dict) -> Dict:
        """Confronta KPI con benchmark nazionali"""
        comparisons = {}
        
        benchmark_mappings = {
            'savings_rate': 'savings_rate',
            'alimentari_ratio': 'food_ratio',
            'trasporti_ratio': 'transport_ratio',
            'intrattenimento_ratio': 'entertainment_ratio',
            'burn_rate': 'avg_monthly_spending'
        }
        
        for kpi_key, benchmark_key in benchmark_mappings.items():
            if kpi_key in kpis and benchmark_key in self.national_benchmarks:
                user_value = kpis[kpi_key]
                benchmark_value = self.national_benchmarks[benchmark_key]
                
                difference = user_value - benchmark_value
                difference_pct = (difference / benchmark_value * 100) if benchmark_value != 0 else 0
                
                status = 'above' if difference > 0 else 'below'
                if abs(difference_pct) < 5:  # Entro 5% è considerato "aligned"
                    status = 'aligned'
                
                comparisons[kpi_key] = {
                    'user_value': round(user_value, 2),
                    'benchmark': round(benchmark_value, 2),
                    'difference': round(difference, 2),
                    'difference_pct': round(difference_pct, 2),
                    'status': status
                }
        
        return comparisons
    
    def generate_financial_score(self, kpis: Dict, goal_progress: Dict) -> Dict:
        """Genera un punteggio finanziario complessivo (0-100)"""
        score_components = {
            'savings_rate': 0,
            'goal_achievement': 0,
            'spending_control': 0,
            'trend_stability': 0
        }
        
        # Savings rate score (30% del totale)
        if 'savings_rate' in kpis:
            savings_rate = kpis['savings_rate']
            if savings_rate >= 20:
                score_components['savings_rate'] = 30
            elif savings_rate >= 10:
                score_components['savings_rate'] = 20
            elif savings_rate >= 5:
                score_components['savings_rate'] = 15
            else:
                score_components['savings_rate'] = max(0, savings_rate)
        
        # Goal achievement score (25% del totale)
        achieved_goals = 0
        total_goals = 0
        for goal_key, goal_data in goal_progress.items():
            if isinstance(goal_data, dict) and 'status' in goal_data:
                total_goals += 1
                if goal_data['status'] in ['achieved', 'on_track']:
                    achieved_goals += 1
        
        if total_goals > 0:
            score_components['goal_achievement'] = (achieved_goals / total_goals) * 25
        
        # Spending control (25% del totale)
        if 'volatilita_spese' in kpis:
            volatility = kpis['volatilita_spese']
            if volatility < 10:
                score_components['spending_control'] = 25
            elif volatility < 20:
                score_components['spending_control'] = 20
            elif volatility < 30:
                score_components['spending_control'] = 15
            else:
                score_components['spending_control'] = 10
        
        # Trend stability (20% del totale)
        if 'trend_spese' in kpis:
            trend = abs(kpis['trend_spese'])
            if trend < 5:
                score_components['trend_stability'] = 20
            elif trend < 10:
                score_components['trend_stability'] = 15
            elif trend < 15:
                score_components['trend_stability'] = 10
            else:
                score_components['trend_stability'] = 5
        
        total_score = sum(score_components.values())
        
        # Determinazione livello
        if total_score >= 80:
            level = "Eccellente"
            emoji = "🌟"
        elif total_score >= 65:
            level = "Buono"
            emoji = "✅"
        elif total_score >= 50:
            level = "Discreto"
            emoji = "⚡"
        elif total_score >= 35:
            level = "Da migliorare"
            emoji = "⚠️"
        else:
            level = "Critico"
            emoji = "🔴"
        
        return {
            'total_score': round(total_score, 1),
            'level': level,
            'emoji': emoji,
            'components': score_components,
            'recommendations': self.generate_recommendations(score_components, kpis)
        }
    
    def calculate_financial_score(self) -> float:
        """Metodo wrapper per compatibilità con i test"""
        kpis = self.calculate_kpis()
        goal_progress = self.calculate_goal_progress()
        score_data = self.generate_financial_score(kpis, goal_progress)
        return score_data.get('total_score', 0.0)
    
    def get_goals_progress(self) -> Dict:
        """Metodo wrapper per compatibilità con i test"""
        return self.calculate_goal_progress()
    
    def get_benchmark_comparison(self) -> Dict:
        """Metodo wrapper per compatibilità con i test"""
        kpis = self.calculate_kpis()
        return self.compare_with_benchmarks(kpis)
    
    def add_goal(self, goal_id: str, target: float, description: str = ""):
        """Aggiunge un nuovo obiettivo finanziario"""
        self.goals[goal_id] = {
            'target': target,
            'description': description,
            'created_date': datetime.now().isoformat()
        }
        self.save_goals()
    
    def generate_recommendations(self, score_components: Dict, kpis: Dict) -> List[str]:
        """Genera raccomandazioni personalizzate"""
        recommendations = []
        
        if score_components['savings_rate'] < 20:
            recommendations.append("💡 Aumenta il tasso di risparmio riducendo le spese non essenziali")
        
        if score_components['spending_control'] < 20:
            recommendations.append("📊 Le tue spese sono molto variabili - considera un budget mensile fisso")
        
        if score_components['goal_achievement'] < 15:
            recommendations.append("🎯 Rivedi i tuoi obiettivi finanziari per renderli più realistici")
        
        if 'burn_rate' in kpis and kpis['burn_rate'] > 1500:
            recommendations.append("💸 La tua spesa mensile è alta - identifica aree di riduzione")
        
        if len(recommendations) == 0:
            recommendations.append("🎉 Ottima gestione finanziaria! Continua così!")
        
        return recommendations
    
    def generate_comprehensive_report(self) -> Dict:
        """Genera report completo con tutti gli analytics"""
        kpis = self.calculate_financial_kpis()
        goal_progress = self.calculate_goal_progress()
        benchmarks = self.compare_with_benchmarks(kpis)
        financial_score = self.generate_financial_score(kpis, goal_progress)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'kpis': kpis,
            'goal_progress': goal_progress,
            'benchmarks': benchmarks,
            'financial_score': financial_score,
            'summary': {
                'total_transactions': len(self.df) if self.df is not None else 0,
                'analysis_period': kpis.get('periodo_analisi', 'N/A'),
                'score': financial_score['total_score'],
                'level': financial_score['level']
            }
        }
    
    def update_goals(self, new_goals: Dict):
        """Aggiorna obiettivi finanziari"""
        self.goals.update(new_goals)
        self.goals['last_updated'] = datetime.now().isoformat()
        self.save_goals()
    
    def export_report(self, format_type: str = 'json', output_path: str = None) -> str:
        """Esporta report in diversi formati"""
        report = self.generate_comprehensive_report()
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"n26_advanced_analytics_{timestamp}"
        
        if format_type == 'json':
            output_path += '.json'
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        
        elif format_type == 'csv':
            output_path += '.csv'
            # Crea un DataFrame con i KPI principali
            kpi_df = pd.DataFrame([report['kpis']])
            kpi_df.to_csv(output_path, index=False)
        
        elif format_type == 'txt':
            output_path += '.txt'
            with open(output_path, 'w') as f:
                f.write(self.format_text_report(report))
        
        return output_path
    
    def format_text_report(self, report: Dict) -> str:
        """Formatta report come testo leggibile"""
        text = "📊 N26 ADVANCED ANALYTICS REPORT\n"
        text += "=" * 50 + "\n\n"
        
        # Financial Score
        score_data = report['financial_score']
        text += f"🏆 PUNTEGGIO FINANZIARIO: {score_data['total_score']}/100 {score_data['emoji']}\n"
        text += f"Livello: {score_data['level']}\n\n"
        
        # KPI principali
        kpis = report['kpis']
        text += "📈 KPI PRINCIPALI:\n"
        text += f"- Tasso di risparmio: {kpis.get('savings_rate', 0)}%\n"
        text += f"- Spesa mensile media: €{kpis.get('burn_rate', 0)}\n"
        text += f"- Saldo netto: €{kpis.get('saldo_netto', 0)}\n\n"
        
        # Raccomandazioni
        text += "💡 RACCOMANDAZIONI:\n"
        for rec in score_data['recommendations']:
            text += f"- {rec}\n"
        
        text += f"\nReport generato: {report['timestamp']}\n"
        
        return text


# Funzioni di integrazione per GUI
def get_advanced_analytics_data(csv_path: str) -> Dict:
    """Ottieni dati analytics per integrazione GUI"""
    analytics = N26AdvancedAnalytics(csv_path)
    return analytics.generate_comprehensive_report()

def update_financial_goals(csv_path: str, goals: Dict) -> bool:
    """Aggiorna obiettivi finanziari"""
    try:
        analytics = N26AdvancedAnalytics(csv_path)
        analytics.update_goals(goals)
        return True
    except Exception as e:
        print(f"Errore aggiornamento goals: {e}")
        return False


if __name__ == "__main__":
    # Test del modulo
    print("📊 N26 Advanced Analytics - Test Module")
    
    # Test con dati esempio (commentato - richiede CSV reale)
    # analytics = N26AdvancedAnalytics("N26_Data.csv")
    # report = analytics.generate_comprehensive_report()
    # print(f"Score finanziario: {report['financial_score']['total_score']}")
    
    print("✅ Modulo Advanced Analytics caricato correttamente")
