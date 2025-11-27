#!/usr/bin/env python3
"""
Utility functions for SQUAREQ
- Feature selection
- Data loading and preprocessing
"""

import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import mutual_info_classif, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from qiskit.quantum_info import Statevector


def perform_feature_selection(X, y, feature_names=None, n_features=6):
    """
    Perform feature selection using multiple methods (MI, F-test, RF) with voting
    
    Args:
        X: Feature matrix
        y: Target vector
        feature_names: Optional list of feature names
        n_features: Number of features to select
    
    Returns:
        selected_indices: Indices of selected features
        selected_names: Names of selected features (if feature_names provided)
    """
    # Method 1: Mutual Information
    mi_scores = mutual_info_classif(X, y, random_state=42)
    mi_indices = np.argsort(mi_scores)[-n_features:]
    
    # Method 2: F-test
    f_scores, _ = f_classif(X, y)
    f_indices = np.argsort(f_scores)[-n_features:]
    
    # Method 3: Random Forest Feature Importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    rf_importance = rf.feature_importances_
    rf_indices = np.argsort(rf_importance)[-n_features:]
    
    # Combine methods (voting)
    all_indices = np.concatenate([mi_indices, f_indices, rf_indices])
    unique, counts = np.unique(all_indices, return_counts=True)
    selected_indices = unique[np.argsort(counts)[-n_features:]]
    
    if feature_names is not None:
        selected_names = [feature_names[i] for i in selected_indices]
        return selected_indices, selected_names
    
    return selected_indices


def load_earthquake_binary_data(data_path='../data/bronze.csv', n_samples=500):
    """
    Load and preprocess earthquake data for binary classification (high/low magnitude)
    
    Args:
        data_path: Path to bronze.csv
        n_samples: Number of samples to use
    
    Returns:
        X: Feature matrix (6 features after selection)
        y: Binary target (1 = high magnitude >= 6.0, 0 = low magnitude)
        selected_features: List of selected feature names
    """
    df = pd.read_csv(data_path)
    
    # Preprocess
    essential_features = ['latitude', 'longitude', 'mag']
    df_clean = df[essential_features + ['depth', 'gap', 'rms', 'magType']].dropna(subset=essential_features)
    
    for col in ['depth', 'gap', 'rms']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    df_clean['magType'] = df_clean['magType'].fillna('unknown')
    df_clean['high_magnitude'] = (df_clean['mag'] >= 6.0).astype(int)
    
    le_magType = LabelEncoder()
    df_clean['magType_encoded'] = le_magType.fit_transform(df_clean['magType'].astype(str))
    
    # All available features
    all_features = ['latitude', 'longitude', 'depth', 'gap', 'rms', 'magType_encoded']
    X_all = df_clean[all_features].values
    y_all = df_clean['high_magnitude'].values
    
    # Feature selection
    selected_indices, selected_names = perform_feature_selection(
        X_all, y_all, feature_names=all_features, n_features=6
    )
    X_selected = X_all[:, selected_indices]
    
    # Sample if needed
    if n_samples and n_samples < len(X_selected):
        X_selected, _, y_all, _ = train_test_split(
            X_selected, y_all, train_size=n_samples, random_state=42, stratify=y_all
        )
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    
    return X_scaled, y_all, selected_names


def load_earthquake_alert_data(data_path='../data/earthquake_alert_balanced_dataset 2.csv'):
    """
    Load and preprocess earthquake alert data for multi-classification
    
    Args:
        data_path: Path to alert dataset
    
    Returns:
        X: Feature matrix (6 features after selection)
        y: Multi-class target (encoded alert types)
        selected_features: List of selected feature names
        label_encoder: LabelEncoder for alert types
    """
    df = pd.read_csv(data_path)
    
    # Feature engineering
    df['sig_abs'] = df['sig'].abs()
    df['depth_mag_ratio'] = df['depth'] / (df['magnitude'] + 1e-6)
    df['mmi_minus_cdi'] = df['mmi'] - df['cdi']
    df['intensity_product'] = df['mmi'] * df['cdi']
    
    feature_cols = ['magnitude', 'depth', 'cdi', 'mmi', 'sig', 'sig_abs', 
                    'depth_mag_ratio', 'mmi_minus_cdi', 'intensity_product']
    X_raw = df[feature_cols].values
    
    # Encode target
    le = LabelEncoder()
    y_raw = le.fit_transform(df['alert'].astype(str))
    
    # Feature selection
    selected_indices, selected_names = perform_feature_selection(
        X_raw, y_raw, feature_names=feature_cols, n_features=6
    )
    X_selected = X_raw[:, selected_indices]
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    
    return X_scaled, y_raw, selected_names, le


def train_multiclass_quantum_qsvc(X_train, y_train, X_val, y_val, X_test, y_test, params):
    """
    Train multi-class QSVC using precomputed kernel matrix
    (Workaround for Qiskit ML multi-class support)
    """
    from squareq_core import create_quantum_circuit_from_params
    
    qc, param_list = create_quantum_circuit_from_params(
        params['theta_values'],
        params['gate_types'],
        params['num_qubits'],
        params['threshold'],
        params['entanglement_strength']
    )
    
    # Generate quantum states
    def _generate_states(qc_template, params_list, X_data):
        states = []
        for sample in X_data:
            bind_dict = {params_list[i]: sample[i] for i in range(len(sample))}
            bound = qc_template.assign_parameters(bind_dict, inplace=False)
            state = Statevector(bound)
            states.append(state)
        return states
    
    # Compute kernel matrix
    def _compute_kernel_matrix(states_a, states_b):
        mat = np.zeros((len(states_a), len(states_b)))
        for i, sa in enumerate(states_a):
            for j, sb in enumerate(states_b):
                mat[i, j] = np.abs(sa.data.conj().dot(sb.data)) ** 2
        return mat
    
    train_states = _generate_states(qc, param_list, X_train)
    val_states = _generate_states(qc, param_list, X_val)
    test_states = _generate_states(qc, param_list, X_test)
    
    K_train = _compute_kernel_matrix(train_states, train_states)
    K_val = _compute_kernel_matrix(val_states, train_states)
    K_test = _compute_kernel_matrix(test_states, train_states)
    
    # Use SVC with precomputed kernel for multi-class
    qsvc = SVC(kernel='precomputed', decision_function_shape='ovr', random_state=42)
    start = time.time()
    qsvc.fit(K_train, y_train)
    train_time = time.time() - start
    
    y_train_pred = qsvc.predict(K_train)
    val_start = time.time()
    y_val_pred = qsvc.predict(K_val)
    val_time = time.time() - val_start
    test_start = time.time()
    y_test_pred = qsvc.predict(K_test)
    test_time = time.time() - test_start
    
    metrics = {}
    for split_name, y_true, y_pred in [
        ('train', y_train, y_train_pred),
        ('val', y_val, y_val_pred),
        ('test', y_test, y_test_pred)
    ]:
        acc = accuracy_score(y_true, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
        metrics[f'{split_name}_accuracy'] = acc
        metrics[f'{split_name}_precision'] = prec
        metrics[f'{split_name}_recall'] = rec
        metrics[f'{split_name}_f1'] = f1
    
    metrics['train_time'] = train_time
    metrics['val_predict_time'] = val_time
    metrics['test_predict_time'] = test_time
    metrics['classification_report'] = classification_report(y_test, y_test_pred, zero_division=0)
    metrics['model'] = qsvc
    return metrics

