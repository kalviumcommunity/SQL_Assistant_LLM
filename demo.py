#!/usr/bin/env python3
"""
Demo script for SQL Assistant LLM
Showcases the project's capabilities with example queries.
"""

import os
import sys
from dotenv import load_dotenv
from utils import DatabaseManager, format_query_results, validate_sql_query, explain_sql_query

# Load environment variables
load_dotenv()

def print_demo_banner():
    """Print demo banner."""
    print("=" * 70)
    print("🔍 SQL Assistant LLM - Demo")
    print("=" * 70)
    print("This demo showcases the project's capabilities")
    print("=" * 70)

def show_database_info():
    """Display database information."""
    print("\n📊 Database Information:")
    print("-" * 40)
    
    try:
        db_manager = DatabaseManager()
        
        # Show schema
        schema_info = db_manager.get_schema_info()
        print("📋 Schema:")
        for table, columns in schema_info.items():
            print(f"  • {table}: {', '.join(columns)}")
        
        # Show sample data
        sample_data = db_manager.get_sample_data()
        print("\n📈 Sample Data:")
        for table, df in sample_data.items():
            print(f"  • {table.upper()} table: {len(df)} rows")
            if not df.empty:
                print(f"    First row: {df.iloc[0].to_dict()}")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

def show_example_queries():
    """Show example queries and their expected SQL."""
    print("\n💡 Example Queries:")
    print("-" * 40)
    
    examples = [
        {
            "query": "How many customers signed up in July?",
            "expected_sql": "SELECT COUNT(*) FROM customers WHERE signup_date LIKE '2025-07%'",
            "description": "Counts customers who signed up in July 2025"
        },
        {
            "query": "Show me all orders above $1000",
            "expected_sql": "SELECT * FROM orders WHERE amount > 1000",
            "description": "Finds all orders with amount greater than $1000"
        },
        {
            "query": "What's the average order amount?",
            "expected_sql": "SELECT AVG(amount) FROM orders",
            "description": "Calculates the average order amount"
        },
        {
            "query": "List customers who made orders in March",
            "expected_sql": "SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.order_date LIKE '2025-03%'",
            "description": "Shows customers who placed orders in March 2025"
        },
        {
            "query": "Show total sales per customer",
            "expected_sql": "SELECT c.name, SUM(o.amount) as total_sales FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name",
            "description": "Calculates total sales for each customer"
        },
        {
            "query": "Find the customer with the highest order amount",
            "expected_sql": "SELECT c.name, o.amount FROM customers c JOIN orders o ON c.id = o.customer_id ORDER BY o.amount DESC LIMIT 1",
            "description": "Finds the customer who made the highest value order"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Natural Language: {example['query']}")
        print(f"   Expected SQL: {example['expected_sql']}")
        print(f"   Description: {example['description']}")

def show_project_structure():
    """Show the project structure."""
    print("\n📁 Project Structure:")
    print("-" * 40)
    
    structure = """
sql-assistant-llm/
├── data/
│   └── customers.db          # SQLite database
├── .env                      # API keys (create from env_template.txt)
├── main.py                   # CLI entry point
├── app.py                    # Streamlit web app
├── utils.py                  # SQL execution helpers
├── create_database.py        # Database setup script
├── setup.py                  # Project setup script
├── demo.py                   # This demo script
├── prompt_template.txt       # LLM prompt template
├── env_template.txt          # Environment template
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
"""
    print(structure)

def show_usage_instructions():
    """Show usage instructions."""
    print("\n🚀 Usage Instructions:")
    print("-" * 40)
    
    print("\n1. Setup (First time only):")
    print("   python3 setup.py")
    print("   # Edit .env file and add your Gemini API key")
    
    print("\n2. CLI Version:")
    print("   python3 main.py")
    print("   # Interactive mode - ask questions in natural language")
    
    print("\n3. Web Version:")
    print("   streamlit run app.py")
    print("   # Opens a web interface in your browser")
    
    print("\n4. Example Queries:")
    print("   • 'How many customers signed up in July?'")
    print("   • 'Show me all orders above $1000'")
    print("   • 'What's the average order amount?'")
    print("   • 'List customers who made orders in March'")
    print("   • 'Show total sales per customer'")

def show_features():
    """Show project features."""
    print("\n✨ Features:")
    print("-" * 40)
    
    features = [
        "🔍 Natural language to SQL conversion using Google Gemini",
        "🗄️ SQLite database with sample customer and order data",
        "⚡ Real-time SQL query execution",
        "📊 Clean, formatted results display",
        "💡 SQL query explanations",
        "🛡️ SQL injection protection",
        "🌐 Web interface with Streamlit",
        "💻 Command-line interface",
        "📋 Database schema visualization",
        "🎯 Zero-shot prompting (no training required)"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_tech_stack():
    """Show the technology stack."""
    print("\n🛠️ Technology Stack:")
    print("-" * 40)
    
    tech_stack = [
        ("LLM", "Google Gemini 1.5 Flash"),
        ("Database", "SQLite"),
        ("Backend", "Python 3.8+"),
        ("Web Framework", "Streamlit"),
        ("Data Processing", "Pandas"),
        ("Environment", "python-dotenv"),
        ("API", "Google Gemini API")
    ]
    
    for tech, tool in tech_stack:
        print(f"  • {tech}: {tool}")

def main():
    """Main demo function."""
    print_demo_banner()
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("\n⚠️  Warning: Gemini API key not configured")
        print("   Please edit .env file and add your API key to test the LLM features")
        print("   You can still explore the project structure and database")
    
    # Show project information
    show_project_structure()
    show_features()
    show_tech_stack()
    show_database_info()
    show_example_queries()
    show_usage_instructions()
    
    print("\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("=" * 70)
    print("\nReady to get started? Run: python3 setup.py")

if __name__ == "__main__":
    main()
