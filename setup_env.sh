#!/bin/bash
# Setup script for SQUAREQ virtual environment

echo "🚀 Setting up SQUAREQ environment..."

# Activate virtual environment
source venv/bin/activate

# Verify installation
echo "✅ Virtual environment activated"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Test imports
echo ""
echo "🧪 Testing imports..."
python -c "
import sys
sys.path.append('src')
try:
    from sac import SACAgent
    from environment import FixedQMetricsQuantumEnvironment
    from circuits import create_quantum_circuit_from_params
    print('✅ Core imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

echo ""
echo "✅ Setup complete! You can now:"
echo "   1. Activate the environment: source venv/bin/activate"
echo "   2. Start Jupyter: jupyter notebook or jupyter lab"
echo "   3. Select 'Python (SQUAREQ)' as your kernel"

