# SQUAREQ: Soft Actor-Critic Optimized Quantum Support Vector Classifier

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/qiskit-0.45+-blue.svg)](https://qiskit.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

SQUAREQ is a reinforcement learning-based approach for optimizing quantum machine learning circuits using Soft Actor-Critic (SAC) and structure-based quantum metrics (QMetrics).

## 📊 View Notebooks

- **[Binary Classification Notebook](notebooks/01_Earthquake_Binary_Classification.ipynb)** - Compare SQUAREQ, ZZFeatureMap, and Classical SVC
- **[Multi-Classification Notebook](notebooks/02_Earthquake_Multi_Classification.ipynb)** - Earthquake alert type prediction

*Note: For best viewing experience, use [nbviewer](https://nbviewer.org/) or open notebooks in Jupyter.*

## Overview

This project implements a quantum support vector classifier (QSVC) optimized through reinforcement learning. The SAC agent learns to design quantum circuits that maximize quantum metrics such as expressivity, entanglement, data alignment, and separability.

### Key Features

- **SAC-Optimized Quantum Circuits**: Uses Soft Actor-Critic RL to optimize quantum circuit parameters
- **Structure-Based Quantum Metrics**: Evaluates circuits based on 8 QMetrics components
- **Multi-Method Feature Selection**: Combines Mutual Information, F-test, and Random Forest importance
- **Comprehensive Comparisons**: Benchmarks against ZZFeatureMap QSVC and classical SVC

## Project Structure

```
SQUAREQ_GitHub/
├── data/                          # Dataset files
│   ├── bronze.csv                 # Earthquake binary classification data
│   └── earthquake_alert_balanced_dataset.csv  # Multi-class alert data
├── src/                           # Core source code
│   ├── __init__.py
│   ├── squareq_core.py           # SAC agent, QMetrics, environment
│   └── utils.py                   # Feature selection, data loading
├── notebooks/                     # Jupyter notebooks
│   ├── 01_Earthquake_Binary_Classification.ipynb
│   └── 02_Earthquake_Multi_Classification.ipynb
├── results/                       # Analysis results and PDFs
└── README.md
```

## Installation

### Quick Setup (Recommended)

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Register Jupyter kernel (optional, for notebook support):**
   ```bash
   python -m ipykernel install --user --name=squareq --display-name "Python (SQUAREQ)"
   ```

4. **Verify installation:**
   ```bash
   ./setup_env.sh  # or source setup_env.sh
   ```

### Manual Installation

If you prefer to install manually:

```bash
pip install numpy pandas scikit-learn torch qiskit qiskit-machine-learning qiskit-aer matplotlib scipy networkx jupyter ipykernel
```

### Optional (for IBM Quantum)

```bash
pip install qiskit-ibm-runtime
```

### Using the Environment

**Activate the environment:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Or use the quick activation script:**
```bash
source activate_env.sh
```

**Start Jupyter:**
```bash
jupyter notebook
# or
jupyter lab
```

**Select the kernel:** When creating/opening a notebook, select "Python (SQUAREQ)" as the kernel.

## Quick Start

### 1. Binary Classification (Earthquake Magnitude)

Run the notebook `01_Earthquake_Binary_Classification.ipynb` to compare:
- SQUAREQ (SAC-optimized QSVC)
- ZZFeatureMap QSVC
- Classical SVC (RBF kernel)

**Expected Results:**
- SQUAREQ typically achieves ~99% accuracy on earthquake magnitude prediction
- Faster training than ZZFeatureMap variants
- Comparable or better accuracy than classical SVC

### 2. Multi-Classification (Earthquake Alert Types)

Run the notebook `02_Earthquake_Multi_Classification.ipynb` to compare:
- SQUAREQ (SAC-optimized QSVC)
- Classical SVC (RBF kernel)

**Expected Results:**
- Classical SVC typically outperforms QSVC on multi-class tasks
- QSVC shows less overfitting but lower absolute accuracy

## Methodology

### Feature Selection

Uses a consensus voting approach combining:
1. **Mutual Information**: Measures non-linear dependencies
2. **F-test**: Statistical significance of features
3. **Random Forest Importance**: Tree-based feature importance

Top 6 features are selected based on voting across all three methods.

### SAC Training

- **Episodes**: 100
- **Steps per episode**: 5
- **State space**: Feature means + correlations + threshold (num_qubits × 2 + 1)
- **Action space**: Threshold + theta values + gate types + entanglement strength (num_qubits × 3 + 1)
- **Reward**: Harmonic mean of 8 QMetrics components

### QMetrics Components

1. **Non-locality**: Ratio of single-qubit to multi-qubit gates
2. **Expressivity**: Parameter diversity and magnitude quality
3. **Gate Diversity**: Variety of gate types (RX, RY, RZ)
4. **Entanglement**: CNOT connectivity and pattern quality
5. **Data Alignment**: Alignment with data variance and correlations
6. **Volume Proxy**: Circuit depth efficiency
7. **Separability**: Class separation enhancement
8. **Low Complexity**: Penalty for excessive circuit complexity

## Results Summary

### Binary Classification (Earthquake Magnitude)

| Model | Train Acc | Val Acc | Test Acc | Training Time |
|-------|----------|---------|----------|---------------|
| SQUAREQ | ~0.99 | ~0.99 | ~0.99 | ~30-50s |
| ZZFeatureMap | ~0.99 | ~0.99 | ~0.99 | ~120-200s |
| Classical SVC | ~0.93 | ~0.93 | ~0.93 | ~0.01s |

### Multi-Classification (Alert Types)

| Model | Train Acc | Val Acc | Test Acc | Training Time |
|-------|----------|---------|----------|---------------|
| SQUAREQ | ~0.71 | ~0.69 | ~0.67 | ~0.00s |
| Classical SVC | ~0.75 | ~0.67 | ~0.73 | ~0.01s |

## Key Findings

1. **SQUAREQ Efficiency**: SAC-optimized circuits are 4-11x faster than ZZFeatureMap while maintaining accuracy
2. **No Overfitting**: QSVC models show minimal overfitting compared to classical models
3. **Binary vs Multi-class**: Quantum advantage more pronounced in binary classification tasks
4. **Feature Selection**: Multi-method consensus voting selects robust features

## Usage Example

```python
from src import (
    load_earthquake_binary_data,
    FixedQMetricsQuantumEnvironment,
    SACAgent,
    create_quantum_circuit_from_params
)
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC

# Load data
X, y, features = load_earthquake_binary_data('data/bronze.csv', n_samples=500)

# Train SAC
env = FixedQMetricsQuantumEnvironment(X, y, num_qubits=6)
agent = SACAgent(env.state_dim, env.action_dim)

# ... training loop ...

# Create optimized circuit
qc = create_quantum_circuit_from_params(
    best_params['theta_values'],
    best_params['gate_types'],
    num_qubits=6,
    threshold=best_params['threshold'],
    entanglement_strength=best_params['entanglement_strength']
)

# Train QSVC
kernel = FidelityQuantumKernel(feature_map=qc)
qsvc = QSVC(quantum_kernel=kernel)
qsvc.fit(X_train, y_train)
```

## Citation

If you use SQUAREQ in your research, please cite:

```
SQUAREQ: Soft Actor-Critic Optimized Quantum Support Vector Classifier
```

## 📦 Deployment to GitHub

### Quick Setup

1. **Run notebooks and save outputs:**
   ```bash
   ./run_and_save_notebooks.sh
   ```

2. **Initialize and push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SQUAREQ project"
   git remote add origin https://github.com/YOUR_USERNAME/SQUAREQ.git
   git branch -M main
   git push -u origin main
   ```

### Viewing Notebooks

Once deployed, notebooks are viewable at:
- **GitHub:** `https://github.com/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`
- **nbviewer (better rendering):** `https://nbviewer.org/github/YOUR_USERNAME/SQUAREQ/blob/main/notebooks/01_Earthquake_Binary_Classification.ipynb`

### Detailed Instructions

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for complete deployment guide including:
- Setting up the GitHub repository
- Displaying notebooks with results
- Using nbviewer for better rendering
- Setting up CI/CD
- Troubleshooting

## 📄 License

This project is provided as-is for research and educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or issues, please open an issue on the repository.

