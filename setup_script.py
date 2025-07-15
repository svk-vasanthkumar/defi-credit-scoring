#!/usr/bin/env python3
"""
Setup Script for DeFi Credit Scoring System
===========================================

This script sets up the complete environment for running the DeFi credit scoring system.

Usage:
    python setup.py
"""

import os
import subprocess
import sys

def run_command(command, description):
    """
    Run a shell command and handle errors.
    
    Args:
        command (str): Command to run
        description (str): Description of what the command does
    """
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install from requirements.txt
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing packages"):
        return False
    
    return True

def create_directory_structure():
    """Create necessary directories."""
    directories = [
        "data",
        "output",
        "plots"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def verify_installation():
    """Verify that all required packages are installed."""
    print("🔍 Verifying installation...")
    
    required_packages = [
        "pandas",
        "numpy",
        "sklearn",
        "matplotlib",
        "seaborn"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("\n✅ All packages are installed correctly")
    return True

def show_usage_instructions():
    """Display usage instructions."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Download the transaction data:")
    print("   python download_data.py")
    print("\n2. Run the credit scoring analysis:")
    print("   python credit_scorer.py user_transactions.json")
    print("\n3. Check the output files:")
    print("   - wallet_credit_scores.csv")
    print("   - score_analysis.json")
    print("   - credit_score_analysis.png")
    
    print("\n📖 Documentation:")
    print("   - README.md: Complete methodology and usage guide")
    print("   - analysis.md: Detailed analysis template")
    
    print("\n🔧 File Structure:")
    print("   ├── credit_scorer.py      # Main scoring script")
    print("   ├── download_data.py      # Data downloader")
    print("   ├── setup.py              # This setup script")
    print("   ├── requirements.txt      # Dependencies")
    print("   ├── README.md             # Documentation")
    print("   ├── analysis.md           # Analysis template")
    print("   ├── data/                 # Data directory")
    print("   ├── output/               # Output directory")
    print("   └── plots/                # Plots directory")

def main():
    """Main setup function."""
    print("🚀 DeFi Credit Scoring System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directory structure
    create_directory_structure()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed")
        sys.exit(1)
    
    # Show usage instructions
    show_usage_instructions()

if __name__ == "__main__":
    main()
