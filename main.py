#!/usr/bin/env python3
"""
SQL Assistant LLM - CLI Version
Converts natural language queries to SQL and executes them.
"""

import os
import sys
from typing import Optional, Tuple
from dotenv import load_dotenv
import google.generativeai as genai
from utils import DatabaseManager, format_query_results, validate_sql_query, explain_sql_query

# Load environment variables
load_dotenv()

class SQLAssistant:
    """Main SQL Assistant class that handles LLM integration and query execution."""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("❌ Error: GEMINI_API_KEY not found in environment variables.")
            print("Please set your Gemini API key in the .env file or environment.")
            sys.exit(1)
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.db_manager = DatabaseManager()
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load the prompt template from file."""
        try:
            with open('prompt_template.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback prompt if file doesn't exist
            return """You are a helpful SQL assistant. Convert the user's natural language query into a valid SQL query based on this schema:

Table: customers(id, name, signup_date)
Table: orders(id, customer_id, amount, order_date)

Important guidelines:
1. Only generate SQL queries, no explanations
2. Use proper SQL syntax
3. Handle date comparisons appropriately
4. Use JOIN when querying across tables
5. Return only the SQL query, no markdown formatting

User query: {query}"""
    
    def natural_language_to_sql(self, query: str) -> Tuple[bool, str, Optional[str]]:
        """
        Convert natural language query to SQL using Gemini.
        
        Returns:
            Tuple of (success, sql_query, error_message)
        """
        try:
            # Prepare the prompt
            prompt = self.prompt_template.format(query=query)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            if response.text:
                sql_query = response.text.strip()
                
                # Clean up the SQL query (remove markdown if present)
                if sql_query.startswith('```sql'):
                    sql_query = sql_query[7:]
                if sql_query.endswith('```'):
                    sql_query = sql_query[:-3]
                sql_query = sql_query.strip()
                
                return True, sql_query, None
            else:
                return False, "", "No response from Gemini API"
            
        except Exception as e:
            return False, "", f"Error generating SQL: {str(e)}"
    
    def execute_query(self, sql_query: str) -> Tuple[bool, str, Optional[str]]:
        """
        Execute SQL query and return formatted results.
        
        Returns:
            Tuple of (success, formatted_results, error_message)
        """
        # Validate the SQL query
        is_valid, error_msg = validate_sql_query(sql_query)
        if not is_valid:
            return False, "", error_msg
        
        # Execute the query
        success, df, error = self.db_manager.execute_query(sql_query)
        if not success:
            return False, "", error
        
        # Format results
        formatted_results = format_query_results(df)
        return True, formatted_results, None
    
    def process_query(self, natural_query: str) -> None:
        """Process a natural language query end-to-end."""
        print(f"\n🔍 Processing: {natural_query}")
        print("-" * 50)
        
        # Step 1: Convert to SQL
        print("🔄 Converting to SQL...")
        success, sql_query, error = self.natural_language_to_sql(natural_query)
        
        if not success:
            print(f"❌ Error: {error}")
            return
        
        print(f"📝 Generated SQL: {sql_query}")
        
        # Step 2: Execute SQL
        print("⚡ Executing SQL...")
        success, results, error = self.execute_query(sql_query)
        
        if not success:
            print(f"❌ Error: {error}")
            return
        
        # Step 3: Display results
        print("\n📊 Results:")
        print(results)
        
        # Step 4: Explain the query (optional)
        explanation = explain_sql_query(sql_query)
        print(f"\n💡 Explanation: {explanation}")
    
    def show_database_info(self):
        """Display database schema and sample data."""
        print("\n📋 Database Schema:")
        schema_info = self.db_manager.get_schema_info()
        for table, columns in schema_info.items():
            print(f"  Table: {table}")
            print(f"    Columns: {', '.join(columns)}")
        
        print("\n📊 Sample Data:")
        sample_data = self.db_manager.get_sample_data()
        for table, df in sample_data.items():
            print(f"\n{table.upper()} table (first 3 rows):")
            print(df.head(3).to_string(index=False))
    
    def run_interactive(self):
        """Run the interactive CLI mode."""
        print("🚀 SQL Assistant LLM - Interactive Mode")
        print("=" * 50)
        print("Ask questions in natural language to query the database!")
        print("Type 'help' for examples, 'schema' for database info, or 'quit' to exit.")
        print("-" * 50)
        
        self.show_database_info()
        
        while True:
            try:
                query = input("\n❓ Your question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif query.lower() == 'help':
                    self.show_examples()
                elif query.lower() == 'schema':
                    self.show_database_info()
                elif not query:
                    continue
                else:
                    self.process_query(query)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
    
    def show_examples(self):
        """Show example queries."""
        examples = [
            "How many customers signed up in July?",
            "Show me all orders above $1000",
            "What's the average order amount?",
            "List customers who made orders in March",
            "Show total sales per customer",
            "Find the customer with the highest order amount"
        ]
        
        print("\n💡 Example Questions:")
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example}")

def main():
    """Main entry point."""
    try:
        assistant = SQLAssistant()
        assistant.run_interactive()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("Please run 'python create_database.py' first to create the sample database.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
