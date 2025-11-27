#!/bin/bash
# Quick activation script for SQUAREQ environment

source venv/bin/activate
echo "✅ SQUAREQ environment activated!"
echo "Python: $(python --version)"
echo ""
echo "To start Jupyter:"
echo "  jupyter notebook"
echo "  or"
echo "  jupyter lab"
echo ""
echo "Select 'Python (SQUAREQ)' as your kernel in the notebooks"

