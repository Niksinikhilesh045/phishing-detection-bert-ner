#!/usr/bin/env python3
"""
Setup script for Phishing Email Detection System
"""

import os
import sys

from setuptools import find_packages, setup

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: This package requires Python 3.8 or higher.")
    sys.exit(1)


# Read long description from README
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return "AI-driven phishing email detection using BERT and Named Entity Recognition"


# Read requirements from requirements.txt
def read_requirements(filename="requirements.txt"):
    requirements = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-r"):
                    requirements.append(line)
    return requirements


setup(
    # Package metadata
    name="phishing-detection-bert-ner",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-driven phishing email detection using BERT and Named Entity Recognition",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Niksinikhilesh045/phishing-detection-bert-ner",
    project_urls={
        "Bug Tracker": "https://github.com/Niksinikhilesh045/phishing-detection-bert-ner/issues",
        "Documentation": "https://github.com/Niksinikhilesh045/phishing-detection-bert-ner/wiki",
    },
    # Package discovery - find packages in current directory
    packages=find_packages(include=["src", "src.*"]),
    package_dir={"": "."},
    # Python version requirement
    python_requires=">=3.8",
    # Dependencies
    install_requires=read_requirements(),
    # Optional dependencies
    extras_require={
        "dev": read_requirements("requirements-dev.txt")
        if os.path.exists("requirements-dev.txt")
        else [],
        "test": [
            "pytest>=7.1.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.8.0",
        ],
        "docs": [
            "sphinx>=5.1.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "api": [
            "fastapi>=0.85.0",
            "uvicorn>=0.18.0",
        ],
    },
    # Package classification
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Communications :: Email",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    # Keywords
    keywords="phishing detection, email security, BERT, NER, machine learning, cybersecurity",
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "phishing-detect=src.cli:main",
        ],
    },
    # Include non-Python files
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt", "*.md"],
        "src.config": ["*.yaml", "*.yml"],
    },
    # Zip safety
    zip_safe=False,
    # Additional metadata
    license="MIT",
    platforms=["any"],
)
