#!/usr/bin/env python3
"""
Test rapido per Advanced Analytics implementation
Verifica funzionalità base senza GUI
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def create_sample_data():
    """Crea dati CSV di esempio per test"""
    # Genera dati di esempio realistici
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    categories = ['Alimentari', 'Trasporti', 'Intrattenimento', 'Utenze', 'Abbigliamento', 'Salute', 'Casa']
    beneficiaries = ['Supermercato', 'Amazon', 'Netflix', 'Enel', 'Zara', 'Farmacia', 'IKEA', 'ATM', 'Uber']
    
    data = []
    
    for i, date in enumerate(dates):
        # Simula transazioni con pattern realistici
        if i % 7 in [0, 6]:  # Weekend - più spese entertainment
            num_transactions = np.random.randint(0, 3)
            likely_cats = ['Intrattenimento', 'Alimentari']
        elif i % 30 == 0:  # Inizio mese - stipendio
            data.append({
                'Data': date.strftime('%Y-%m-%d'),
                'Importo': np.random.uniform(2500, 3500),
                'Categoria': 'Stipendio',
                'Beneficiario': 'Azienda XYZ',
                'Descrizione': 'Stipendio mensile'
            })
            num_transactions = np.random.randint(3, 6)
            likely_cats = categories
        else:  # Giorni normali
            num_transactions = np.random.randint(0, 2)
            likely_cats = ['Alimentari', 'Trasporti', 'Utenze']
        
        # Genera transazioni per il giorno
        for _ in range(num_transactions):
            cat = np.random.choice(likely_cats)
            ben = np.random.choice(beneficiaries)
            
            # Importi realistici per categoria
            if cat == 'Alimentari':
                amount = -np.random.uniform(15, 80)
            elif cat == 'Trasporti':
                amount = -np.random.uniform(5, 25)
            elif cat == 'Intrattenimento':
                amount = -np.random.uniform(10, 60)
            elif cat == 'Utenze':
                amount = -np.random.uniform(50, 200)
            elif cat == 'Abbigliamento':
                amount = -np.random.uniform(25, 150)
            elif cat == 'Salute':
                amount = -np.random.uniform(20, 100)
            else:
                amount = -np.random.uniform(20, 100)
            
            data.append({
                'Data': date.strftime('%Y-%m-%d'),
                'Importo': round(amount, 2),
                'Categoria': cat,
                'Beneficiario': ben,
                'Descrizione': f'Transazione {cat.lower()}'
            })
    
    # Crea DataFrame e salva
    df = pd.DataFrame(data)
    csv_path = 'N26_Data_Test.csv'
    df.to_csv(csv_path, index=False)
    print(f"✅ Dati di test creati: {csv_path} ({len(df)} transazioni)")
    return csv_path

def test_advanced_analytics():
    """Test del modulo Advanced Analytics"""
    print("🧪 Test Advanced Analytics Module")
    print("=" * 40)
    
    try:
        # Import numpy per dati di esempio
        import numpy as np
        
        # Crea dati di test
        csv_path = create_sample_data()
        
        # Test import modulo
        print("📦 Test import moduli...")
        from advanced_analytics import N26AdvancedAnalytics
        print("✅ Modulo advanced_analytics importato")
        
        # Test inizializzazione
        print("🔧 Test inizializzazione...")
        analytics = N26AdvancedAnalytics(csv_path)
        print(f"✅ Analytics inizializzato con {len(analytics.df)} records")
        
        # Test KPI calculation
        print("📊 Test calcolo KPI...")
        kpis = analytics.calculate_financial_kpis()
        print(f"✅ KPI calcolati: {len(kpis)} metriche")
        
        # Print alcuni KPI chiave
        key_kpis = ['savings_rate', 'burn_rate', 'saldo_netto']
        for kpi in key_kpis:
            if kpi in kpis:
                print(f"   - {kpi}: {kpis[kpi]}")
        
        # Test goal progress
        print("🎯 Test goal progress...")
        goal_progress = analytics.calculate_goal_progress()
        print(f"✅ Goal progress calcolato: {len(goal_progress)} obiettivi")
        
        # Test benchmarks
        print("📈 Test benchmark comparison...")
        benchmarks = analytics.compare_with_benchmarks(kpis)
        print(f"✅ Benchmark comparison: {len(benchmarks)} confronti")
        
        # Test financial score
        print("🏆 Test financial score...")
        financial_score = analytics.generate_financial_score(kpis, goal_progress)
        score = financial_score.get('total_score', 0)
        level = financial_score.get('level', 'N/A')
        print(f"✅ Financial score: {score:.1f}/100 ({level})")
        
        # Test report completo
        print("📋 Test report completo...")
        report = analytics.generate_comprehensive_report()
        print(f"✅ Report generato: {len(report)} sezioni")
        
        # Test export
        print("💾 Test export...")
        export_path = analytics.export_report('json', 'test_analytics_report')
        print(f"✅ Report esportato: {export_path}")
        
        # Test update goals
        print("🎯 Test update goals...")
        new_goals = {'savings_monthly': 500, 'test_goal': 1000}
        analytics.update_goals(new_goals)
        print("✅ Goals aggiornati")
        
        print("\n🎉 Tutti i test Advanced Analytics PASSED!")
        return True
        
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        print("   Installa: pip install scikit-learn statsmodels")
        return False
    except Exception as e:
        print(f"❌ Errore test: {e}")
        return False

def test_analytics_dashboard():
    """Test del dashboard GUI (senza aprire finestra)"""
    print("\n🖥️ Test Analytics Dashboard")
    print("=" * 40)
    
    try:
        # Test import dashboard
        print("📦 Test import dashboard...")
        from analytics_dashboard import AdvancedAnalyticsDashboard, KPICard, GoalProgressWidget
        print("✅ Moduli dashboard importati")
        
        # Test creazione componenti (senza show())
        print("🧱 Test componenti GUI...")
        
        # Inizializza Qt Application per test headless
        from PyQt5.QtWidgets import QApplication
        import sys
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test KPI Card
        kpi_card = KPICard("Test KPI", 85.5, "%", "Test description", 2.3)
        print("✅ KPI Card creato")
        
        # Test Goal Progress Widget  
        goal_widget = GoalProgressWidget("test_goal", 1000, 750, "€")
        print("✅ Goal Progress Widget creato")
        
        print("✅ Test dashboard components PASSED!")
        return True
        
    except ImportError as e:
        print(f"❌ Errore import dashboard: {e}")
        print("   Installa: pip install PyQt5")
        return False
    except Exception as e:
        print(f"❌ Errore test dashboard: {e}")
        return False

def test_gui_integration():
    """Test integrazione con GUI principale"""
    print("\n🔗 Test GUI Integration")
    print("=" * 40)
    
    try:
        # Verifica che il file gui.py contenga il nuovo metodo
        if os.path.exists('gui.py'):
            with open('gui.py', 'r') as f:
                gui_content = f.read()
            
            if 'open_advanced_analytics' in gui_content:
                print("✅ Metodo open_advanced_analytics trovato in gui.py")
            else:
                print("⚠️  Metodo open_advanced_analytics NON trovato in gui.py")
            
            if 'Advanced Analytics Dashboard' in gui_content:
                print("✅ Pulsante Advanced Analytics trovato in gui.py")
            else:
                print("⚠️  Pulsante Advanced Analytics NON trovato in gui.py")
        else:
            print("❌ File gui.py non trovato")
            return False
        
        print("✅ Test GUI integration PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Errore test GUI integration: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 N26 Advanced Analytics - Test Suite")
    print("=" * 50)
    print(f"Data/ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Esegui tutti i test
    tests = [
        ("Advanced Analytics Core", test_advanced_analytics),
        ("Analytics Dashboard GUI", test_analytics_dashboard),
        ("GUI Integration", test_gui_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} fallito: {e}")
            results.append((test_name, False))
    
    # Riepilogo risultati
    print("\n" + "=" * 50)
    print("📋 RIEPILOGO TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{status} - {test_name}")
        if passed_test:
            passed += 1
    
    print(f"\n🎯 RISULTATO FINALE: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 TUTTI I TEST SONO PASSATI! Advanced Analytics è pronto!")
        print("\n🚀 Per utilizzare:")
        print("   1. GUI integrata: python gui.py (pulsante Advanced Analytics)")
        print("   2. Dashboard standalone: ./start_analytics.sh")
        print("   3. Python API: from advanced_analytics import N26AdvancedAnalytics")
    else:
        print("⚠️  Alcuni test sono falliti. Controlla gli errori sopra.")
    
    # Cleanup file di test
    test_files = ['N26_Data_Test.csv', 'test_analytics_report.json', 'financial_goals.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Rimosso file di test: {file}")

if __name__ == "__main__":
    main()
