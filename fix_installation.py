#!/usr/bin/env python3
"""
Quick fix script for package installation issues
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and report success/failure"""
    print(f"[RUNNING] {description}...")
    try:
        # Set environment variable for UTF-8 encoding on Windows
        env = os.environ.copy()
        if os.name == 'nt':  # Windows
            env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".", env=env)
        if result.returncode == 0:
            print(f"[SUCCESS] {description}")
            return True
        else:
            print(f"[FAILED] {description}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[ERROR] {description} - Exception: {e}")
        return False

def clean_build_artifacts():
    """Clean build artifacts"""
    print("[CLEANUP] Cleaning build artifacts...")
    import shutil
    
    patterns_to_clean = [
        "build", 
        "dist", 
        "*.egg-info",
        "__pycache__",
        "src/__pycache__"
    ]
    
    for pattern in patterns_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                try:
                    shutil.rmtree(path)
                    print(f"   Removed directory: {path}")
                except Exception as e:
                    print(f"   Could not remove {path}: {e}")
    
    # Also clean any .pyc files
    for pyc_file in Path(".").rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"   Removed: {pyc_file}")
        except Exception:
            pass

def fix_encoding_on_windows():
    """Set up Windows environment for proper Unicode handling"""
    if os.name == 'nt':  # Windows
        print("[CONFIG] Configuring Windows environment for Unicode...")
        # Set console to UTF-8 mode
        try:
            subprocess.run("chcp 65001", shell=True, check=False, capture_output=True)
            print("   Set console to UTF-8 mode")
        except:
            pass
        
        # Set environment variables
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PYTHONUTF8'] = '1'
        print("   Set Python encoding variables")

def test_cli_safe():
    """Test CLI with safe commands that avoid Unicode issues"""
    print("\n[TEST] Testing CLI functionality...")
    
    # Set encoding environment for subprocess
    env = os.environ.copy()
    if os.name == 'nt':
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
    
    test_commands = [
        ("phishing-detect --help", "CLI help"),
        ("phishing-detect --version", "CLI version"),
    ]
    
    success_count = 0
    for command, description in test_commands:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
            if result.returncode == 0:
                print(f"[SUCCESS] {description}")
                success_count += 1
            else:
                print(f"[FAILED] {description}")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"[ERROR] {description} - {e}")
    
    return success_count > 0

def main():
    print("=" * 60)
    print("PHISHING DETECTION - INSTALLATION FIX")
    print("=" * 60)
    
    # Step 1: Fix Windows encoding issues
    fix_encoding_on_windows()
    
    # Step 2: Clean build artifacts
    clean_build_artifacts()
    
    # Step 3: Uninstall existing package
    run_command("pip uninstall phishing-detection-bert-ner -y", "Uninstalling existing package")
    
    # Step 4: Reinstall in development mode
    success = run_command("pip install -e .", "Installing package in development mode")
    
    if success:
        print("\n[SUCCESS] Package installation completed!")
        
        # Step 5: Test CLI commands (safe ones first)
        if test_cli_safe():
            print("\n[INFO] Basic CLI functionality is working!")
            print("Now testing full commands...")
            
            # Test the problematic commands with proper encoding
            env = os.environ.copy()
            if os.name == 'nt':
                env['PYTHONIOENCODING'] = 'utf-8'
                env['PYTHONUTF8'] = '1'
            
            print("\n[TEST] Testing info command...")
            try:
                result = subprocess.run("phishing-detect info", shell=True, capture_output=True, text=True, env=env)
                if result.returncode == 0:
                    print("[SUCCESS] Info command works!")
                    print("Output preview:")
                    # Show first few lines to avoid potential encoding issues
                    lines = result.stdout.split('\n')[:5]
                    for line in lines:
                        print(f"   {line}")
                else:
                    print(f"[ISSUE] Info command still has problems")
                    print("   This may be a Windows console encoding issue")
                    print("   Try: python run_cli.py info (if available)")
            except Exception as e:
                print(f"[ERROR] Could not test info command: {e}")
        
    else:
        print("\n[FAILED] Installation still has issues. Creating alternative...")
        
        # Create alternative runner
        create_alternative_runner()

def create_alternative_runner():
    """Create alternative ways to run the CLI"""
    print("\n[ALTERNATIVE] Creating direct runner...")
    
    # Create run_cli.py
    runner_content = '''#!/usr/bin/env python3
"""
Direct CLI runner - bypasses package installation issues
"""

import sys
import os
from pathlib import Path

# Set encoding for Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

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
'''
    
    with open("run_cli.py", "w", encoding="utf-8") as f:
        f.write(runner_content)
    
    print("[SUCCESS] Created run_cli.py")
    print("   Usage: python run_cli.py info")
    print("   Usage: python run_cli.py status")
    
    # Create batch file for Windows
    if os.name == 'nt':
        batch_content = '''@echo off
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
python run_cli.py %*
'''
        with open("pd.bat", "w") as f:
            f.write(batch_content)
        print("[SUCCESS] Created pd.bat for Windows")
        print("   Usage: pd info")
        print("   Usage: pd status")

if __name__ == "__main__":
    main()
    
    print("\n" + "=" * 60)
    print("INSTALLATION FIX COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Try: phishing-detect --help")
    print("2. If that works, try: phishing-detect info")
    print("3. If issues persist, use: python run_cli.py info")
    print("4. On Windows, you can also use: pd info")
    print("\nThe encoding issues should now be resolved!")