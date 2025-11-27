#!/bin/bash
# Script to push SQUAREQ to GitHub

echo "🚀 Pushing SQUAREQ to GitHub..."
echo ""

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "✅ Remote 'origin' already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "   Current remote: $REMOTE_URL"
else
    echo "📝 Setting up GitHub remote..."
    echo ""
    echo "Please provide your GitHub username:"
    read -r GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ GitHub username required"
        exit 1
    fi
    
    echo ""
    echo "Repository name (default: SQUAREQ):"
    read -r REPO_NAME
    REPO_NAME=${REPO_NAME:-SQUAREQ}
    
    echo ""
    echo "🔗 Adding remote: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    
    echo ""
    echo "⚠️  IMPORTANT: Create the repository on GitHub first!"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Repository name: $REPO_NAME"
    echo "   3. Description: 'SAC-optimized Quantum Support Vector Classifier'"
    echo "   4. Choose Public or Private"
    echo "   5. DO NOT initialize with README, .gitignore, or license"
    echo "   6. Click 'Create repository'"
    echo ""
    echo "Press Enter when the repository is created..."
    read -r
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    echo "📌 Renaming branch to 'main'..."
    git branch -M main
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    REMOTE_URL=$(git remote get-url origin)
    REPO_PATH=$(echo "$REMOTE_URL" | sed 's/.*github.com[:/]\([^.]*\).*/\1/')
    echo "📊 View your notebooks at:"
    echo "   GitHub: https://github.com/$REPO_PATH/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb"
    echo "   nbviewer: https://nbviewer.org/github/$REPO_PATH/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb"
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   1. Repository doesn't exist on GitHub - create it first"
    echo "   2. Authentication required - use GitHub CLI or SSH keys"
    echo "   3. Wrong remote URL - check with: git remote -v"
fi

