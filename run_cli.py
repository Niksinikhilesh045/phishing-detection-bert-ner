#!/usr/bin/env python3
"""
Direct CLI runner - bypasses package installation issues
"""

import os
import sys
from pathlib import Path

# Set encoding for Windows
if os.name == "nt":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

# Ensure we can import from src
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the CLI
try:
    from src.cli import main

    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the project root directory")
    print("and that src/cli.py exists")
