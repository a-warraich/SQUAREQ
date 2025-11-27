"""SQUAREQ: Soft Actor-Critic Optimized Quantum Support Vector Classifier"""

from .sac import SACAgent
from .environment import FixedQMetricsQuantumEnvironment, StructureBasedQuantumMetrics
from .circuits import create_quantum_circuit_from_params, create_circuit_structure_from_action
from .utils import (
    perform_feature_selection,
    load_earthquake_binary_data,
    load_earthquake_alert_data
)

__version__ = "1.0.0"

