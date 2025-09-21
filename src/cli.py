#!/usr/bin/env python3
"""
Command-line interface for Phishing Detection System
"""

import click
import sys
import os
from pathlib import Path

# Add project root to path to ensure imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import from src
try:
    from src.utils.logger import get_logger, setup_logging
except ImportError:
    # Fallback if logger not available yet
    import logging
    logging.basicConfig(level=logging.INFO)
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)

@click.group()
@click.version_option(version="0.1.0")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(verbose):
    """Phishing Email Detection System - BERT & NER powered email security"""
    if verbose:
        try:
            setup_logging(level="DEBUG")
        except:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose mode enabled")

@main.command()
@click.argument("email_file", type=click.Path(exists=True), required=False)
def predict(email_file):
    """Predict if an email is phishing or legitimate"""
    if email_file:
        logger.info(f"Analyzing email file: {email_file}")
        click.echo(f"Analyzing: {email_file}")
    else:
        click.echo("No email file provided.")
        click.echo("Usage: phishing-detect predict <email_file>")
    click.echo("Status: Not implemented yet - Part of Issue #11")

@main.command()
@click.option("--data-path", type=click.Path(), help="Path to training data")
@click.option("--epochs", default=3, help="Number of training epochs")
def train(data_path, epochs):
    """Train the phishing detection model"""
    logger.info(f"Starting training with data: {data_path}, epochs: {epochs}")
    click.echo(f"Training model with {epochs} epochs...")
    if data_path:
        click.echo(f"Using data from: {data_path}")
    click.echo("Status: Not implemented yet - Part of Issue #10")

@main.command()
def info():
    """Show system information"""
    click.echo("=== Phishing Detection System Info ===")
    click.echo(f"Python version: {sys.version}")
    
    # Check core dependencies
    try:
        import torch
        click.echo(f"PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            click.echo(f"CUDA available: {torch.cuda.get_device_name()}")
        else:
            click.echo("CUDA: Not available (using CPU)")
    except ImportError:
        click.echo("PyTorch: Not installed")
    
    try:
        import transformers
        click.echo(f"Transformers version: {transformers.__version__}")
    except ImportError:
        click.echo("Transformers: Not installed")
    
    try:
        import spacy
        click.echo(f"spaCy version: {spacy.__version__}")
        try:
            nlp = spacy.load("en_core_web_sm")
            click.echo("spaCy English model: Available")
        except OSError:
            click.echo("spaCy English model: Not found (run: python -m spacy download en_core_web_sm)")
    except ImportError:
        click.echo("spaCy: Not installed")
    
    # Project structure info
    click.echo(f"Project root: {project_root}")
    click.echo(f"Current directory: {os.getcwd()}")
    
    # Check key directories
    key_dirs = ["src", "data", "notebooks", "tests", "logs"]
    for dir_name in key_dirs:
        dir_path = project_root / dir_name
        status = "✓" if dir_path.exists() else "✗"
        click.echo(f"{status} {dir_name}/ directory")

@main.command()
def status():
    """Show development status and next steps"""
    click.echo("=== Development Status ===")
    click.echo("\n✅ Completed:")
    click.echo("  - Project infrastructure setup (Issue #1)")
    click.echo("  - Virtual environment and dependencies")
    click.echo("  - Code quality tools (black, isort, flake8)")
    click.echo("  - Pre-commit hooks")
    click.echo("  - Basic CLI framework")
    
    click.echo("\n🔄 In Progress:")
    click.echo("  - Configuration management system (Issue #2)")
    click.echo("  - Data collection setup (Issue #3)")
    
    click.echo("\n📋 Next Steps:")
    click.echo("  1. Complete configuration management (Issue #2)")
    click.echo("  2. Set up data collection pipeline (Issue #3)")
    click.echo("  3. Implement email text cleaning (Issue #4)")
    click.echo("  4. Begin Sprint 2 development")
    
    click.echo(f"\n📍 Current Sprint: Sprint 1 (Foundation)")

if __name__ == "__main__":
    main()