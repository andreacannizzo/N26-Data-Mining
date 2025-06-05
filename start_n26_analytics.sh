#!/bin/bash

# N26 Advanced Analytics Launcher
# This script activates the virtual environment and launches the system

echo "🚀 N26 Advanced Analytics System"
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv_n26" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Run: python -m venv venv_n26 && source venv_n26/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_n26/bin/activate

# Check for GUI or dashboard mode
if [ "$1" = "dashboard" ]; then
    echo "📊 Starting Advanced Analytics Dashboard..."
    python analytics_dashboard.py
elif [ "$1" = "demo" ]; then
    echo "🎯 Running complete demo..."
    python run_complete_demo.py
elif [ "$1" = "validate" ]; then
    echo "✅ Running system validation..."
    python final_validation.py
else
    echo "🖥️ Starting N26 GUI (with Advanced Analytics)..."
    python gui.py
fi

echo "👋 Shutting down N26 Advanced Analytics System"
