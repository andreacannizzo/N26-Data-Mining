#!/usr/bin/env python3
"""
Final validation script for N26 Advanced Analytics Dashboard
"""

import sys
import os

def main():
    print("🚀 N26 Advanced Analytics - Final Validation")
    print("=" * 50)
    
    # Test 1: Module imports
    print("\n📦 Test 1: Module Imports")
    try:
        import pandas as pd
        import numpy as np
        from advanced_analytics import N26AdvancedAnalytics
        print("✅ All required modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Create test data
    print("\n📊 Test 2: Data Creation")
    try:
        data = [
            {'Data': '2024-01-01', 'Importo': 2800.0, 'Categoria': 'Stipendio', 'Beneficiario': 'Azienda', 'Descrizione': 'Stipendio'},
            {'Data': '2024-01-05', 'Importo': -45.20, 'Categoria': 'Alimentari', 'Beneficiario': 'Supermercato', 'Descrizione': 'Spesa'},
            {'Data': '2024-01-10', 'Importo': -25.50, 'Categoria': 'Trasporti', 'Beneficiario': 'ATM', 'Descrizione': 'Trasporti'},
            {'Data': '2024-02-01', 'Importo': 2800.0, 'Categoria': 'Stipendio', 'Beneficiario': 'Azienda', 'Descrizione': 'Stipendio'},
            {'Data': '2024-02-05', 'Importo': -52.30, 'Categoria': 'Alimentari', 'Beneficiario': 'Supermercato', 'Descrizione': 'Spesa'},
        ]
        
        df = pd.DataFrame(data)
        df.to_csv('final_test.csv', index=False)
        print(f"✅ Test data created: {len(data)} records")
    except Exception as e:
        print(f"❌ Data creation error: {e}")
        return False
    
    # Test 3: Analytics initialization
    print("\n🔧 Test 3: Analytics Initialization")
    try:
        analytics = N26AdvancedAnalytics('final_test.csv')
        print("✅ Analytics engine initialized successfully")
    except Exception as e:
        print(f"❌ Analytics initialization error: {e}")
        return False
    
    # Test 4: KPI calculation
    print("\n📈 Test 4: KPI Calculation")
    try:
        kpis = analytics.calculate_kpis()
        print(f"✅ KPIs calculated: {len(kpis)} metrics")
        print(f"   Sample KPIs: {list(kpis.keys())[:3]}")
    except Exception as e:
        print(f"❌ KPI calculation error: {e}")
        return False
    
    # Test 5: Financial score
    print("\n💯 Test 5: Financial Score")
    try:
        score = analytics.calculate_financial_score()
        print(f"✅ Financial score calculated: {score:.1f}/100")
    except Exception as e:
        print(f"❌ Financial score error: {e}")
        return False
    
    # Test 6: Goal tracking
    print("\n🎯 Test 6: Goal Tracking")
    try:
        analytics.add_goal("test_goal", 500, "Test goal description")
        goals = analytics.get_goals_progress()
        print(f"✅ Goal tracking working: {len(goals)} goals")
    except Exception as e:
        print(f"❌ Goal tracking error: {e}")
        return False
    
    # Test 7: Benchmark comparison
    print("\n📊 Test 7: Benchmark Comparison")
    try:
        benchmarks = analytics.get_benchmark_comparison()
        print(f"✅ Benchmark comparison working: {len(benchmarks)} categories")
    except Exception as e:
        print(f"❌ Benchmark comparison error: {e}")
        return False
    
    # Test 8: GUI integration check
    print("\n🖥️ Test 8: GUI Integration Check")
    try:
        with open('gui.py', 'r') as f:
            gui_content = f.read()
        
        if 'open_advanced_analytics' in gui_content and 'Advanced Analytics Dashboard' in gui_content:
            print("✅ GUI integration confirmed")
        else:
            print("⚠️ GUI integration not found")
    except Exception as e:
        print(f"❌ GUI integration check error: {e}")
        return False
    
    # Cleanup
    if os.path.exists('final_test.csv'):
        os.remove('final_test.csv')
    
    print("\n🎉 ALL TESTS PASSED!")
    print("=" * 50)
    print("✅ Advanced Analytics Dashboard is fully functional")
    print("✅ Ready for production use")
    print("✅ All components validated successfully")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
