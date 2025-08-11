#!/usr/bin/env python3
"""
Setup script for SQL Assistant LLM
Helps users get started with the project.
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Print project banner."""
    print("=" * 60)
    print("🔍 SQL Assistant LLM - Setup")
    print("=" * 60)
    print("Natural language to SQL conversion using LLMs")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_database():
    """Create the sample database."""
    print("\n🗄️ Creating sample database...")
    try:
        subprocess.check_call([sys.executable, "create_database.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_env_file():
    """Set up the .env file."""
    print("\n🔑 Setting up environment file...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_template.txt'):
        try:
            shutil.copy('env_template.txt', '.env')
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your Gemini API key")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("❌ env_template.txt not found")
        return False

def test_setup():
    """Test the setup by running a simple check."""
    print("\n🧪 Testing setup...")
    
    # Check if database exists
    if not os.path.exists('data/customers.db'):
        print("❌ Database not found. Please run setup again.")
        return False
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please create it manually.")
    
    print("✅ Setup test completed!")
    return True

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Edit .env file and add your Gemini API key")
    print("2. Run the CLI version: python3 main.py")
    print("3. Run the web version: streamlit run app.py")
    print("\n💡 Example usage:")
    print("   python3 main.py")
    print("   # Then ask: 'How many customers signed up in July?'")
    print("\n🌐 Web interface:")
    print("   streamlit run app.py")
    print("   # Then open your browser to the provided URL")
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Setup environment file
    setup_env_file()
    
    # Test setup
    if not test_setup():
        sys.exit(1)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
