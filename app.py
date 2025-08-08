#!/usr/bin/env python3
"""
SQL Assistant LLM - Streamlit Web App
Web interface for natural language to SQL conversion.
"""

import streamlit as st
import pandas as pd
import os
from typing import Optional, Tuple
from dotenv import load_dotenv
import google.generativeai as genai
from utils import DatabaseManager, format_query_results, validate_sql_query, explain_sql_query

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SQL Assistant LLM",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .sql-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitSQLAssistant:
    """Streamlit version of the SQL Assistant."""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            st.error("❌ GEMINI_API_KEY not found in environment variables.")
            st.info("Please set your Gemini API key in the .env file or environment.")
            st.stop()
        
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
    
    def natural_language_to_sql(self, query: str) -> Tuple[bool, str, Optional[str]]:
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
                
                return True, sql_query, None
            else:
                return False, "", "No response from Gemini API"
            
        except Exception as e:
            return False, "", f"Error generating SQL: {str(e)}"
    
    def execute_query(self, sql_query: str) -> Tuple[bool, pd.DataFrame, Optional[str]]:
        """Execute SQL query and return results."""
        is_valid, error_msg = validate_sql_query(sql_query)
        if not is_valid:
            return False, pd.DataFrame(), error_msg
        
        success, df, error = self.db_manager.execute_query(sql_query)
        if not success:
            return False, pd.DataFrame(), error
        
        return True, df, None
    
    def process_query(self, natural_query: str) -> None:
        """Process a natural language query and display results."""
        with st.spinner("🔄 Converting to SQL..."):
            success, sql_query, error = self.natural_language_to_sql(natural_query)
        
        if not success:
            st.error(f"❌ Error: {error}")
            return
        
        # Display generated SQL
        st.markdown("### 📝 Generated SQL")
        st.code(sql_query, language="sql")
        
        with st.spinner("⚡ Executing SQL..."):
            success, df, error = self.execute_query(sql_query)
        
        if not success:
            st.error(f"❌ Error: {error}")
            return
        
        # Display results
        st.markdown("### 📊 Query Results")
        if df.empty:
            st.info("No data found.")
        else:
            st.dataframe(df, use_container_width=True)
            st.info(f"Found {len(df)} rows.")
        
        # Display explanation
        explanation = explain_sql_query(sql_query)
        st.markdown("### 💡 Query Explanation")
        st.info(explanation)
    
    def show_database_info(self):
        """Display database schema and sample data."""
        st.markdown("### 📋 Database Schema")
        schema_info = self.db_manager.get_schema_info()
        
        for table, columns in schema_info.items():
            with st.expander(f"Table: {table}"):
                st.write(f"**Columns:** {', '.join(columns)}")
        
        st.markdown("### 📊 Sample Data")
        sample_data = self.db_manager.get_sample_data()
        
        for table, df in sample_data.items():
            with st.expander(f"{table.upper()} table"):
                st.dataframe(df, use_container_width=True)

def main():
    """Main Streamlit app."""
    st.markdown('<h1 class="main-header">🔍 SQL Assistant LLM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask questions in natural language and get SQL results instantly!</p>', unsafe_allow_html=True)
    
    # Initialize assistant
    try:
        assistant = StreamlitSQLAssistant()
    except FileNotFoundError as e:
        st.error(f"❌ {e}")
        st.info("Please run 'python create_database.py' first to create the sample database.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Tools")
        
        if st.button("📋 Show Database Schema"):
            assistant.show_database_info()
        
        if st.button("💡 Show Examples"):
            examples = [
                "How many customers signed up in July?",
                "Show me all orders above $1000",
                "What's the average order amount?",
                "List customers who made orders in March",
                "Show total sales per customer",
                "Find the customer with the highest order amount"
            ]
            
            st.markdown("### 💡 Example Questions")
            for i, example in enumerate(examples, 1):
                st.write(f"{i}. {example}")
        
        st.markdown("---")
        st.markdown("### 📊 Database Info")
        try:
            schema_info = assistant.db_manager.get_schema_info()
            st.write(f"**Tables:** {len(schema_info)}")
            for table in schema_info.keys():
                st.write(f"• {table}")
        except:
            st.write("Database not available")
    
    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Query input
        natural_query = st.text_area(
            "❓ Ask your question in natural language:",
            placeholder="e.g., How many customers signed up in July?",
            height=100
        )
        
        if st.button("🚀 Execute Query", type="primary"):
            if natural_query.strip():
                assistant.process_query(natural_query.strip())
            else:
                st.warning("Please enter a question.")
        
        # Quick examples
        st.markdown("### 🚀 Quick Examples")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("Count July signups"):
                assistant.process_query("How many customers signed up in July?")
            
            if st.button("Orders above $1000"):
                assistant.process_query("Show me all orders above $1000")
            
            if st.button("Average order amount"):
                assistant.process_query("What's the average order amount?")
        
        with col_b:
            if st.button("March orders"):
                assistant.process_query("List customers who made orders in March")
            
            if st.button("Total sales per customer"):
                assistant.process_query("Show total sales per customer")
            
            if st.button("Highest order"):
                assistant.process_query("Find the customer with the highest order amount")

if __name__ == "__main__":
    main()
