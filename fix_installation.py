#!/usr/bin/env python3
"""
Quick fix script for package installation issues
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and report success/failure"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("🚀 Fixing package installation issues...\n")
    
    # Step 1: Uninstall existing installation
    run_command("pip uninstall phishing-detection-bert-ner -y", "Uninstalling existing package")
    
    # Step 2: Clean build artifacts
    print("🧹 Cleaning build artifacts...")
    import shutil
    for dir_name in ["build", "dist", "*.egg-info"]:
        for path in Path(".").glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed: {path}")
    
    # Step 3: Reinstall in development mode
    success = run_command("pip install -e .", "Installing package in development mode")
    
    if success:
        print("\n✅ Package installation fixed!")
        
        # Step 4: Test CLI commands
        print("\n🧪 Testing CLI commands...")
        run_command("phishing-detect --help", "Testing CLI help")
        run_command("phishing-detect info", "Testing CLI info command")
        run_command("phishing-detect status", "Testing CLI status command")
        
    else:
        print("\n❌ Installation still has issues. Let's try alternative approach...")
        
        # Alternative: Direct execution
        print("\n🔄 Setting up alternative CLI access...")
        
        # Create a wrapper script
        wrapper_content = '''#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run CLI
from src.cli import main

if __name__ == "__main__":
    main()
'''
        
        with open("phishing_detect.py", "w") as f:
            f.write(wrapper_content)
        
        print("✅ Created wrapper script: phishing_detect.py")
        print("   You can now run: python phishing_detect.py info")

if __name__ == "__main__":
    main()