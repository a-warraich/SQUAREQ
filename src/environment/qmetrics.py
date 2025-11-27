#!/usr/bin/env python3
"""Structure-based quantum metrics for reward calculation"""

import numpy as np
from scipy.stats import entropy
from collections import Counter
import networkx as nx
from sklearn.preprocessing import StandardScaler


class StructureBasedQuantumMetrics:
    """Structure-based quantum metrics for reward calculation"""
    
    def __init__(self, X, y, num_qubits):
        self.X = X
        self.y = y
        self.num_qubits = num_qubits
        
        # Precompute data statistics
        self.X_normalized = StandardScaler().fit_transform(X[:, :num_qubits])
        self.feature_correlations = np.corrcoef(self.X_normalized.T)
        self.class_centroids = {
            label: np.mean(self.X_normalized[self.y == label], axis=0) 
            for label in np.unique(self.y)
        }
        self.data_variance = np.var(self.X_normalized, axis=0)
        self.between_class_variance = self._compute_between_class_variance()
    
    def _compute_between_class_variance(self):
        centroids = np.array(list(self.class_centroids.values()))
        return np.var(centroids, axis=0)
    
    def quantum_locality_ratio(self, circuit_structure):
        single_qubit_gates = sum(1 for gate in circuit_structure if gate['num_qubits'] == 1)
        total_gates = len(circuit_structure)
        return single_qubit_gates / total_gates if total_gates > 0 else 0.0
    
    def parameter_expressivity_proxy(self, theta_values):
        if len(theta_values) == 0:
            return 0.0
            
        param_std = np.std(theta_values)
        param_mean = np.mean(np.abs(theta_values))
        diversity = param_std / (param_mean + 1e-8)
        
        optimal_magnitude = np.pi / 2
        magnitude_scores = [np.exp(-2 * ((abs(theta) - optimal_magnitude) / optimal_magnitude)**2) 
                          for theta in theta_values]
        magnitude_quality = np.mean(magnitude_scores)
        
        param_entropy = entropy(np.abs(theta_values) + 1e-8)
        max_entropy = np.log(len(theta_values))
        balance = param_entropy / max_entropy if max_entropy > 0 else 0
        
        return 0.4 * diversity + 0.35 * magnitude_quality + 0.25 * balance
    
    def gate_type_diversity(self, gate_types):
        if len(gate_types) == 0:
            return 0.0
            
        gate_indices = [int((g + 1) * 1.5) % 3 for g in gate_types]
        unique_gates = len(set(gate_indices))
        max_possible = min(3, len(gate_types))
        
        gate_counts = Counter(gate_indices)
        uniformity = 1.0 - np.std(list(gate_counts.values())) / (np.mean(list(gate_counts.values())) + 1e-8)
        
        diversity_ratio = unique_gates / max_possible
        return 0.7 * diversity_ratio + 0.3 * uniformity
    
    def entanglement_capability_proxy(self, theta_values, circuit_structure):
        if len(theta_values) < 2:
            return 0.0
        
        entanglement_strength = 0
        cnot_count = sum(1 for gate in circuit_structure if gate['type'] == 'cnot')
        
        for i in range(len(theta_values) - 1):
            param_product = abs(theta_values[i] * theta_values[i + 1])
            optimal_product = (np.pi / 3) ** 2
            strength = np.exp(-((param_product - optimal_product) / optimal_product)**2)
            entanglement_strength += strength
        
        if len(theta_values) > 1:
            entanglement_strength /= (len(theta_values) - 1)
        
        connectivity_ratio = cnot_count / max(1, len(theta_values))
        connectivity_score = min(1.0, connectivity_ratio)
        
        pattern_quality = self._evaluate_entanglement_pattern(circuit_structure)
        
        return 0.5 * entanglement_strength + 0.3 * connectivity_score + 0.2 * pattern_quality
    
    def _evaluate_entanglement_pattern(self, circuit_structure):
        G = nx.Graph()
        G.add_nodes_from(range(self.num_qubits))
        
        for gate in circuit_structure:
            if gate['type'] == 'cnot' and len(gate['qubits']) == 2:
                G.add_edge(gate['qubits'][0], gate['qubits'][1])
        
        if G.number_of_edges() == 0:
            return 0.0
        
        connectivity = 1.0 if nx.is_connected(G) else 0.5
        
        max_edges = self.num_qubits * (self.num_qubits - 1) // 2
        edge_ratio = G.number_of_edges() / max_edges
        over_entanglement_penalty = np.exp(-2 * (edge_ratio - 0.3)**2)
        
        return 0.6 * connectivity + 0.4 * over_entanglement_penalty
    
    def data_encoding_alignment(self, theta_values, gate_types):
        if len(theta_values) == 0:
            return 0.0
        
        variance_alignment = 0
        for i, theta in enumerate(theta_values[:len(self.data_variance)]):
            feature_importance = self.data_variance[i] + self.between_class_variance[i]
            optimal_theta = np.sqrt(feature_importance) * np.pi / 2
            alignment = np.exp(-((abs(theta) - optimal_theta) / (optimal_theta + 1e-8))**2)
            variance_alignment += alignment
        
        if len(theta_values) > 0:
            variance_alignment /= min(len(theta_values), len(self.data_variance))
        
        correlation_match = 0
        param_pairs = 0
        for i in range(len(theta_values)):
            for j in range(i + 1, len(theta_values)):
                if i < self.feature_correlations.shape[0] and j < self.feature_correlations.shape[1]:
                    feature_corr = abs(self.feature_correlations[i, j])
                    param_corr = abs(theta_values[i] * theta_values[j]) / (np.pi**2 / 4)
                    match = 1 - abs(feature_corr - np.tanh(param_corr))
                    correlation_match += match
                    param_pairs += 1
        
        if param_pairs > 0:
            correlation_match /= param_pairs
        
        gate_appropriateness = 0
        for i, gate_type in enumerate(gate_types[:len(self.data_variance)]):
            gate_idx = int((gate_type + 1) * 1.5) % 3
            variance = self.data_variance[i]
            
            if variance > np.percentile(self.data_variance, 66):
                appropriateness = 1.0 if gate_idx == 1 else 0.5
            elif variance < np.percentile(self.data_variance, 33):
                appropriateness = 1.0 if gate_idx == 2 else 0.5
            else:
                appropriateness = 1.0 if gate_idx == 0 else 0.7
            
            gate_appropriateness += appropriateness
        
        if len(gate_types) > 0:
            gate_appropriateness /= min(len(gate_types), len(self.data_variance))
        
        return 0.4 * variance_alignment + 0.35 * correlation_match + 0.25 * gate_appropriateness
    
    def quantum_volume_proxy(self, circuit_depth):
        if circuit_depth == 0:
            return 0.0
        return min(1.0, 4 * self.num_qubits / (self.num_qubits * circuit_depth))
    
    def separability_enhancement_proxy(self, theta_values):
        if len(theta_values) == 0 or len(self.class_centroids) < 2:
            return 0.0
        
        class_means = np.array(list(self.class_centroids.values()))
        class_diff = class_means[0] - class_means[1] if len(class_means) >= 2 else np.zeros_like(class_means[0])
        
        separability_alignment = 0
        for i, theta in enumerate(theta_values[:len(class_diff)]):
            feature_separability = abs(class_diff[i])
            alignment = feature_separability * abs(theta)
            separability_alignment += alignment
        
        max_possible = np.sum(np.abs(class_diff)) * np.sum(np.abs(theta_values[:len(class_diff)]))
        return separability_alignment / (max_possible + 1e-8)
    
    def circuit_complexity_penalty(self, circuit_structure, theta_values):
        gate_count = len(circuit_structure)
        param_count = len(theta_values)
        two_qubit_gates = sum(1 for gate in circuit_structure if gate['num_qubits'] == 2)
        
        gate_density = gate_count / self.num_qubits
        param_density = param_count / self.num_qubits  
        entangling_density = two_qubit_gates / self.num_qubits
        
        complexity = 0.4 * gate_density + 0.3 * param_density + 0.3 * entangling_density
        return min(1.0, complexity / 10.0)
    
    def compute_harmonic_mean_reward(self, theta_values, gate_types, circuit_structure, circuit_depth):
        locality = self.quantum_locality_ratio(circuit_structure)
        expressivity = self.parameter_expressivity_proxy(theta_values)
        gate_diversity = self.gate_type_diversity(gate_types)
        entanglement = self.entanglement_capability_proxy(theta_values, circuit_structure)
        data_alignment = self.data_encoding_alignment(theta_values, gate_types)
        volume_proxy = self.quantum_volume_proxy(circuit_depth)
        separability = self.separability_enhancement_proxy(theta_values)
        complexity_penalty = self.circuit_complexity_penalty(circuit_structure, theta_values)
        
        metrics = [
            1 - locality,
            expressivity,
            gate_diversity,
            entanglement,
            data_alignment,
            volume_proxy,
            separability,
            1 - complexity_penalty
        ]
        
        metrics = [max(m, 1e-6) for m in metrics]
        harmonic_mean = len(metrics) / sum(1/m for m in metrics)
        
        return {
            'reward': harmonic_mean,
            'components': {
                'non_locality': 1 - locality,
                'expressivity': expressivity,
                'gate_diversity': gate_diversity, 
                'entanglement': entanglement,
                'data_alignment': data_alignment,
                'volume_proxy': volume_proxy,
                'separability': separability,
                'low_complexity': 1 - complexity_penalty
            }
        }

