#!/usr/bin/env python3
"""
N26 Data Mining - Web Dashboard con Flask e Plotly
Dashboard web interattiva real-time per analisi N26
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime
import os

app = Flask(__name__)

class N26WebDashboard:
    """Dashboard web per visualizzazione dati N26"""
    
    def __init__(self, csv_path="N26_Data.csv"):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Carica dati CSV"""
        try:
            if os.path.exists(self.csv_path):
                self.df = pd.read_csv(self.csv_path)
                self.df['Data'] = pd.to_datetime(self.df['Data'])
                self.df['Importo'] = pd.to_numeric(self.df['Importo'], errors='coerce')
        except Exception as e:
            print(f"Errore caricamento: {e}")
    
    def get_summary_stats(self):
        """Statistiche riepilogative"""
        if self.df is None or self.df.empty:
            return {}
        
        return {
            'totale_transazioni': len(self.df),
            'saldo_totale': round(self.df['Importo'].sum(), 2),
            'spesa_media': round(self.df['Importo'].mean(), 2),
            'ultima_transazione': self.df['Data'].max().strftime('%Y-%m-%d'),
            'categoria_top': self.df['Categoria'].mode().iloc[0] if not self.df['Categoria'].empty else 'N/A'
        }
    
    def create_spending_timeline(self):
        """Grafico timeline spese"""
        if self.df is None or self.df.empty:
            return {}
        
        daily_spending = self.df.groupby(self.df['Data'].dt.date)['Importo'].sum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_spending.index,
            y=daily_spending.values,
            mode='lines+markers',
            name='Spese Giornaliere',
            line=dict(color='#34a853', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Andamento Spese nel Tempo',
            xaxis_title='Data',
            yaxis_title='Importo (€)',
            template='plotly_dark',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def create_category_pie(self):
        """Grafico a torta categorie"""
        if self.df is None or self.df.empty:
            return {}
        
        category_spending = self.df.groupby('Categoria')['Importo'].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=category_spending.index,
            values=category_spending.values,
            hole=0.4,
            marker_colors=['#34a853', '#4285f4', '#ea4335', '#fbbc04', '#9aa0a6']
        )])
        
        fig.update_layout(
            title='Distribuzione Spese per Categoria',
            template='plotly_dark',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    def create_heatmap(self):
        """Heatmap spese per giorno/ora"""
        if self.df is None or self.df.empty:
            return {}
        
        self.df['giorno_settimana'] = self.df['Data'].dt.day_name()
        self.df['ora'] = self.df['Data'].dt.hour
        
        heatmap_data = self.df.pivot_table(
            values='Importo', 
            index='giorno_settimana', 
            columns='ora', 
            aggfunc='sum', 
            fill_value=0
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Greens'
        ))
        
        fig.update_layout(
            title='Heatmap Spese (Giorno/Ora)',
            xaxis_title='Ora del Giorno',
            yaxis_title='Giorno della Settimana',
            template='plotly_dark',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Istanza globale dashboard
dashboard = N26WebDashboard()

@app.route('/')
def index():
    """Pagina principale dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API statistiche"""
    return jsonify(dashboard.get_summary_stats())

@app.route('/api/timeline')
def api_timeline():
    """API grafico timeline"""
    return dashboard.create_spending_timeline()

@app.route('/api/categories')
def api_categories():
    """API grafico categorie"""
    return dashboard.create_category_pie()

@app.route('/api/heatmap')
def api_heatmap():
    """API heatmap"""
    return dashboard.create_heatmap()

@app.route('/api/refresh')
def api_refresh():
    """Aggiorna dati"""
    dashboard.load_data()
    return jsonify({'status': 'success', 'message': 'Dati aggiornati'})

if __name__ == '__main__':
    # Crea template directory se non esiste
    os.makedirs('templates', exist_ok=True)
    
    # Template HTML (creato automaticamente)
    html_template = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N26 Data Mining - Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { 
            background: #222; 
            color: #fff; 
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .header { 
            text-align: center; 
            color: #34a853; 
            margin-bottom: 30px;
        }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: #333; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
        }
        .stat-value { 
            font-size: 24px; 
            font-weight: bold; 
            color: #34a853;
        }
        .charts-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 20px;
        }
        .chart-container { 
            background: #333; 
            border-radius: 10px; 
            padding: 10px;
        }
        .full-width { 
            grid-column: 1 / -1;
        }
        .refresh-btn {
            background: #34a853;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 N26 Data Mining Dashboard</h1>
        <button class="refresh-btn" onclick="refreshData()">🔄 Aggiorna Dati</button>
    </div>
    
    <div class="stats-grid" id="stats-grid">
        <!-- Stats cards will be populated by JavaScript -->
    </div>
    
    <div class="charts-grid">
        <div class="chart-container full-width">
            <div id="timeline-chart"></div>
        </div>
        <div class="chart-container">
            <div id="category-chart"></div>
        </div>
        <div class="chart-container">
            <div id="heatmap-chart"></div>
        </div>
    </div>

    <script>
        // Carica statistiche
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            const statsGrid = document.getElementById('stats-grid');
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.totale_transazioni || 0}</div>
                    <div>Transazioni</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">€${stats.saldo_totale || 0}</div>
                    <div>Saldo Totale</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">€${stats.spesa_media || 0}</div>
                    <div>Spesa Media</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.categoria_top || 'N/A'}</div>
                    <div>Categoria Top</div>
                </div>
            `;
        }
        
        // Carica grafici
        async function loadCharts() {
            // Timeline
            const timelineResponse = await fetch('/api/timeline');
            const timelineData = await timelineResponse.json();
            Plotly.newPlot('timeline-chart', timelineData.data, timelineData.layout);
            
            // Categorie
            const categoryResponse = await fetch('/api/categories');
            const categoryData = await categoryResponse.json();
            Plotly.newPlot('category-chart', categoryData.data, categoryData.layout);
            
            // Heatmap
            const heatmapResponse = await fetch('/api/heatmap');
            const heatmapData = await heatmapResponse.json();
            Plotly.newPlot('heatmap-chart', heatmapData.data, heatmapData.layout);
        }
        
        // Aggiorna dati
        async function refreshData() {
            await fetch('/api/refresh');
            loadStats();
            loadCharts();
        }
        
        // Caricamento iniziale
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadCharts();
            
            // Auto-refresh ogni 30 secondi
            setInterval(refreshData, 30000);
        });
    </script>
</body>
</html>
    '''
    
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("🌐 Avvio Web Dashboard su http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
