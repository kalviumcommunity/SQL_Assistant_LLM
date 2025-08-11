#!/usr/bin/env python3
"""
Test script for Gemini API integration
Verifies that the Gemini API is working correctly.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test the Gemini API connection."""
    print("🧪 Testing Gemini API Connection...")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Error: GEMINI_API_KEY not found or not set properly.")
        print("Please edit .env file and add your Gemini API key:")
        print("GEMINI_API_KEY=your_actual_api_key_here")
        return False
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple query
        test_prompt = """You are a helpful SQL assistant. Convert the user's natural language query into a valid SQL query based on this schema:

Table: customers(id, name, signup_date)
Table: orders(id, customer_id, amount, order_date)

Important guidelines:
1. Only generate SQL queries, no explanations
2. Use proper SQL syntax
3. Handle date comparisons appropriately
4. Use JOIN when querying across tables
5. Return only the SQL query, no markdown formatting

User query: How many customers signed up in July?"""
        
        print("🔄 Testing SQL generation...")
        response = model.generate_content(test_prompt)
        
        if response.text:
            sql_query = response.text.strip()
            print("✅ Gemini API is working!")
            print(f"📝 Generated SQL: {sql_query}")
            return True
        else:
            print("❌ No response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure your API key is correct")
        print("2. Check your internet connection")
        print("3. Verify the API key has proper permissions")
        return False

def test_sql_assistant():
    """Test the SQL Assistant functionality."""
    print("\n🔍 Testing SQL Assistant...")
    print("=" * 50)
    
    try:
        from main import SQLAssistant
        assistant = SQLAssistant()
        print("✅ SQL Assistant initialized successfully!")
        
        # Test a simple query
        test_query = "How many customers signed up in July?"
        print(f"🔄 Testing query: '{test_query}'")
        
        success, sql_query, error = assistant.natural_language_to_sql(test_query)
        
        if success:
            print(f"✅ SQL generated: {sql_query}")
            
            # Test execution
            success, results, error = assistant.execute_query(sql_query)
            if success:
                print("✅ Query executed successfully!")
                print(f"📊 Results: {results}")
            else:
                print(f"❌ Query execution failed: {error}")
        else:
            print(f"❌ SQL generation failed: {error}")
            
    except Exception as e:
        print(f"❌ Error testing SQL Assistant: {e}")

def main():
    """Main test function."""
    print("🚀 SQL Assistant LLM - Gemini API Test")
    print("=" * 60)
    
    # Test Gemini connection
    if test_gemini_connection():
        # Test SQL Assistant
        test_sql_assistant()
    
    print("\n" + "=" * 60)
    print("🎉 Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
