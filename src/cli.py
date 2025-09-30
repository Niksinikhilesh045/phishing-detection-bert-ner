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

# Windows-safe symbols
def get_symbol(check=True):
    """Get appropriate symbols for different platforms"""
    if os.name == 'nt':  # Windows
        return "[OK]" if check else "[X]"
    else:  # Unix/Linux/Mac
        return "✓" if check else "✗"

def safe_echo(text):
    """Safely echo text, handling Windows encoding issues"""
    try:
        click.echo(text)
    except UnicodeEncodeError:
        # Replace problematic Unicode characters for Windows
        safe_text = text.replace("✓", "[OK]").replace("✗", "[X]").replace("✅", "[DONE]").replace("🔄", "[PROGRESS]").replace("📋", "[TODO]").replace("📍", "[CURRENT]")
        click.echo(safe_text)

@click.group()
@click.version_option(version="0.1.0")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def main(ctx, verbose):
    """Phishing Email Detection System - BERT & NER powered email security"""
    # Store verbose in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    if verbose:
        setup_logging(level="DEBUG")
    #if verbose:
        #try:
            #setup_logging(level="DEBUG")
        #except:
            #logging.getLogger().setLevel(logging.DEBUG)
        #logger.info("Verbose mode enabled")

@main.command()
@click.argument("email_file", type=click.Path(exists=True), required=False)
def predict(email_file):
    """Predict if an email is phishing or legitimate"""
    if email_file:
        logger.info(f"Analyzing email file: {email_file}")
        safe_echo(f"Analyzing: {email_file}")
    else:
        safe_echo("No email file provided.")
        safe_echo("Usage: phishing-detect predict <email_file>")
    safe_echo("Status: Not implemented yet - Part of Issue #11")

@main.command()
@click.option("--data-path", type=click.Path(), help="Path to training data")
@click.option("--epochs", default=3, help="Number of training epochs")
def train(data_path, epochs):
    """Train the phishing detection model"""
    logger.info(f"Starting training with data: {data_path}, epochs: {epochs}")
    safe_echo(f"Training model with {epochs} epochs...")
    if data_path:
        safe_echo(f"Using data from: {data_path}")
    safe_echo("Status: Not implemented yet - Part of Issue #10")

@main.command()
def info():
    """Show system information"""
    safe_echo("=== Phishing Detection System Info ===")
    safe_echo(f"Python version: {sys.version}")
    
    # Check core dependencies
    try:
        import torch
        safe_echo(f"PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            safe_echo(f"CUDA available: {torch.cuda.get_device_name()}")
        else:
            safe_echo("CUDA: Not available (using CPU)")
    except ImportError:
        safe_echo("PyTorch: Not installed")
    
    try:
        import transformers
        safe_echo(f"Transformers version: {transformers.__version__}")
    except ImportError:
        safe_echo("Transformers: Not installed")
    
    try:
        import spacy
        safe_echo(f"spaCy version: {spacy.__version__}")
        try:
            nlp = spacy.load("en_core_web_sm")
            safe_echo("spaCy English model: Available")
        except OSError:
            safe_echo("spaCy English model: Not found (run: python -m spacy download en_core_web_sm)")
    except ImportError:
        safe_echo("spaCy: Not installed")
    
    # Project structure info
    safe_echo(f"Project root: {project_root}")
    safe_echo(f"Current directory: {os.getcwd()}")
    
    # Check key directories
    key_dirs = ["src", "data", "notebooks", "tests", "logs"]
    for dir_name in key_dirs:
        dir_path = project_root / dir_name
        status = get_symbol(True) if dir_path.exists() else get_symbol(False)
        safe_echo(f"{status} {dir_name}/ directory")

@main.command()
def status():
    """Show development status and next steps"""
    safe_echo("=== Development Status ===")
    safe_echo("")
    safe_echo("[DONE] Completed:")
    safe_echo("  - Project infrastructure setup (Issue #1)")
    safe_echo("  - Virtual environment and dependencies")
    safe_echo("  - Code quality tools (black, isort, flake8)")
    safe_echo("  - Pre-commit hooks")
    safe_echo("  - Basic CLI framework")
    
    safe_echo("")
    safe_echo("[PROGRESS] In Progress:")
    safe_echo("  - Configuration management system (Issue #2)")
    safe_echo("  - Data collection setup (Issue #3)")
    
    safe_echo("")
    safe_echo("[TODO] Next Steps:")
    safe_echo("  1. Complete configuration management (Issue #2)")
    safe_echo("  2. Set up data collection pipeline (Issue #3)")
    safe_echo("  3. Implement email text cleaning (Issue #4)")
    safe_echo("  4. Begin Sprint 2 development")
    
    safe_echo("")
    safe_echo("[CURRENT] Current Sprint: Sprint 1 (Foundation)")

@main.command()
def test():
    """Test system functionality"""
    safe_echo("=== System Test ===")
    
    # Test imports
    test_imports = [
        ("sys", "Python standard library"),
        ("pathlib", "Path handling"),
        ("click", "CLI framework"),
    ]
    
    optional_imports = [
        ("torch", "PyTorch"),
        ("transformers", "Hugging Face Transformers"),
        ("spacy", "spaCy NLP"),
        ("pandas", "Pandas data processing"),
        ("numpy", "NumPy numerical computing"),
    ]
    
    safe_echo("Required dependencies:")
    for module, description in test_imports:
        try:
            __import__(module)
            safe_echo(f"{get_symbol(True)} {description}")
        except ImportError:
            safe_echo(f"{get_symbol(False)} {description} - MISSING")
    
    safe_echo("")
    safe_echo("Optional dependencies:")
    for module, description in optional_imports:
        try:
            __import__(module)
            safe_echo(f"{get_symbol(True)} {description}")
        except ImportError:
            safe_echo(f"{get_symbol(False)} {description} - Not installed")
    
    # Test project structure
    safe_echo("")
    safe_echo("Project structure:")
    required_dirs = ["src", "data", "notebooks", "tests"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        exists = dir_path.exists()
        safe_echo(f"{get_symbol(exists)} {dir_name}/ directory")
    
    safe_echo("")
    safe_echo("Test completed!")

if __name__ == "__main__":
    main()