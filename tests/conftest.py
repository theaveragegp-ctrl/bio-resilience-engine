"""
Pytest configuration and shared fixtures.

Provides common test fixtures and configuration for the test suite.

Author: Dr. Li Chen
Date: 2024-01-27
"""

import pytest
import numpy as np
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_video_frame():
    """Generate sample video frame for testing."""
    return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)


@pytest.fixture
def sample_keypoints():
    """Generate sample pose keypoints (17x3 array)."""
    return np.random.rand(17, 3) * np.array([640, 480, 1])


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
