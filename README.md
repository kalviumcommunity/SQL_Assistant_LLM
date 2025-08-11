# 🔍 SQL Assistant LLM

A natural language-to-SQL assistant powered by Large Language Models (LLMs). This tool allows users to query a SQL database using plain English and returns the results instantly. It's perfect for non-technical users to access data effortlessly, or for learning and understanding SQL better.

## ✨ Features

- 🔍 **Natural Language Processing**: Ask questions like "How many users signed up last month?"
- 🤖 **LLM Integration**: Converts natural language to SQL using Google Gemini 1.5 Flash
- ⚡ **Real-time Execution**: Executes SQL on a real database (SQLite)
- 📊 **Clean Results**: Returns results in a clean, readable format
- 💡 **Query Explanations**: Explains SQL queries in plain English
- 🛡️ **Security**: SQL injection protection and query validation
- 🌐 **Web Interface**: Beautiful Streamlit web application
- ⚛️ **React Frontend**: Modern React.js interface with Material-UI
- 💻 **CLI Interface**: Command-line interface for power users
- 📋 **Schema Visualization**: View database structure and sample data
- 🎯 **Zero-shot Prompting**: No training required, works out of the box

## 🚀 Quick Start

### 1. Setup (First time only)

```bash
# Clone the repository
git clone <your-repo-url>
cd SQL_Assistant_LLM

# Run the setup script
python3 setup.py
```

### 2. Configure API Key

Edit the `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the Application

**React Frontend (Recommended):**
```bash
python3 start_react_app.py
# Opens at http://localhost:5001
```

**CLI Version:**
```bash
python3 main.py
```

**Streamlit Web Version:**
```bash
streamlit run app.py
```

## 📊 Sample Database

We use a small sample database `data/customers.db` with two tables:

### Schema:

```sql
-- Table: customers
id INTEGER PRIMARY KEY,
name TEXT,
signup_date TEXT

-- Table: orders
id INTEGER PRIMARY KEY,
customer_id INTEGER,
amount REAL,
order_date TEXT
```

The database comes pre-populated with 10 customers and 15 orders for testing.

## 💡 Example Queries

| Natural Language | Generated SQL |
|------------------|---------------|
| "How many customers signed up in July?" | `SELECT COUNT(*) FROM customers WHERE signup_date LIKE '2025-07%'` |
| "Show me all orders above $1000" | `SELECT * FROM orders WHERE amount > 1000` |
| "What's the average order amount?" | `SELECT AVG(amount) FROM orders` |
| "List customers who made orders in March" | `SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.order_date LIKE '2025-03%'` |
| "Show total sales per customer" | `SELECT c.name, SUM(o.amount) as total_sales FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name` |

## 🛠️ Technology Stack

| Component | Tool/Library |
|-----------|--------------|
| LLM | Google Gemini 1.5 Flash |
| Database | SQLite |
| Backend | Python 3.8+ |
| Web Framework | Streamlit |
| React Frontend | React.js + Material-UI |
| API Server | Flask |
| Data Processing | Pandas |
| Environment | python-dotenv |
| API | Google Gemini API |

## 📁 Project Structure

```
sql-assistant-llm/
├── data/
│   └── customers.db          # SQLite database
├── frontend/                 # React frontend
│   ├── build/               # Built React app
│   ├── src/                 # React source code
│   └── package.json         # React dependencies
├── .env                      # API keys (create from env_template.txt)
├── main.py                   # CLI entry point
├── app.py                    # Streamlit web app
├── api.py                    # Flask API server
├── start_react_app.py        # React app startup script
├── utils.py                  # SQL execution helpers
├── create_database.py        # Database setup script
├── setup.py                  # Project setup script
├── demo.py                   # Demo script
├── prompt_template.txt       # LLM prompt template
├── env_template.txt          # Environment template
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## 🔧 How It Works

### 1. Natural Language Processing
The system uses Google's Gemini 1.5 Flash model to convert natural language queries into SQL. The prompt template provides the database schema and guidelines for SQL generation.

### 2. SQL Generation
```python
# Example prompt
You are a helpful SQL assistant. Convert the user's natural language query into a valid SQL query based on this schema:
Table: customers(id, name, signup_date)
Table: orders(id, customer_id, amount, order_date)
```

### 3. Query Execution
Generated SQL queries are validated for security and then executed against the SQLite database using pandas.

### 4. Result Formatting
Results are formatted and displayed with explanations of what the query does.

## 🎯 Prompt Engineering

We use the following prompt engineering techniques:

- **Model**: Gemini 1.5 Flash (fast and efficient)
- **System Context**: Clear role definition as SQL expert
- **Schema Context**: Database schema provided in prompt
- **Safety Guidelines**: Only SELECT queries allowed
- **Format Instructions**: Clean SQL output without markdown

## 🛡️ Security Features

- **SQL Injection Protection**: Validates queries before execution
- **Query Restrictions**: Only allows SELECT queries
- **Input Sanitization**: Cleans and validates user input
- **Error Handling**: Graceful error messages without exposing internals

## 🌐 Frontend Interfaces

### React Frontend (Recommended)
- **Modern UI**: Beautiful Material-UI design
- **Real-time Results**: Instant SQL generation and execution
- **Interactive Examples**: One-click example queries
- **Schema Explorer**: View database structure
- **Copy to Clipboard**: Easy SQL copying
- **Responsive Design**: Works on desktop and mobile

### Streamlit Web Interface
- **Interactive Query Input**: Text area for natural language questions
- **Real-time Results**: Instant SQL generation and execution
- **Schema Explorer**: View database structure and sample data
- **Quick Examples**: One-click example queries
- **Responsive Design**: Works on desktop and mobile
- **Beautiful UI**: Modern, clean interface

### CLI Interface
- **Interactive Mode**: Continuous query session
- **Help Commands**: Built-in help and examples
- **Schema Display**: View database structure
- **Error Handling**: Clear error messages
- **Exit Commands**: Easy session management

## 🚀 Usage Examples

### React Frontend
```bash
python3 start_react_app.py
# Opens browser at http://localhost:5001
# Type queries in the text area
# Click "Execute Query" button
```

### CLI Mode
```bash
python3 main.py
> How many customers signed up in July?
> Show me all orders above $1000
> help
> schema
> quit
```

### Streamlit Mode
```bash
streamlit run app.py
# Opens browser interface
# Type queries in the text area
# Click "Execute Query" button
```

## 🔍 Demo

Run the demo script to see all features:
```bash
python3 demo.py
```

## 📋 Development Timeline

| Day | Task | Status |
|-----|------|--------|
| 1 | Design schema and setup SQLite DB | ✅ Complete |
| 2 | Test prompts manually with Gemini | ✅ Complete |
| 3 | Code LLM-to-SQL + query executor | ✅ Complete |
| 4 | Build CLI and Streamlit app | ✅ Complete |
| 5 | Add error handling | ✅ Complete |
| 6 | Add "Explain this SQL" feature | ✅ Complete |
| 7 | Build React frontend | ✅ Complete |
| 8 | Polish, test, and document | ✅ Complete |

## 🔮 Future Improvements

- [ ] Support for INSERT, UPDATE, DELETE operations
- [ ] Visualize results using charts and graphs
- [ ] Schema-aware prompting using RAG
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Voice input support (NLQ via microphone)
- [ ] Query history and favorites
- [ ] Export results to CSV/Excel
- [ ] Custom database schema support

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is set in `.env`
2. **Database Not Found**: Run `python3 create_database.py`
3. **Import Errors**: Install dependencies with `pip3 install -r requirements.txt`
4. **React Build Issues**: Run `cd frontend && npm run build`
5. **Flask Server Issues**: Check if port 5000 is available

### Getting Help

- Check the demo: `python3 demo.py`
- View database info: Run `schema` command in CLI
- Test setup: `python3 setup.py`
- Test API: `python3 test_gemini.py`

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Dhananjai Yadav**  
Email: dhananjaiyadav2006@gmail.com  
GitHub: https://github.com/dhananjaiyadav1234

---

**🎉 Ready to query your database with natural language!**
