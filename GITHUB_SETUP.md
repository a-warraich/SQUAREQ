# Complete GitHub Setup Guide

## Step 1: Prepare Notebooks with Outputs

To display results on GitHub, notebooks need to have saved outputs:

### Option A: Run Script (Easiest)
```bash
chmod +x run_and_save_notebooks.sh
./run_and_save_notebooks.sh
```

### Option B: Manual (In Jupyter)
1. Activate environment: `source venv/bin/activate`
2. Start Jupyter: `jupyter notebook`
3. Open each notebook
4. Run all cells: `Cell → Run All`
5. Save: `File → Save`
6. Close Jupyter

## Step 2: Initialize Git Repository

```bash
cd SQUAREQ_GitHub

# Initialize git (if not already done)
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: SQUAREQ - SAC-optimized Quantum Support Vector Classifier"
```

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `SQUAREQ` (or your preferred name)
3. Description: "Soft Actor-Critic Optimized Quantum Support Vector Classifier"
4. Choose Public or Private
5. **Don't** initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"

## Step 4: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/SQUAREQ.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 5: View Notebooks on GitHub

Once pushed, your notebooks will be viewable at:

- **Binary Classification:**
  - GitHub: `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`
  - nbviewer: `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`

- **Multi-Classification:**
  - GitHub: `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/02_Earthquake_Multi_Classification.ipynb`
  - nbviewer: `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/02_Earthquake_Multi_Classification.ipynb`

## Displaying Results

### GitHub Native Rendering
- GitHub automatically renders `.ipynb` files
- Notebooks with saved outputs will show results inline
- Best for quick viewing

### nbviewer (Recommended for Best Experience)
- Better rendering of plots and outputs
- More reliable for complex notebooks
- Just paste your GitHub notebook URL

### Jupyter Book (Advanced - Optional)
For a full documentation site:
```bash
pip install jupyter-book
jupyter-book create docs/
# Follow jupyter-book documentation
```

## Repository Badges

Add these to your README for a professional look:

```markdown
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/qiskit-0.45+-blue.svg)](https://qiskit.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
```

## Continuous Integration

The `.github/workflows/notebook-tests.yml` workflow will:
- Automatically test imports on push
- Verify code structure
- Run on pull requests

## Troubleshooting

### Notebooks not showing outputs?
1. Make sure you ran all cells and saved
2. Check file size (GitHub has limits)
3. Try nbviewer for better rendering

### Large files?
- GitHub has a 100MB file limit
- Use Git LFS for large data files if needed
- Consider excluding large results files

### Authentication issues?
- Use SSH: `git@github.com:YOUR_USERNAME/SQUAREQ.git`
- Or use GitHub CLI: `gh repo create`

## Next Steps

1. ✅ Push to GitHub
2. ✅ Add repository description and topics
3. ✅ Enable GitHub Pages (optional)
4. ✅ Share your work!

