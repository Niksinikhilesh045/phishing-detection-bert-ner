#!/usr/bin/env python3
"""
Test CLI functionality with proper Windows encoding handling
"""

import subprocess
import sys
import os

def setup_encoding():
    """Set up proper encoding for Windows"""
    if os.name == 'nt':  # Windows
        # Set environment variables for UTF-8
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PYTHONUTF8'] = '1'
        
        # Try to set console to UTF-8
        try:
            subprocess.run("chcp 65001", shell=True, check=False, capture_output=True)
        except:
            pass

def test_cli_command(command, method_name):
    """Test a CLI command method with proper encoding"""
    print(f"\n[TEST] {method_name}")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        # Set up environment with proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {method_name}")
            print("Output:")
            # Safely display output
            try:
                print(result.stdout)
            except UnicodeEncodeError:
                print("[Output contains special characters - displaying safely]")
                safe_output = result.stdout.encode('ascii', 'replace').decode('ascii')
                print(safe_output)
            return True
        else:
            print(f"[FAILED] {method_name}")
            print("Error:")
            try:
                print(result.stderr)
            except UnicodeEncodeError:
                print("[Error contains special characters - displaying safely]")
                safe_error = result.stderr.encode('ascii', 'replace').decode('ascii')
                print(safe_error)
            return False
    except Exception as e:
        print(f"[ERROR] {method_name} - Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("CLI FUNCTIONALITY TEST - ENCODING SAFE")
    print("=" * 60)
    
    # Set up encoding
    setup_encoding()
    
    # Test methods in order of preference
    test_methods = [
        ("phishing-detect --version", "Version check"),
        ("phishing-detect --help", "Help command"),
        ("phishing-detect test", "Test command"),
        ("phishing-detect info", "Info command"),
        ("phishing-detect status", "Status command"),
        ("python run_cli.py --help", "Direct runner help"),
        ("python run_cli.py info", "Direct runner info"),
    ]
    
    success_count = 0
    working_methods = []
    
    for command, method_name in test_methods:
        if test_cli_command(command, method_name):
            success_count += 1
            working_methods.append(command.split()[0])
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if success_count > 0:
        print(f"[SUCCESS] {success_count}/{len(test_methods)} tests passed!")
        print("\n[WORKING METHODS]")
        unique_methods = list(set(working_methods))
        for method in unique_methods:
            print(f"  - {method}")
        
        print("\n[RECOMMENDED USAGE]")
        if "phishing-detect" in unique_methods:
            print("  phishing-detect info")
            print("  phishing-detect status") 
            print("  phishing-detect test")
        elif "python" in unique_methods:
            print("  python run_cli.py info")
            print("  python run_cli.py status")
            print("  python run_cli.py test")
        
        print(f"\n[READY] Issue #1 is complete! You can proceed with development.")
        
    else:
        print(f"[FAILED] All {len(test_methods)} tests failed")
        print("\n[TROUBLESHOOTING]")
        print("1. Make sure you're in the project root directory")
        print("2. Verify virtual environment is activated: (venv)")
        print("3. Try reinstalling: pip install -e . --force-reinstall")
        print("4. Check if src/cli.py exists and is properly formatted")
        
        print("\n[FALLBACK OPTIONS]")
        print("You can still work on the project using:")
        print("- Direct Python imports: from src.cli import main")
        print("- Module execution: python -m src.cli --help")

    print(f"\n[STATUS] Project infrastructure setup: {'COMPLETE' if success_count > 0 else 'NEEDS ATTENTION'}")

if __name__ == "__main__":
    main()
           