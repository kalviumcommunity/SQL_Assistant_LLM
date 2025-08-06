#  SQL Assistant using LLMs

A natural language-to-SQL assistant powered by Large Language Models (LLMs). This tool allows users to query a SQL database using plain English and returns the results instantly. It's perfect for non-technical users to access data effortlessly, or for learning and understanding SQL better.

---

##  Features

-  Ask questions like “How many users signed up last month?”
-  Converts natural language to SQL using an LLM
-  Executes SQL on a real database (SQLite)
-  Returns results in a clean, readable format
-  (Optional) Explains SQL queries in plain English

---

##  Use Case

This tool is designed for:
- Business users who want to query databases without SQL
- Developers prototyping a natural language interface
- Learners who want to understand how SQL is constructed from natural language

---

##  Tech Stack

| Component       | Tool/Library                      |
|----------------|-----------------------------------|
| LLM             | OpenAI GPT-4 / HuggingFace T5     |
| Database        | SQLite                            |
| Backend         | Python (`openai`, `sqlite3`, `pandas`) |
| UI (Optional)   | Streamlit                         |

---


##  Sample Database

We use a small sample database `customers.db` with two tables:

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

You can replace it with any SQLite database of your own.

---

##  How It Works

###  CLI Version
```bash
python main.py
```

Then input a question like:
```
> Show me all customers who signed up in July 2025
```

It returns:
- The generated SQL
- The result of the query


---

##  Prompt Engineering Details

We use the following prompt:

```
You are a helpful SQL assistant. Convert the user's natural language query into a valid SQL query based on this schema:
Table: customers(id, name, signup_date)
Table: orders(id, customer_id, amount, order_date)
```

- Temperature: `0.0` (for deterministic output)
- Output Format: SQL wrapped in markdown or JSON
- Function Calling: (Optional) if using OpenAI’s function-calling API

---

##  Example Inputs

| Natural Language                         | Generated SQL |
|-----------------------------------------|---------------|
| How many users signed up in July?       | `SELECT COUNT(*) FROM customers WHERE signup_date BETWEEN '2025-07-01' AND '2025-07-31';` |
| List all orders above $1000             | `SELECT * FROM orders WHERE amount > 1000;` |
| Show average order amount per customer  | `SELECT customer_id, AVG(amount) FROM orders GROUP BY customer_id;` |

---

##  Error Handling

- If SQL is invalid: catches the error and informs the user
- If no results: shows a "No data found" message
- Prompts are retried or rephrased if malformed SQL is returned

---

##  Project Structure

```
sql-assistant-llm/
│
├── data/
│   └── customers.db               # SQLite database
│
├── .env                           # API keys
├── main.py                        # CLI entry point
├── app.py                         # Streamlit app
├── utils.py                       # SQL execution helpers
├── prompt_template.txt            # Prompt used for LLM
├── requirements.txt               # Python dependencies
└── README.md                      # You're reading it!
```






##  Development Timeline (7 Days)

| Day | Task |
|-----|------|
| 1   | Design schema and setup SQLite DB |
| 2   | Test prompts manually with GPT |
| 3   | Code LLM-to-SQL + query executor |
| 4   | Build CLI or Streamlit app |
| 5   | Add error handling |
| 6   | Add “Explain this SQL” feature (optional) |
| 7   | Polish, test, and document |

---

##  Future Improvements

- [ ] Support for INSERT, UPDATE, DELETE
- [ ] Visualize results using charts
- [ ] Schema-aware prompting using RAG
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Voice input support (NLQ via microphone)

---


##  Author

 **[Dhananjai yadav]**  
 Email: dhananjaiyadav2006@gmail.com 
 GitHub: https://github.com/dhananjaiyadav1234
