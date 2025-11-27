#!/bin/bash
# Script to prepare SQUAREQ for GitHub deployment

echo "🚀 Preparing SQUAREQ for GitHub deployment..."

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Must run from SQUAREQ_GitHub directory"
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if notebooks have outputs
echo ""
echo "📓 Checking notebooks..."
for notebook in notebooks/*.ipynb; do
    if [ -f "$notebook" ]; then
        # Check if notebook has outputs
        if python3 -c "import json; nb = json.load(open('$notebook')); outputs = sum(len(c.get('outputs', [])) for c in nb['cells'] if c['cell_type'] == 'code'); print(f'{notebook}: {outputs} outputs')" 2>/dev/null; then
            echo "  ✅ $notebook has outputs"
        else
            echo "  ⚠️  $notebook may not have outputs - run it in Jupyter first"
        fi
    fi
done

echo ""
echo "📋 Next steps:"
echo "1. Review .gitignore to ensure sensitive files are excluded"
echo "2. Run notebooks in Jupyter and save with outputs:"
echo "   source venv/bin/activate"
echo "   jupyter notebook"
echo "   (Then: Cell → Run All, File → Save)"
echo "3. Commit and push:"
echo "   git add ."
echo "   git commit -m 'Initial commit: SQUAREQ project'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/SQUAREQ.git"
echo "   git push -u origin main"
echo ""
echo "✅ Preparation complete!"

