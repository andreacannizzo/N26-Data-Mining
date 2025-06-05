#!/usr/bin/env python3
"""
Test semplificato per Advanced Analytics - Solo modulo core
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def create_test_data():
    """Crea dati CSV di test semplificati"""
    print("📊 Creazione dati di test...")
    
    # Dati di esempio realistici per 6 mesi
    data = []
    
    # Stipendio mensile
    for month in range(1, 7):
        data.append({
            'Data': f'2024-0{month}-01',
            'Importo': 2800.0,
            'Categoria': 'Stipendio',
            'Beneficiario': 'Azienda XYZ',
            'Descrizione': 'Stipendio mensile'
        })
    
    # Spese varie
    expenses = [
        ('2024-01-05', -45.20, 'Alimentari', 'Supermercato', 'Spesa settimanale'),
        ('2024-01-10', -25.50, 'Trasporti', 'ATM', 'Abbonamento mensile'),
        ('2024-01-15', -120.00, 'Utenze', 'Enel', 'Bolletta elettrica'),
        ('2024-02-03', -52.30, 'Alimentari', 'Supermercato', 'Spesa settimanale'),
        ('2024-02-12', -89.99, 'Intrattenimento', 'Amazon', 'Acquisti vari'),
        ('2024-02-20', -75.00, 'Abbigliamento', 'Zara', 'Vestiti'),
        ('2024-03-01', -200.00, 'Casa', 'IKEA', 'Mobili'),
        ('2024-03-15', -45.60, 'Alimentari', 'Supermercato', 'Spesa settimanale'),
        ('2024-04-05', -30.00, 'Salute', 'Farmacia', 'Medicinali'),
        ('2024-04-18', -156.80, 'Intrattenimento', 'Weekend fuori', 'Viaggio'),
        ('2024-05-10', -67.40, 'Alimentari', 'Supermercato', 'Spesa settimanale'),
        ('2024-05-25', -89.90, 'Trasporti', 'Uber', 'Corse varie'),
        ('2024-06-02', -123.45, 'Utenze', 'Vodafone', 'Bolletta telefono'),
        ('2024-06-15', -78.20, 'Alimentari', 'Supermercato', 'Spesa settimanale'),
    ]
    
    for date, amount, cat, ben, desc in expenses:
        data.append({
            'Data': date,
            'Importo': amount,
            'Categoria': cat,
            'Beneficiario': ben,
            'Descrizione': desc
        })
    
    # Crea DataFrame e salva CSV
    df = pd.DataFrame(data)
    df.to_csv('test_data.csv', index=False)
    print(f"✅ Creati {len(data)} record di test in test_data.csv")
    return df

def test_advanced_analytics():
    """Test del modulo Advanced Analytics"""
    print("\n🧪 Test Advanced Analytics Module")
    print("=" * 40)
    
    try:
        # Test import
        print("📦 Test import advanced_analytics...")
        from advanced_analytics import N26AdvancedAnalytics
        print("✅ Modulo importato correttamente")
        
        # Crea dati di test
        df = create_test_data()
        
        # Inizializza analytics
        print("🔧 Inizializzazione analytics...")
        analytics = N26AdvancedAnalytics('test_data.csv')
        print("✅ Analytics inizializzato")
        
        # Test calcolo KPI
        print("📊 Test calcolo KPI...")
        kpis = analytics.calculate_kpis()
        print(f"✅ KPI calcolati: {len(kpis)} metriche")
        
        for key, value in kpis.items():
            if isinstance(value, (int, float)):
                print(f"   • {key}: {value:.2f}")
            else:
                print(f"   • {key}: {value}")
        
        # Test financial score
        print("\n💯 Test Financial Score...")
        score = analytics.calculate_financial_score()
        print(f"✅ Financial Score: {score:.1f}/100")
        
        # Test benchmark
        print("\n📈 Test Benchmark...")
        benchmarks = analytics.get_benchmark_comparison()
        print(f"✅ Benchmark generati: {len(benchmarks)} categorie")
        
        # Test goals (esempio)
        print("\n🎯 Test Goal Tracking...")
        analytics.add_goal("risparmio_mensile", 500, "Risparmio target mensile")
        goals = analytics.get_goals_progress()
        print(f"✅ Goal tracking: {len(goals)} obiettivi")
        
        print("\n🎉 TUTTI I TEST SUPERATI!")
        return True
        
    except Exception as e:
        print(f"❌ Errore test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')

if __name__ == "__main__":
    print("🚀 N26 Advanced Analytics - Test Core Module")
    print("=" * 50)
    print(f"Data/ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_advanced_analytics()
    
    if success:
        print("\n✅ Test completato con successo!")
        sys.exit(0)
    else:
        print("\n❌ Test fallito!")
        sys.exit(1)
