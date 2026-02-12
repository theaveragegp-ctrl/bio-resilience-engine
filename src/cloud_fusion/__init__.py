"""
Cloud Fusion Module for Bio-Resilience Engine.

Multi-modal sensor fusion backend with Bayesian state estimation
and predictive physiological analytics.

Author: Dr. Maya Anderson
Date: 2024-01-22
"""

__version__ = "0.4.2"

from .bayesian_fusion import BayesianFusion, PhysiologicalState
from .config import settings

__all__ = ["BayesianFusion", "PhysiologicalState", "settings"]
