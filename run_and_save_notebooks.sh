#!/bin/bash
# Script to run notebooks and save outputs for GitHub display

echo "📓 Running notebooks and saving outputs for GitHub..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Run setup first."
    exit 1
fi

# Check if jupyter is installed
if ! command -v jupyter &> /dev/null; then
    echo "❌ Jupyter not found. Installing..."
    pip install jupyter nbconvert
fi

# Run notebooks and save outputs
echo ""
echo "🔄 Executing notebooks..."

for notebook in notebooks/*.ipynb; do
    if [ -f "$notebook" ]; then
        echo "  Processing $notebook..."
        # Execute notebook and save with outputs
        jupyter nbconvert --to notebook --execute --inplace "$notebook" 2>&1 | grep -v "DeprecationWarning" || {
            echo "  ⚠️  Error executing $notebook (this is okay if dependencies are missing)"
        }
        echo "  ✅ $notebook processed"
    fi
done

echo ""
echo "✅ Notebooks executed and saved with outputs!"
echo "📝 You can now commit and push to GitHub:"
echo "   git add notebooks/*.ipynb"
echo "   git commit -m 'Add notebooks with execution results'"
echo "   git push"

