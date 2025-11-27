#!/bin/bash
# Simple push script - just provide GitHub username

if [ -z "$1" ]; then
    echo "Usage: ./SIMPLE_PUSH.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

USERNAME=$1
REPO_NAME=${2:-SQUAREQ}

echo "🚀 Pushing SQUAREQ to GitHub..."

# Remove existing remote if any
git remote remove origin 2>/dev/null

# Add remote
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
git branch -M main

echo ""
echo "📤 Pushing..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Done! View at: https://github.com/$USERNAME/$REPO_NAME"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. Repository exists: https://github.com/$USERNAME/$REPO_NAME"
    echo "   2. You're authenticated (use GitHub CLI: gh auth login)"
fi

