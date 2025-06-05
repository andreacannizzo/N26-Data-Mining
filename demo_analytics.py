#!/usr/bin/env python3
"""
N26 Advanced Analytics - Demonstration Script
Mostra le funzionalità avanzate implementate
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import sys

def create_demo_data():
    """Crea dati dimostrativi realistici"""
    print("📊 Generazione dati dimostrativi N26...")
    
    # Genera 6 mesi di transazioni realistiche
    data = []
    base_date = datetime(2024, 1, 1)
    
    # Stipendi mensili
    for month in range(6):
        salary_date = base_date + timedelta(days=month*30)
        data.append({
            'Data': salary_date.strftime('%Y-%m-%d'),
            'Importo': 2850.00,
            'Categoria': 'Stipendio',
            'Beneficiario': 'MIA AZIENDA SRL',
            'Descrizione': 'Stipendio mensile'
        })
    
    # Spese ricorrenti e casuali
    expenses_data = [
        # Alimentari
        ('2024-01-03', -67.45, 'Alimentari', 'COOP SUPERMERCATO', 'Spesa alimentare'),
        ('2024-01-08', -43.20, 'Alimentari', 'CARREFOUR EXPRESS', 'Spesa quotidiana'),
        ('2024-01-15', -89.30, 'Alimentari', 'ESSELUNGA', 'Spesa settimanale'),
        
        # Trasporti
        ('2024-01-02', -35.00, 'Trasporti', 'ATM MILANO', 'Abbonamento mensile'),
        ('2024-01-12', -15.50, 'Trasporti', 'UBER', 'Corsa urbana'),
        ('2024-01-20', -28.00, 'Trasporti', 'TRENORD', 'Biglietto treno'),
        
        # Utenze
        ('2024-01-15', -125.67, 'Utenze', 'ENEL ENERGIA', 'Bolletta elettrica'),
        ('2024-01-18', -45.23, 'Utenze', 'VODAFONE', 'Bolletta telefono'),
        ('2024-01-25', -89.40, 'Utenze', 'HERA GAS', 'Bolletta gas'),
        
        # Intrattenimento
        ('2024-01-05', -12.99, 'Intrattenimento', 'NETFLIX', 'Abbonamento streaming'),
        ('2024-01-10', -156.80, 'Intrattenimento', 'AMAZON', 'Acquisti online'),
        ('2024-01-22', -78.50, 'Intrattenimento', 'CINEMA ODEON', 'Uscita serale'),
        
        # Casa
        ('2024-01-07', -234.50, 'Casa', 'IKEA', 'Mobili e accessori'),
        ('2024-01-14', -67.30, 'Casa', 'LEROY MERLIN', 'Materiali fai da te'),
        
        # Salute
        ('2024-01-09', -45.00, 'Salute', 'FARMACIA SAN CARLO', 'Medicinali'),
        ('2024-01-16', -85.00, 'Salute', 'STUDIO MEDICO', 'Visita specialistica'),
        
        # Abbigliamento
        ('2024-01-11', -89.99, 'Abbigliamento', 'ZARA', 'Vestiti invernali'),
        ('2024-01-19', -125.50, 'Abbigliamento', 'NIKE STORE', 'Scarpe sportive'),
    ]
    
    # Replica per altri mesi con variazioni
    for month_offset in range(1, 6):
        for date_str, amount, cat, ben, desc in expenses_data:
            original_date = datetime.strptime(date_str, '%Y-%m-%d')
            new_date = original_date + timedelta(days=month_offset*30)
            
            # Aggiungi variazione casuale
            variation = np.random.uniform(0.8, 1.2)
            new_amount = amount * variation
            
            data.append({
                'Data': new_date.strftime('%Y-%m-%d'),
                'Importo': round(new_amount, 2),
                'Categoria': cat,
                'Beneficiario': ben,
                'Descrizione': desc
            })
    
    # Salva in CSV
    df = pd.DataFrame(data)
    df = df.sort_values('Data').reset_index(drop=True)
    df.to_csv('demo_n26_data.csv', index=False)
    
    print(f"✅ Creati {len(data)} record dimostrativi")
    return df

def demo_advanced_analytics():
    """Dimostra le funzionalità advanced analytics"""
    print("\n🔬 DEMO: N26 Advanced Analytics Engine")
    print("=" * 50)
    
    try:
        # Import del modulo
        from advanced_analytics import N26AdvancedAnalytics
        
        # Crea dati demo
        df = create_demo_data()
        
        # Inizializza analytics
        analytics = N26AdvancedAnalytics('demo_n26_data.csv')
        print("✅ Advanced Analytics Engine inizializzato")
        
        # 1. KPI FINANZIARI AVANZATI
        print("\n📊 1. KPI FINANZIARI AVANZATI")
        print("-" * 35)
        kpis = analytics.calculate_kpis()
        
        key_metrics = [
            'monthly_income', 'monthly_expenses', 'savings_rate', 
            'burn_rate', 'runway_months', 'expense_volatility'
        ]
        
        for metric in key_metrics:
            if metric in kpis:
                value = kpis[metric]
                if isinstance(value, (int, float)):
                    if metric == 'savings_rate':
                        print(f"   💰 Tasso di Risparmio: {value:.1f}%")
                    elif metric == 'monthly_income':
                        print(f"   📈 Reddito Mensile: €{value:,.2f}")
                    elif metric == 'monthly_expenses':
                        print(f"   📉 Spese Mensili: €{abs(value):,.2f}")
                    elif metric == 'burn_rate':
                        print(f"   🔥 Burn Rate: €{abs(value):,.2f}/mese")
                    elif metric == 'runway_months':
                        print(f"   🛫 Autonomia: {value:.1f} mesi")
                    elif metric == 'expense_volatility':
                        print(f"   📊 Volatilità Spese: {value:.2f}")
        
        # 2. FINANCIAL SCORE
        print("\n💯 2. FINANCIAL SCORE")
        print("-" * 25)
        score = analytics.calculate_financial_score()
        score_level = "Eccellente" if score >= 80 else "Buono" if score >= 60 else "Da Migliorare"
        print(f"   🎯 Financial Score: {score:.1f}/100 ({score_level})")
        
        # 3. GOAL TRACKING
        print("\n🎯 3. GOAL TRACKING")
        print("-" * 20)
        
        # Aggiungi alcuni obiettivi demo
        analytics.add_goal("risparmio_mensile", 500, "Risparmio target mensile")
        analytics.add_goal("spese_alimentari", 300, "Budget alimentari mensile")
        analytics.add_goal("emergency_fund", 5000, "Fondo di emergenza")
        
        goals = analytics.get_goals_progress()
        for goal_id, goal_data in goals.items():
            progress = goal_data.get('progress', 0)
            target = goal_data.get('target', 0)
            progress_pct = (progress / target * 100) if target > 0 else 0
            status = "✅" if progress_pct >= 100 else "🔄" if progress_pct >= 50 else "⚠️"
            print(f"   {status} {goal_data.get('description', goal_id)}: {progress_pct:.1f}%")
        
        # 4. BENCHMARK COMPARISON
        print("\n📈 4. BENCHMARK COMPARISON")
        print("-" * 28)
        benchmarks = analytics.get_benchmark_comparison()
        
        for category, data in list(benchmarks.items())[:4]:
            user_value = data.get('user_value', 0)
            benchmark = data.get('benchmark', 0)
            status = data.get('status', 'neutral')
            status_icon = "✅" if status == 'good' else "⚠️" if status == 'warning' else "❌"
            print(f"   {status_icon} {category}: {user_value:.1f}% (benchmark: {benchmark:.1f}%)")
        
        # 5. EXPORT CAPABILITIES
        print("\n📁 5. EXPORT CAPABILITIES")
        print("-" * 25)
        
        # Export JSON report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'kpis': kpis,
            'financial_score': score,
            'goals': goals,
            'benchmarks': benchmarks
        }
        
        with open('demo_analytics_report.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        print("   📄 Report JSON esportato: demo_analytics_report.json")
        
        # Export CSV summary
        summary_data = []
        for metric, value in kpis.items():
            summary_data.append({'Metric': metric, 'Value': value})
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv('demo_kpi_summary.csv', index=False)
        print("   📊 KPI Summary CSV esportato: demo_kpi_summary.csv")
        
        print("\n🎉 DEMO COMPLETATA CON SUCCESSO!")
        print("=" * 50)
        print("✅ Tutte le funzionalità Advanced Analytics sono operative")
        print("✅ Il sistema è pronto per l'integrazione produttiva")
        print("✅ I file demo sono stati generati per testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup dei file temporanei (opzionale)
        temp_files = ['demo_n26_data.csv']
        for file in temp_files:
            if os.path.exists(file):
                # os.remove(file)  # Manteniamo i file per testing
                pass

if __name__ == "__main__":
    print("🚀 N26 ADVANCED ANALYTICS - DEMO SYSTEM")
    print("=" * 55)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"💻 Directory: {os.getcwd()}")
    print()
    
    success = demo_advanced_analytics()
    
    if success:
        print("\n✨ La demo è stata eseguita con successo!")
        print("   Puoi ora utilizzare il sistema Advanced Analytics.")
        sys.exit(0)
    else:
        print("\n❌ Demo fallita. Verifica la configurazione.")
        sys.exit(1)
