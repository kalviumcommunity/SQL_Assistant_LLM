import sqlite3
import os

def create_sample_database():
    """Create the sample database with customers and orders tables."""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('data/customers.db')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            signup_date TEXT
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Insert sample data into customers table
    customers_data = [
        (1, 'John Smith', '2025-01-15'),
        (2, 'Jane Doe', '2025-02-20'),
        (3, 'Bob Johnson', '2025-03-10'),
        (4, 'Alice Brown', '2025-04-05'),
        (5, 'Charlie Wilson', '2025-05-12'),
        (6, 'Diana Davis', '2025-06-18'),
        (7, 'Eve Miller', '2025-07-03'),
        (8, 'Frank Garcia', '2025-08-25'),
        (9, 'Grace Lee', '2025-09-14'),
        (10, 'Henry Taylor', '2025-10-30')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO customers (id, name, signup_date)
        VALUES (?, ?, ?)
    ''', customers_data)
    
    # Insert sample data into orders table
    orders_data = [
        (1, 1, 150.00, '2025-01-20'),
        (2, 1, 75.50, '2025-02-15'),
        (3, 2, 1200.00, '2025-02-25'),
        (4, 3, 89.99, '2025-03-15'),
        (5, 4, 450.00, '2025-04-10'),
        (6, 5, 200.00, '2025-05-20'),
        (7, 6, 1800.00, '2025-06-25'),
        (8, 7, 95.00, '2025-07-08'),
        (9, 8, 320.00, '2025-08-30'),
        (10, 9, 750.00, '2025-09-20'),
        (11, 10, 125.00, '2025-10-05'),
        (12, 1, 300.00, '2025-11-10'),
        (13, 2, 85.00, '2025-11-15'),
        (14, 3, 1200.00, '2025-12-01'),
        (15, 4, 65.00, '2025-12-10')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO orders (id, customer_id, amount, order_date)
        VALUES (?, ?, ?, ?)
    ''', orders_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("✅ Sample database created successfully!")
    print("📊 Database location: data/customers.db")
    print("📋 Tables created: customers, orders")
    print("📈 Sample data inserted: 10 customers, 15 orders")

if __name__ == "__main__":
    create_sample_database()
