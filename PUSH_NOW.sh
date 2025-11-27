#!/bin/bash
# Quick push script - just provide your GitHub username

echo "🚀 Quick GitHub Push for SQUAREQ"
echo ""

if [ -z "$1" ]; then
    echo "Usage: ./PUSH_NOW.sh YOUR_GITHUB_USERNAME [REPO_NAME]"
    echo ""
    echo "Example: ./PUSH_NOW.sh johndoe"
    echo "Example: ./PUSH_NOW.sh johndoe my-quantum-project"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=${2:-SQUAREQ}

echo "📝 Configuration:"
echo "   Username: $GITHUB_USERNAME"
echo "   Repository: $REPO_NAME"
echo ""

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists"
    echo "   Current: $(git remote get-url origin)"
    echo ""
    read -p "Overwrite? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "Cancelled. Use: git remote set-url origin <new-url>"
        exit 1
    fi
fi

# Add remote
echo "🔗 Adding remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Ensure main branch
git branch -M main 2>/dev/null

echo ""
echo "⚠️  IMPORTANT: Create the repository on GitHub first!"
echo ""
echo "   1. Go to: https://github.com/new"
echo "   2. Repository name: $REPO_NAME"
echo "   3. Description: 'SAC-optimized Quantum Support Vector Classifier'"
echo "   4. Choose Public or Private"
echo "   5. DO NOT initialize with README, .gitignore, or license"
echo "   6. Click 'Create repository'"
echo ""
read -p "Press Enter when repository is created..."

# Push
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Repository pushed to GitHub!"
    echo ""
    echo "📊 View your notebooks:"
    echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb"
    echo "   https://nbviewer.org/github/$GITHUB_USERNAME/$REPO_NAME/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb"
else
    echo ""
    echo "❌ Push failed. Try:"
    echo "   1. Check repository exists: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "   2. Use GitHub CLI: gh auth login && gh repo create $REPO_NAME --public --source=. --push"
    echo "   3. Or use SSH: git remote set-url origin git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
fi

