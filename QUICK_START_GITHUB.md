# 🚀 Quick Start: Deploy to GitHub

## One-Command Setup (After creating GitHub repo)

```bash
# 1. Run notebooks and save outputs
./run_and_save_notebooks.sh

# 2. Initialize git and push
git init
git add .
git commit -m "Initial commit: SQUAREQ project"
git remote add origin https://github.com/YOUR_USERNAME/SQUAREQ.git
git branch -M main
git push -u origin main
```

## View Your Notebooks

After pushing, notebooks will be available at:

**GitHub (native rendering):**
- `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`
- `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/02_Earthquake_Multi_Classification.ipynb`

**nbviewer (better rendering - recommended):**
- `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`
- `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/02_Earthquake_Multi_Classification.ipynb`

## What Gets Displayed

✅ **Code cells** - All Python code  
✅ **Output cells** - Print statements, results  
✅ **Plots** - Matplotlib visualizations  
✅ **DataFrames** - Pandas tables  
✅ **Markdown** - Documentation and explanations  

## Tips

1. **Run all cells before committing** - Ensures outputs are saved
2. **Use nbviewer for best experience** - Better rendering than GitHub native
3. **Keep file sizes reasonable** - GitHub has 100MB limit per file
4. **Add repository topics** - Helps others find your work (quantum, machine-learning, reinforcement-learning, qiskit)

## Need Help?

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions.

