#!/usr/bin/env python3
"""
N26 Data Mining - AI/ML Advanced Analytics Module
Implementazioni avanzate di intelligenza artificiale per analisi finanziarie
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class N26AIAnalytics:
    """Modulo di analisi AI avanzate per dati N26"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Carica e preprocessa i dati"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.df['Data'] = pd.to_datetime(self.df['Data'])
            self.df['Importo'] = pd.to_numeric(self.df['Importo'], errors='coerce')
            self.df = self.df.dropna()
        except Exception as e:
            print(f"Errore caricamento dati: {e}")
    
    def spending_pattern_analysis(self):
        """Analisi pattern di spesa con clustering"""
        features = [
            'giorno_settimana', 'ora', 'importo_normalizzato', 
            'categoria_encoded', 'stagione'
        ]
        
        # Feature engineering
        self.df['giorno_settimana'] = self.df['Data'].dt.dayofweek
        self.df['ora'] = self.df['Data'].dt.hour
        self.df['stagione'] = self.df['Data'].dt.month % 12 // 3
        
        # Normalizzazione importi
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        self.df['importo_normalizzato'] = scaler.fit_transform(
            self.df[['Importo']]
        )
        
        # Encoding categorie
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        self.df['categoria_encoded'] = le.fit_transform(self.df['Categoria'])
        
        # K-means clustering
        from sklearn.cluster import KMeans
        X = self.df[features].fillna(0)
        kmeans = KMeans(n_clusters=5, random_state=42)
        self.df['cluster_spesa'] = kmeans.fit_predict(X)
        
        return self.analyze_clusters()
    
    def analyze_clusters(self):
        """Analizza i cluster identificati"""
        cluster_analysis = {}
        for cluster in self.df['cluster_spesa'].unique():
            cluster_data = self.df[self.df['cluster_spesa'] == cluster]
            
            cluster_analysis[f'Cluster_{cluster}'] = {
                'dimensione': len(cluster_data),
                'spesa_media': cluster_data['Importo'].mean(),
                'categoria_principale': cluster_data['Categoria'].mode().iloc[0],
                'giorno_preferito': cluster_data['giorno_settimana'].mode().iloc[0],
                'caratteristiche': self.describe_cluster(cluster_data)
            }
        
        return cluster_analysis
    
    def describe_cluster(self, cluster_data):
        """Descrizione automatica del cluster"""
        avg_amount = cluster_data['Importo'].mean()
        top_category = cluster_data['Categoria'].mode().iloc[0]
        preferred_day = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'][
            cluster_data['giorno_settimana'].mode().iloc[0]
        ]
        
        if avg_amount > 100:
            amount_desc = "spese elevate"
        elif avg_amount > 30:
            amount_desc = "spese medie"
        else:
            amount_desc = "spese piccole"
        
        return f"{amount_desc} in {top_category}, preferibilmente {preferred_day}"
    
    def anomaly_detection(self):
        """Rilevamento anomalie nelle spese"""
        from sklearn.ensemble import IsolationForest
        
        features = ['Importo', 'giorno_settimana', 'ora']
        X = self.df[features].fillna(0)
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        self.df['anomalia'] = iso_forest.fit_predict(X)
        
        anomalies = self.df[self.df['anomalia'] == -1]
        
        return {
            'numero_anomalie': len(anomalies),
            'spesa_anomala_media': anomalies['Importo'].mean(),
            'anomalie_dettagli': anomalies[['Data', 'Importo', 'Categoria', 'Beneficiario']].to_dict('records')[:10]
        }
    
    def spending_forecast(self, days_ahead=30):
        """Previsione spese future con modello ARIMA"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            
            # Aggregazione giornaliera
            daily_spending = self.df.groupby(self.df['Data'].dt.date)['Importo'].sum()
            daily_spending.index = pd.to_datetime(daily_spending.index)
            
            # Riempimento giorni mancanti
            date_range = pd.date_range(start=daily_spending.index.min(), 
                                     end=daily_spending.index.max(), freq='D')
            daily_spending = daily_spending.reindex(date_range, fill_value=0)
            
            # Modello ARIMA
            model = ARIMA(daily_spending, order=(1,1,1))
            fitted_model = model.fit()
            
            # Previsione
            forecast = fitted_model.forecast(steps=days_ahead)
            
            return {
                'previsione_prossimi_giorni': forecast.tolist(),
                'spesa_prevista_totale': forecast.sum(),
                'confidenza_modello': fitted_model.aic
            }
        except Exception as e:
            return {'errore': f'Impossibile creare previsione: {e}'}
    
    def smart_budgeting(self):
        """Sistema di budgeting intelligente"""
        monthly_spending = self.df.groupby(
            [self.df['Data'].dt.year, self.df['Data'].dt.month, 'Categoria']
        )['Importo'].sum().reset_index()
        
        # Calcolo budget suggeriti per categoria
        budget_suggestions = {}
        for categoria in self.df['Categoria'].unique():
            cat_spending = monthly_spending[monthly_spending['Categoria'] == categoria]['Importo']
            
            if len(cat_spending) > 0:
                avg_monthly = cat_spending.mean()
                std_monthly = cat_spending.std()
                
                # Budget = media + 1 deviazione standard (margine sicurezza)
                suggested_budget = avg_monthly + std_monthly
                
                budget_suggestions[categoria] = {
                    'budget_suggerito': round(suggested_budget, 2),
                    'spesa_media_mensile': round(avg_monthly, 2),
                    'volatilita': round(std_monthly, 2)
                }
        
        return budget_suggestions
    
    def generate_ai_insights(self):
        """Genera insights AI comprensivi"""
        insights = {
            'pattern_analysis': self.spending_pattern_analysis(),
            'anomalies': self.anomaly_detection(),
            'forecast': self.spending_forecast(),
            'smart_budget': self.smart_budgeting(),
            'timestamp': datetime.now().isoformat()
        }
        
        return insights

# Funzioni di utilità per integrazione GUI
def get_ai_recommendations(csv_path):
    """Ottieni raccomandazioni AI"""
    try:
        ai_analyzer = N26AIAnalytics(csv_path)
        return ai_analyzer.generate_ai_insights()
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # Test del modulo
    print("🤖 N26 AI Analytics - Test Module")
    # ai = N26AIAnalytics("N26_Data.csv")  # Uncomment when CSV available
    # insights = ai.generate_ai_insights()
    # print(insights)
