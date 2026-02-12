"""Setup script for Bio-Resilience Engine."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bio-resilience-engine",
    version="0.4.2",
    author="Bio-Resilience Technologies",
    author_email="info@bio-resilience.org",
    description="Real-time biosignal analysis and computer vision fusion platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bio-resilience/bio-resilience-engine",
    project_urls={
        "Bug Tracker": "https://github.com/bio-resilience/bio-resilience-engine/issues",
        "Documentation": "https://docs.bio-resilience.org",
        "Source Code": "https://github.com/bio-resilience/bio-resilience-engine",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=24.1.1",
            "ruff>=0.1.14",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
        ],
        "edge": [
            "jetson-stats>=4.2.6",
            # "tensorrt>=8.6.1.6",  # Requires NVIDIA JetPack
        ],
    },
    entry_points={
        "console_scripts": [
            "bio-resilience-edge=src.edge_node.main:main",
            "bio-resilience-api=src.cloud_fusion.main:main",
        ],
    },
)
