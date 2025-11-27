#!/usr/bin/env python3
"""Quantum circuit creation utilities"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector


def create_circuit_structure_from_action(theta_values, gate_types, num_qubits, threshold, entanglement_strength):
    """Create circuit structure representation from action parameters"""
    circuit_structure = []
    
    for i, (theta, gate_type) in enumerate(zip(theta_values, gate_types)):
        gate_idx = int((gate_type + 1) * 1.5) % 3
        gate_names = ['rx', 'ry', 'rz']
        
        circuit_structure.append({
            'type': gate_names[gate_idx],
            'qubits': [i % num_qubits],
            'num_qubits': 1,
            'parameter': theta
        })
    
    for i in range(num_qubits - 1):
        prob = threshold
        if i < len(entanglement_strength):
            prob *= (1 + entanglement_strength[i])
        prob = min(prob, 1.0)
        
        if np.random.random() < prob:
            circuit_structure.append({
                'type': 'cnot',
                'qubits': [i, i + 1],
                'num_qubits': 2
            })
    
    return circuit_structure


def create_quantum_circuit_from_params(theta_values, gate_types, num_qubits, threshold, entanglement_strength):
    """Create Qiskit QuantumCircuit from SAC-optimized parameters"""
    x = ParameterVector('x', num_qubits)
    qc = QuantumCircuit(num_qubits)
    
    for i, (theta_val, gate_type) in enumerate(zip(theta_values, gate_types)):
        gate_idx = int((gate_type + 1) * 1.5) % 3
        if gate_idx == 0:
            qc.rx(x[i] * theta_val, i)
        elif gate_idx == 1:
            qc.ry(x[i] * theta_val, i)
        else:
            qc.rz(x[i] * theta_val, i)
    
    for i in range(num_qubits - 1):
        prob = threshold
        if i < len(entanglement_strength):
            prob *= (1 + entanglement_strength[i])
        prob = min(prob, 1.0)
        if np.random.random() < prob:
            qc.cx(i, i + 1)
    
    return qc

