# GitHub Deployment Guide for SQUAREQ

This guide explains how to deploy SQUAREQ to GitHub and display notebook results.

## Quick Start

1. **Initialize Git repository:**
   ```bash
   cd SQUAREQ_GitHub
   git init
   git add .
   git commit -m "Initial commit: SQUAREQ project"
   ```

2. **Create GitHub repository:**
   - Go to GitHub.com
   - Click "New repository"
   - Name it (e.g., "SQUAREQ")
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/SQUAREQ.git
   git branch -M main
   git push -u origin main
   ```

## Displaying Notebooks on GitHub

GitHub automatically renders Jupyter notebooks. However, for best results:

### Option 1: GitHub Native Rendering (Recommended)
- GitHub automatically renders `.ipynb` files
- Notebooks with saved outputs will display with results
- Just commit the notebooks with their outputs

### Option 2: nbviewer (For Better Rendering)
- Go to https://nbviewer.org/
- Paste your GitHub notebook URL:
  ```
  https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb
  ```
- nbviewer will render it with all outputs

### Option 3: GitHub Pages with Jupyter Book
For a more polished documentation site, you can use Jupyter Book (optional).

## Ensuring Notebooks Display Results

To make sure notebooks show results on GitHub:

1. **Run notebooks and save outputs:**
   ```bash
   # Activate environment
   source venv/bin/activate
   
   # Start Jupyter
   jupyter notebook
   ```

2. **In Jupyter:**
   - Run all cells (Cell → Run All)
   - Save the notebook (File → Save)
   - The outputs will be saved in the notebook file

3. **Commit notebooks with outputs:**
   ```bash
   git add notebooks/*.ipynb
   git commit -m "Add notebooks with execution results"
   git push
   ```

## Repository Structure

Your GitHub repository should have:
```
SQUAREQ/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── bronze.csv
│   └── earthquake_alert_balanced_dataset.csv
├── src/
│   ├── sac/
│   ├── environment/
│   ├── circuits/
│   └── utils.py
├── notebooks/
│   ├── 01_Earthquake_Binary_Classification.ipynb
│   └── 02_Earthquake_Multi_Classification.ipynb
└── results/
    └── comprehensive_quantum_analysis_20250929_164609.pdf
```

## Adding Badges (Optional)

Add these to your README.md for a professional look:

```markdown
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Qiskit](https://img.shields.io/badge/qiskit-0.45+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

## Continuous Integration

The `.github/workflows/notebook-tests.yml` file will automatically test your code on push.

## Viewing Notebooks

Once deployed, notebooks can be viewed at:
- `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`
- Or via nbviewer: `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`

