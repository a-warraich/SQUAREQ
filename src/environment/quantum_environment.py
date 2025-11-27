#!/usr/bin/env python3
"""RL Environment for quantum circuit optimization"""

import numpy as np
from .qmetrics import StructureBasedQuantumMetrics

# Handle import for both relative and absolute cases
try:
    from ..circuits.circuit_utils import create_circuit_structure_from_action
except ImportError:
    from circuits.circuit_utils import create_circuit_structure_from_action


class FixedQMetricsQuantumEnvironment:
    """RL Environment for quantum circuit optimization using QMetrics"""
    
    def __init__(self, X, y, num_qubits=6):
        self.X = X
        self.y = y
        self.num_qubits = num_qubits
        self.state_dim = num_qubits * 2 + 1
        self.action_dim = num_qubits * 3 + 1
        
        self.qmetrics = StructureBasedQuantumMetrics(X, y, num_qubits)
        self.X = (self.X - np.mean(self.X, axis=0)) / np.std(self.X, axis=0)
        
    def reset(self):
        """Reset environment and return initial state"""
        correlations = np.corrcoef(self.X.T)
        upper_tri = correlations[np.triu_indices_from(correlations, k=1)]
        
        feature_means = np.mean(self.X, axis=0)
        
        num_corr_needed = self.num_qubits
        if len(upper_tri) > num_corr_needed:
            upper_tri = upper_tri[:num_corr_needed]
        elif len(upper_tri) < num_corr_needed:
            upper_tri = np.pad(upper_tri, (0, num_corr_needed - len(upper_tri)), 'constant')
        
        state = np.concatenate([
            feature_means,
            upper_tri,
            [0.5]
        ])
        
        return state
    
    def step(self, action):
        """Execute action and return next state, reward, done"""
        threshold = (action[0] + 1) / 2
        theta_values = action[1:self.num_qubits+1]
        gate_types = action[self.num_qubits+1:self.num_qubits*2+1]
        entanglement_strength = action[self.num_qubits*2+1:]
        
        circuit_structure = create_circuit_structure_from_action(
            theta_values, gate_types, self.num_qubits, threshold, entanglement_strength
        )
        
        components = self.qmetrics.compute_harmonic_mean_reward(
            theta_values, gate_types, circuit_structure, circuit_depth=len(circuit_structure)
        )
        reward = components['reward']
        
        next_state = self.reset()
        
        return next_state, reward, True
        
    def get_reward_components(self, action):
        """Get detailed component scores for an action"""
        threshold = (action[0] + 1) / 2
        theta_values = action[1:self.num_qubits+1]
        gate_types = action[self.num_qubits+1:self.num_qubits*2+1]
        entanglement_strength = action[self.num_qubits*2+1:]
        
        circuit_structure = create_circuit_structure_from_action(
            theta_values, gate_types, self.num_qubits, threshold, entanglement_strength
        )
        components = self.qmetrics.compute_harmonic_mean_reward(
            theta_values, gate_types, circuit_structure, circuit_depth=len(circuit_structure)
        )
        return components

