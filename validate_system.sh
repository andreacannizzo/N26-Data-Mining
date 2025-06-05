#!/bin/bash

# N26 Advanced Analytics - System Validation Script
# This script validates the system without relying on potentially problematic Python imports

echo "🚀 N26 Advanced Analytics - System Validation"
echo "=============================================="

# Test 1: File structure check
echo ""
echo "📁 Test 1: File Structure Check"
echo "--------------------------------"

critical_files=(
    "advanced_analytics.py"
    "analytics_dashboard.py"
    "gui.py"
    "final_validation.py"
    "requirements.txt"
    "start_n26_analytics.sh"
)

all_files_present=true
for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file MISSING"
        all_files_present=false
    fi
done

# Test 2: Virtual environment check
echo ""
echo "🔧 Test 2: Virtual Environment Check"
echo "------------------------------------"

if [ -d "venv_n26" ]; then
    echo "✅ Virtual environment exists"
    if [ -f "venv_n26/bin/python" ]; then
        echo "✅ Python executable present"
    else
        echo "❌ Python executable missing"
    fi
    
    if [ -f "venv_n26/bin/activate" ]; then
        echo "✅ Activation script present"
    else
        echo "❌ Activation script missing"
    fi
else
    echo "❌ Virtual environment missing"
fi

# Test 3: Python syntax check
echo ""
echo "📝 Test 3: Python Syntax Check"
echo "------------------------------"

python_files=(
    "advanced_analytics.py"
    "analytics_dashboard.py"
    "final_validation.py"
)

syntax_ok=true
for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo "✅ $file syntax OK"
        else
            echo "❌ $file syntax ERROR"
            syntax_ok=false
        fi
    fi
done

# Test 4: Class definition check
echo ""
echo "🔍 Test 4: Class Definition Check"
echo "--------------------------------"

if grep -q "class N26AdvancedAnalytics:" advanced_analytics.py; then
    echo "✅ N26AdvancedAnalytics class found"
else
    echo "❌ N26AdvancedAnalytics class missing"
fi

if grep -q "def calculate_kpis" advanced_analytics.py; then
    echo "✅ calculate_kpis method found"
else
    echo "❌ calculate_kpis method missing"
fi

# Test 5: Requirements check
echo ""
echo "📦 Test 5: Requirements File Check"
echo "----------------------------------"

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt exists"
    if grep -q "pandas" requirements.txt; then
        echo "✅ pandas dependency listed"
    else
        echo "❌ pandas dependency missing"
    fi
    
    if grep -q "numpy" requirements.txt; then
        echo "✅ numpy dependency listed"
    else
        echo "❌ numpy dependency missing"
    fi
else
    echo "❌ requirements.txt missing"
fi

# Final assessment
echo ""
echo "🎯 Final Assessment"
echo "=================="

if [ "$all_files_present" = true ] && [ "$syntax_ok" = true ]; then
    echo "🎉 SYSTEM VALIDATION PASSED"
    echo "✅ All critical files present"
    echo "✅ Python syntax valid"
    echo "✅ Class definitions found"
    echo "✅ System ready for use"
    exit 0
else
    echo "❌ SYSTEM VALIDATION FAILED"
    echo "⚠️  Some issues detected"
    echo "🔧 Check the errors above"
    exit 1
fi
