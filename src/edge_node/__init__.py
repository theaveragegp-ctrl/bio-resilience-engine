"""
Edge Node Module for Bio-Resilience Engine.

This package implements real-time pose estimation and activity classification
on NVIDIA Jetson edge devices with TensorRT optimization.

Author: Dr. Li Chen
Date: 2024-01-20
"""

__version__ = "0.4.2"

from .inference_pipeline import InferencePipeline, InferenceResult
from .activity_classifier import LSTMActivityClassifier
from .preprocessing import FramePreprocessor

__all__ = [
    "InferencePipeline",
    "InferenceResult",
    "LSTMActivityClassifier",
    "FramePreprocessor",
]
