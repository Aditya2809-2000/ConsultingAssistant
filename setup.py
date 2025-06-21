#!/usr/bin/env python3
"""
Setup script for Legal Document Review System
This script helps validate the installation and configuration.
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit',
        'Pillow',
        'pdf2image',
        'google.generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_poppler():
    """Check if Poppler is available."""
    try:
        result = subprocess.run(['pdftoppm', '-h'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Poppler-utils is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Poppler-utils not found")
    print("📥 Install Poppler:")
    print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/")
    print("  macOS: brew install poppler")
    print("  Ubuntu/Debian: sudo apt-get install poppler-utils")
    return False

def check_api_key():
    """Check if API key is configured."""
    # Check environment variable
    if os.getenv('GOOGLE_API_KEY'):
        print("✅ GOOGLE_API_KEY found in environment variables")
        return True
    
    # Check Streamlit secrets
    secrets_path = os.path.join('.streamlit', 'secrets.toml')
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, 'r') as f:
                content = f.read()
                if 'GOOGLE_API_KEY' in content and 'your_google_api_key_here' not in content:
                    print("✅ GOOGLE_API_KEY found in Streamlit secrets")
                    return True
                else:
                    print("⚠️  GOOGLE_API_KEY placeholder found in secrets.toml")
        except Exception:
            pass
    
    print("❌ GOOGLE_API_KEY not configured")
    print("🔑 Configure your API key:")
    print("  1. Get your key from https://makersuite.google.com/app/apikey")
    print("  2. Set it in .streamlit/secrets.toml or as environment variable")
    return False

def create_secrets_template():
    """Create a template secrets.toml file."""
    secrets_dir = '.streamlit'
    secrets_file = os.path.join(secrets_dir, 'secrets.toml')
    
    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir)
        print(f"📁 Created directory: {secrets_dir}")
    
    if not os.path.exists(secrets_file):
        template_content = """# Google API Key for Gemini AI
# Replace 'your_google_api_key_here' with your actual API key
GOOGLE_API_KEY = "your_google_api_key_here"
"""
        with open(secrets_file, 'w') as f:
            f.write(template_content)
        print(f"📄 Created template: {secrets_file}")
        print("🔑 Please edit this file and add your actual API key")
    else:
        print(f"📄 Secrets file already exists: {secrets_file}")

def main():
    """Main setup function."""
    print("🔧 Legal Document Review System - Setup Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 4
    
    # Check Python version
    if check_python_version():
        checks_passed += 1
    
    print()
    
    # Check dependencies
    if check_dependencies():
        checks_passed += 1
    
    print()
    
    # Check Poppler
    if check_poppler():
        checks_passed += 1
    
    print()
    
    # Check API key
    if check_api_key():
        checks_passed += 1
    
    print()
    print("=" * 50)
    
    if checks_passed == total_checks:
        print("🎉 All checks passed! Your system is ready.")
        print("🚀 Run the application with: streamlit run app.py")
    else:
        print(f"⚠️  {checks_passed}/{total_checks} checks passed")
        print("📋 Please address the issues above before running the application")
        
        # Offer to create secrets template
        if not check_api_key():
            print("\n💡 Would you like to create a template secrets.toml file? (y/n)")
            try:
                response = input().lower().strip()
                if response in ['y', 'yes']:
                    create_secrets_template()
            except KeyboardInterrupt:
                print("\n👋 Setup cancelled")

if __name__ == "__main__":
    main() 