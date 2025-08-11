#!/usr/bin/env python3
"""
Flask API for SQL Assistant LLM
Serves the React frontend and handles SQL Assistant requests.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from utils import DatabaseManager, format_query_results, validate_sql_query, explain_sql_query

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

class APISQLAssistant:
    """API version of the SQL Assistant."""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
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
    
    def natural_language_to_sql(self, query: str):
        """Convert natural language query to SQL using Gemini."""
        try:
            prompt = self.prompt_template.format(query=query)
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                sql_query = response.text.strip()
                
                # Clean up the SQL query
                if sql_query.startswith('```sql'):
                    sql_query = sql_query[7:]
                if sql_query.endswith('```'):
                    sql_query = sql_query[:-3]
                sql_query = sql_query.strip()
                
                return {"success": True, "sql": sql_query, "error": None}
            else:
                return {"success": False, "sql": None, "error": "No response from Gemini API"}
            
        except Exception as e:
            return {"success": False, "sql": None, "error": f"Error generating SQL: {str(e)}"}
    
    def execute_query(self, sql_query: str):
        """Execute SQL query and return results."""
        is_valid, error_msg = validate_sql_query(sql_query)
        if not is_valid:
            return {"success": False, "data": None, "error": error_msg}
        
        success, df, error = self.db_manager.execute_query(sql_query)
        if not success:
            return {"success": False, "data": None, "error": error}
        
        # Convert DataFrame to JSON
        data = df.to_dict('records') if not df.empty else []
        return {"success": True, "data": data, "error": None}
    
    def get_database_info(self):
        """Get database schema and sample data."""
        try:
            schema_info = self.db_manager.get_schema_info()
            sample_data = self.db_manager.get_sample_data()
            
            # Convert sample data to JSON
            sample_data_json = {}
            for table, df in sample_data.items():
                sample_data_json[table] = df.to_dict('records') if not df.empty else []
            
            return {
                "success": True,
                "schema": schema_info,
                "sample_data": sample_data_json
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Initialize the assistant
try:
    assistant = APISQLAssistant()
except Exception as e:
    print(f"Error initializing assistant: {e}")
    assistant = None

@app.route('/')
def serve():
    """Serve the React app."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process a natural language query."""
    if not assistant:
        return jsonify({"error": "Assistant not initialized"}), 500
    
    try:
        data = request.get_json()
        natural_query = data.get('query', '').strip()
        
        if not natural_query:
            return jsonify({"error": "Query is required"}), 400
        
        # Step 1: Convert to SQL
        sql_result = assistant.natural_language_to_sql(natural_query)
        
        if not sql_result["success"]:
            return jsonify({
                "error": sql_result["error"],
                "sql": None,
                "data": None,
                "explanation": None
            }), 400
        
        sql_query = sql_result["sql"]
        
        # Step 2: Execute SQL
        execution_result = assistant.execute_query(sql_query)
        
        if not execution_result["success"]:
            return jsonify({
                "error": execution_result["error"],
                "sql": sql_query,
                "data": None,
                "explanation": explain_sql_query(sql_query)
            }), 400
        
        # Step 3: Generate explanation
        explanation = explain_sql_query(sql_query)
        
        return jsonify({
            "success": True,
            "sql": sql_query,
            "data": execution_result["data"],
            "explanation": explanation,
            "row_count": len(execution_result["data"])
        })
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/database-info', methods=['GET'])
def get_database_info():
    """Get database schema and sample data."""
    if not assistant:
        return jsonify({"error": "Assistant not initialized"}), 500
    
    try:
        result = assistant.get_database_info()
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify({"error": result["error"]}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example queries."""
    examples = [
        {
            "query": "How many customers signed up in July?",
            "description": "Counts customers who signed up in July 2025"
        },
        {
            "query": "Show me all orders above $1000",
            "description": "Finds all orders with amount greater than $1000"
        },
        {
            "query": "What's the average order amount?",
            "description": "Calculates the average order amount"
        },
        {
            "query": "List customers who made orders in March",
            "description": "Shows customers who placed orders in March 2025"
        },
        {
            "query": "Show total sales per customer",
            "description": "Calculates total sales for each customer"
        },
        {
            "query": "Find the customer with the highest order amount",
            "description": "Finds the customer who made the highest value order"
        }
    ]
    
    return jsonify({"examples": examples})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "assistant_ready": assistant is not None,
        "api_key_configured": bool(os.getenv('GEMINI_API_KEY'))
    })

# Handle React routing
@app.errorhandler(404)
def not_found(e):
    """Handle React routing."""
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    print("🚀 Starting SQL Assistant LLM API Server...")
    print("📊 API endpoints:")
    print("  - POST /api/query - Process natural language queries")
    print("  - GET  /api/database-info - Get database schema")
    print("  - GET  /api/examples - Get example queries")
    print("  - GET  /api/health - Health check")
    print("🌐 React app will be served at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
