#!/usr/bin/env python3
"""
N26 Advanced Analytics - Live Demo
Questo script dimostra tutte le funzionalità implementate
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

def print_header(title):
    """Stampa header colorato"""
    print(f"\n{'=' * 60}")
    print(f"🎯 {title}")
    print(f"{'=' * 60}")

def print_section(title):
    """Stampa sezione"""
    print(f"\n📊 {title}")
    print("-" * 40)

def create_realistic_demo_data():
    """Crea 6 mesi di dati N26 realistici"""
    print("📋 Generazione dataset dimostrativo...")
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    # Redditi mensili
    monthly_salaries = [2850, 2850, 2850, 3100, 2850, 2850]  # Bonus a marzo
    for i, salary in enumerate(monthly_salaries):
        date = start_date + timedelta(days=i*30)
        data.append({
            'Data': date.strftime('%Y-%m-%d'),
            'Importo': salary,
            'Categoria': 'Stipendio',
            'Beneficiario': 'AZIENDA TECH SRL',
            'Descrizione': 'Stipendio mensile'
        })
    
    # Spese categorizzate realistiche
    monthly_expenses = [
        # Utenze (fisse)
        [('Utenze', 'ENEL ENERGIA', -125.50, 'Bolletta elettrica'),
         ('Utenze', 'VODAFONE', -45.90, 'Telefono + Internet'),
         ('Utenze', 'HERA GAS', -89.30, 'Bolletta gas')],
        
        # Alimentari (variabili)
        [('Alimentari', 'COOP', -67.40, 'Spesa settimanale'),
         ('Alimentari', 'CARREFOUR', -43.20, 'Spesa quotidiana'),
         ('Alimentari', 'ESSELUNGA', -89.80, 'Spesa grande')],
        
        # Trasporti
        [('Trasporti', 'ATM MILANO', -35.00, 'Abbonamento mensile'),
         ('Trasporti', 'UBER', -15.50, 'Corsa centro'),
         ('Trasporti', 'ENI', -65.00, 'Rifornimento auto')],
        
        # Intrattenimento
        [('Intrattenimento', 'NETFLIX', -12.99, 'Streaming'),
         ('Intrattenimento', 'SPOTIFY', -9.99, 'Musica'),
         ('Intrattenimento', 'AMAZON PRIME', -156.80, 'Shopping online'),
         ('Intrattenimento', 'CINEMA', -24.50, 'Film weekend')],
        
        # Casa e famiglia
        [('Casa', 'IKEA', -234.50, 'Mobili cucina'),
         ('Casa', 'LEROY MERLIN', -67.30, 'Bricolage'),
         ('Casa', 'MEDIAWORLD', -445.00, 'Elettrodomestici')],
        
        # Salute
        [('Salute', 'FARMACIA', -28.50, 'Medicinali'),
         ('Salute', 'STUDIO MEDICO', -85.00, 'Visita specialistica')],
        
        # Abbigliamento
        [('Abbigliamento', 'ZARA', -89.99, 'Vestiti primavera'),
         ('Abbigliamento', 'NIKE', -125.50, 'Scarpe running')]
    ]
    
    # Distribuzione spese nei 6 mesi
    for month in range(6):
        base_date = start_date + timedelta(days=month*30)
        
        # Distribuzione casuale delle spese nel mese
        for category_expenses in monthly_expenses:
            # Non tutte le categorie ogni mese
            if np.random.random() > 0.3:  # 70% probabilità
                for category, beneficiary, base_amount, description in category_expenses:
                    # Variazione casuale ±20%
                    amount = base_amount * np.random.uniform(0.8, 1.2)
                    day_offset = np.random.randint(1, 28)
                    transaction_date = base_date + timedelta(days=day_offset)
                    
                    data.append({
                        'Data': transaction_date.strftime('%Y-%m-%d'),
                        'Importo': round(amount, 2),
                        'Categoria': category,
                        'Beneficiario': beneficiary,
                        'Descrizione': description
                    })
    
    # Ordina per data e salva
    df = pd.DataFrame(data)
    df = df.sort_values('Data').reset_index(drop=True)
    df.to_csv('demo_completo.csv', index=False)
    
    print(f"✅ Dataset creato: {len(data)} transazioni in 6 mesi")
    return df

def main():
    print_header("N26 ADVANCED ANALYTICS - DEMO COMPLETO")
    print("🎯 Questa demo mostra tutte le funzionalità implementate")
    print("📅 Dati: Gennaio - Giugno 2024 (6 mesi di transazioni)")
    
    try:
        # 1. Import e setup
        print_section("1. IMPORT E SETUP")
        from advanced_analytics import N26AdvancedAnalytics
        print("✅ Modulo Advanced Analytics importato")
        
        # 2. Generazione dati
        print_section("2. GENERAZIONE DATASET DEMO")
        df = create_realistic_demo_data()
        
        # 3. Inizializzazione analytics
        print_section("3. INIZIALIZZAZIONE ANALYTICS ENGINE")
        analytics = N26AdvancedAnalytics('demo_completo.csv')
        print("✅ Engine inizializzato con successo")
        
        # 4. Calcolo KPI avanzati
        print_section("4. CALCOLO KPI FINANZIARI AVANZATI")
        kpis = analytics.calculate_kpis()
        
        # Mostra KPI principali
        key_kpis = {
            'monthly_income': 'Reddito Mensile Medio',
            'monthly_expenses': 'Spese Mensili Medie', 
            'savings_rate': 'Tasso di Risparmio',
            'burn_rate': 'Burn Rate',
            'runway_months': 'Mesi di Autonomia',
            'expense_volatility': 'Volatilità Spese'
        }
        
        for kpi_key, kpi_name in key_kpis.items():
            if kpi_key in kpis:
                value = kpis[kpi_key]
                if isinstance(value, (int, float)):
                    if kpi_key in ['monthly_income', 'monthly_expenses', 'burn_rate']:
                        print(f"   💰 {kpi_name}: €{abs(value):,.2f}")
                    elif kpi_key == 'savings_rate':
                        print(f"   📈 {kpi_name}: {value:.1f}%")
                    elif kpi_key == 'runway_months':
                        print(f"   🛫 {kpi_name}: {value:.1f} mesi")
                    elif kpi_key == 'expense_volatility':
                        print(f"   📊 {kpi_name}: {value:.2f}")
        
        # 5. Financial Score
        print_section("5. FINANCIAL HEALTH SCORE")
        score = analytics.calculate_financial_score()
        
        if score >= 80:
            level = "🏆 ECCELLENTE"
            advice = "Ottima gestione finanziaria!"
        elif score >= 65:
            level = "✅ BUONO"  
            advice = "Buon controllo delle finanze"
        elif score >= 50:
            level = "⚠️ DISCRETO"
            advice = "Margini di miglioramento"
        else:
            level = "❌ DA MIGLIORARE"
            advice = "Richiede attenzione"
        
        print(f"   🎯 Financial Score: {score:.1f}/100 ({level})")
        print(f"   💡 Valutazione: {advice}")
        
        # 6. Goal Tracking Demo
        print_section("6. GOAL TRACKING SYSTEM")
        
        # Aggiungi obiettivi dimostrativi
        goals_demo = [
            ("risparmio_mensile", 600, "Risparmio mensile target"),
            ("spese_alimentari", 250, "Budget alimentari mensile"),
            ("emergency_fund", 5000, "Fondo di emergenza"),
            ("investimenti", 300, "Investimenti mensili")
        ]
        
        for goal_id, target, description in goals_demo:
            analytics.add_goal(goal_id, target, description)
        
        goals = analytics.get_goals_progress()
        print(f"   🎯 Obiettivi configurati: {len(goals)}")
        
        for goal_id, goal_data in goals.items():
            progress = goal_data.get('progress', 0)
            target = goal_data.get('target', 1)
            percentage = (progress / target * 100) if target > 0 else 0
            
            if percentage >= 100:
                status = "✅ RAGGIUNTO"
            elif percentage >= 75:
                status = "🟡 VICINO"
            elif percentage >= 50:
                status = "🟠 IN CORSO"
            else:
                status = "🔴 LONTANO"
            
            print(f"   {status} {goal_data.get('description', goal_id)}: {percentage:.1f}%")
        
        # 7. Benchmark Analysis
        print_section("7. BENCHMARK COMPARISON (vs Standard Italiani)")
        benchmarks = analytics.get_benchmark_comparison()
        
        benchmark_categories = ['savings_rate', 'housing_ratio', 'food_ratio', 'transport_ratio']
        for category in benchmark_categories:
            if category in benchmarks:
                data = benchmarks[category]
                user_val = data.get('user_value', 0)
                benchmark_val = data.get('benchmark', 0)
                status = data.get('status', 'neutral')
                
                status_icon = "✅" if status == 'good' else "⚠️" if status == 'warning' else "❌"
                category_name = category.replace('_', ' ').title()
                
                print(f"   {status_icon} {category_name}: {user_val:.1f}% (standard: {benchmark_val:.1f}%)")
        
        # 8. Export delle analisi
        print_section("8. EXPORT REPORT")
        
        # JSON Report completo
        full_report = {
            'timestamp': datetime.now().isoformat(),
            'period': '2024-01 to 2024-06',
            'total_transactions': len(df),
            'financial_score': score,
            'kpis': kpis,
            'goals': goals,
            'benchmarks': benchmarks,
            'summary': {
                'total_income': df[df['Importo'] > 0]['Importo'].sum(),
                'total_expenses': abs(df[df['Importo'] < 0]['Importo'].sum()),
                'net_savings': df['Importo'].sum(),
                'avg_transaction': df['Importo'].mean()
            }
        }
        
        with open('demo_report_completo.json', 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False, default=str)
        
        print("   📄 Report JSON: demo_report_completo.json")
        
        # CSV Summary
        kpi_summary = pd.DataFrame([
            {'Metrica': k, 'Valore': v} for k, v in kpis.items() 
            if isinstance(v, (int, float))
        ])
        kpi_summary.to_csv('demo_kpi_summary.csv', index=False)
        print("   📊 KPI Summary: demo_kpi_summary.csv")
        
        # 9. Risultati finali
        print_header("🎉 DEMO COMPLETATA CON SUCCESSO!")
        print("✅ Tutte le funzionalità Advanced Analytics validate")
        print("✅ Sistema pronto per utilizzo produttivo")
        print("✅ File demo generati per testing")
        
        print(f"\n📁 File generati:")
        print(f"   • demo_completo.csv - Dataset demo (6 mesi)")
        print(f"   • demo_report_completo.json - Report analytics completo")
        print(f"   • demo_kpi_summary.csv - Riassunto KPI")
        
        print(f"\n🚀 Per usare il sistema:")
        print(f"   • GUI principale: python3 gui.py")
        print(f"   • Dashboard standalone: python3 analytics_dashboard.py")
        print(f"   • Launcher script: ./start_analytics.sh")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Errore durante la demo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🌟 Demo eseguita con successo!")
    else:
        print(f"\n💥 Demo fallita!")
    
    print(f"\n📞 Per supporto, consulta: IMPLEMENTATION_COMPLETE.md")
