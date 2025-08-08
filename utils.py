import sqlite3
import pandas as pd
from typing import Tuple, Optional, List, Dict, Any
import os

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = "data/customers.db"):
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure the database file exists."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at {self.db_path}. Please run create_database.py first.")
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str) -> Tuple[bool, pd.DataFrame, Optional[str]]:
        """
        Execute a SQL query and return results.
        
        Returns:
            Tuple of (success, dataframe, error_message)
        """
        try:
            conn = self.get_connection()
            df = pd.read_sql_query(query, conn)
            conn.close()
            return True, df, None
        except Exception as e:
            return False, pd.DataFrame(), str(e)
    
    def get_schema_info(self) -> Dict[str, List[str]]:
        """Get database schema information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        schema_info = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
            schema_info[table] = columns
        
        conn.close()
        return schema_info
    
    def get_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Get sample data from all tables."""
        schema_info = self.get_schema_info()
        sample_data = {}
        
        for table in schema_info.keys():
            success, df, _ = self.execute_query(f"SELECT * FROM {table} LIMIT 5")
            if success:
                sample_data[table] = df
        
        return sample_data

def format_query_results(df: pd.DataFrame) -> str:
    """Format query results for display."""
    if df.empty:
        return "No data found."
    
    # Convert to string with proper formatting
    result = df.to_string(index=False)
    return f"Query Results ({len(df)} rows):\n{result}"

def validate_sql_query(query: str) -> Tuple[bool, Optional[str]]:
    """Basic SQL query validation."""
    query = query.strip().upper()
    
    # Check for basic SQL injection attempts
    dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
    for keyword in dangerous_keywords:
        if keyword in query and 'SELECT' not in query:
            return False, f"Query contains potentially dangerous keyword: {keyword}"
    
    # Check if it starts with SELECT
    if not query.startswith('SELECT'):
        return False, "Only SELECT queries are allowed for safety."
    
    return True, None

def explain_sql_query(query: str) -> str:
    """Generate a simple explanation of what the SQL query does."""
    query_upper = query.upper()
    
    explanation = "This query "
    
    if "COUNT(*)" in query_upper:
        explanation += "counts the total number of records"
    elif "AVG(" in query_upper:
        explanation += "calculates the average"
    elif "SUM(" in query_upper:
        explanation += "calculates the sum"
    elif "MAX(" in query_upper:
        explanation += "finds the maximum value"
    elif "MIN(" in query_upper:
        explanation += "finds the minimum value"
    else:
        explanation += "retrieves data"
    
    if "WHERE" in query_upper:
        explanation += " that match specific conditions"
    
    if "ORDER BY" in query_upper:
        explanation += " and sorts the results"
    
    if "GROUP BY" in query_upper:
        explanation += " and groups the results"
    
    explanation += "."
    
    return explanation
