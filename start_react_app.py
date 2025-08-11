#!/usr/bin/env python3
"""
Startup script for SQL Assistant LLM with React frontend
Runs the Flask API server that serves the React app.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import flask_cors
        import google.generativeai
        print("✅ All Python dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip3 install -r requirements.txt")
        return False
    
    return True

def check_api_key():
    """Check if Gemini API key is configured."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  Warning: GEMINI_API_KEY not configured")
        print("Please edit .env file and add your Gemini API key")
        print("The app will still run but SQL generation will fail")
    else:
        print("✅ Gemini API key is configured")
    
    return True

def check_database():
    """Check if database exists."""
    if not os.path.exists('data/customers.db'):
        print("❌ Database not found. Creating sample database...")
        try:
            subprocess.check_call([sys.executable, "create_database.py"])
            print("✅ Database created successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating database: {e}")
            return False
    else:
        print("✅ Database exists")
    
    return True

def check_react_build():
    """Check if React app is built."""
    if not os.path.exists('frontend/build'):
        print("❌ React build not found. Building React app...")
        try:
            subprocess.check_call(['npm', 'run', 'build'], cwd='frontend')
            print("✅ React app built successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error building React app: {e}")
            return False
    else:
        print("✅ React build exists")
    
    return True

def start_server():
    """Start the Flask server."""
    print("\n🚀 Starting SQL Assistant LLM with React frontend...")
    print("=" * 60)
    print("📊 API endpoints:")
    print("  - POST /api/query - Process natural language queries")
    print("  - GET  /api/database-info - Get database schema")
    print("  - GET  /api/examples - Get example queries")
    print("  - GET  /api/health - Health check")
    print("\n🌐 React app will be served at: http://localhost:5001")
    print("📱 You can test the zero-shot prompting capabilities!")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "api.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function."""
    print("🔍 SQL Assistant LLM - React Frontend Startup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check API key
    check_api_key()
    
    # Check database
    if not check_database():
        sys.exit(1)
    
    # Check React build
    if not check_react_build():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
