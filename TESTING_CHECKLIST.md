# 🧪 SQL Assistant LLM - Testing Checklist

## ✅ Server Status Check

### **1. Server is Running**
```bash
# Check if server is responding
curl -s http://localhost:5001/api/health
```
**Expected Output:**
```json
{
  "api_key_configured": true,
  "assistant_ready": true,
  "status": "healthy"
}
```

### **2. API Endpoints Working**
```bash
# Test examples endpoint
curl -s http://localhost:5001/api/examples

# Test database info endpoint
curl -s http://localhost:5001/api/database-info
```

### **3. React Frontend Accessible**
```bash
# Check if React app is served
curl -s http://localhost:5001/ | head -5
```
**Expected Output:** HTML with React app content

## 🎯 Zero-Shot Prompting Tests

### **Test 1: Basic Counting Query**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"How many customers signed up in July?"}' \
  http://localhost:5001/api/query
```
**Expected:** SQL with COUNT(*) and date filtering

### **Test 2: Numeric Filtering**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"Show me all orders above $1000"}' \
  http://localhost:5001/api/query
```
**Expected:** SQL with WHERE amount > 1000

### **Test 3: Aggregation Function**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"What is the average order amount?"}' \
  http://localhost:5001/api/query
```
**Expected:** SQL with AVG(amount)

### **Test 4: JOIN Operation**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query":"Show total sales per customer"}' \
  http://localhost:5001/api/query
```
**Expected:** SQL with JOIN and GROUP BY

## 🌐 Browser Testing

### **1. Open React Frontend**
- Open browser to: **http://localhost:5001**
- Should see "🔍 SQL Assistant LLM" header
- Health status chips should show green

### **2. Test Interactive Features**
- [ ] **Query Input**: Type a natural language query
- [ ] **Execute Button**: Click to process query
- [ ] **Loading State**: Should show spinner while processing
- [ ] **Results Display**: Should show SQL, explanation, and data table
- [ ] **Copy Button**: Click to copy generated SQL
- [ ] **Examples**: Click example queries to populate input

### **3. Test Sidebar Features**
- [ ] **Quick Examples**: Click "Try This" buttons
- [ ] **Database Schema**: Expand tables to see columns
- [ ] **Health Status**: Should show API and Gemini status

### **4. Test Error Handling**
- [ ] **Empty Query**: Try submitting empty query
- [ ] **Invalid Query**: Try "Show me all data" (should show error)
- [ ] **Network Error**: Disconnect internet temporarily

## 📊 Database Verification

### **1. Check Database Exists**
```bash
ls -la data/customers.db
```
**Expected:** File should exist and be readable

### **2. Verify Sample Data**
```bash
sqlite3 data/customers.db "SELECT COUNT(*) FROM customers;"
sqlite3 data/customers.db "SELECT COUNT(*) FROM orders;"
```
**Expected:** 10 customers, 15 orders

### **3. Test Direct Database Queries**
```bash
# Test a simple query
sqlite3 data/customers.db "SELECT COUNT(*) FROM customers WHERE signup_date LIKE '2025-07%';"
```

## 🔧 Component Testing

### **1. CLI Application**
```bash
python3 main.py
# Type: "How many customers signed up in July?"
# Type: "help"
# Type: "quit"
```

### **2. Streamlit Application**
```bash
streamlit run app.py
# Should open browser with Streamlit interface
```

### **3. Demo Script**
```bash
python3 demo.py
# Should show project overview and examples
```

## 🐛 Troubleshooting

### **Common Issues & Solutions**

#### **1. Port 5001 Already in Use**
```bash
# Check what's using the port
lsof -i :5001

# Kill the process if needed
kill -9 <PID>
```

#### **2. API Key Not Configured**
```bash
# Check .env file
cat .env

# Should contain:
# GEMINI_API_KEY=your_actual_api_key_here
```

#### **3. Database Not Found**
```bash
# Create database
python3 create_database.py
```

#### **4. React Build Missing**
```bash
# Build React app
cd frontend && npm run build
```

#### **5. Dependencies Missing**
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install React dependencies
cd frontend && npm install
```

## 🎯 Zero-Shot Testing Scenarios

### **Scenario 1: Basic Queries**
- [ ] "How many customers are there?"
- [ ] "Show me all customers"
- [ ] "What's the total number of orders?"

### **Scenario 2: Filtering Queries**
- [ ] "Show customers who signed up in March"
- [ ] "Find orders above $500"
- [ ] "List customers with names starting with 'J'"

### **Scenario 3: Aggregation Queries**
- [ ] "What's the average order amount?"
- [ ] "Show the total sales"
- [ ] "Find the highest order amount"

### **Scenario 4: JOIN Queries**
- [ ] "Show customers and their orders"
- [ ] "List customers who made orders"
- [ ] "Find total sales per customer"

### **Scenario 5: Complex Queries**
- [ ] "Show customers who made orders in March with amounts above $100"
- [ ] "Find the customer with the most orders"
- [ ] "Show average order amount per month"

## 📈 Performance Metrics

### **Response Time**
- [ ] SQL generation: < 3 seconds
- [ ] Query execution: < 1 second
- [ ] Page load: < 2 seconds

### **Accuracy**
- [ ] SQL syntax is correct
- [ ] Results match expected output
- [ ] Error handling works properly

### **User Experience**
- [ ] Interface is responsive
- [ ] Loading states work
- [ ] Error messages are clear
- [ ] Copy functionality works

## 🎉 Success Criteria

### **✅ All Systems Working**
- [ ] Flask API server running on port 5001
- [ ] React frontend accessible at http://localhost:5001
- [ ] Gemini API key configured and working
- [ ] Database populated with sample data
- [ ] All API endpoints responding correctly

### **✅ Zero-Shot Prompting Working**
- [ ] Natural language queries generate correct SQL
- [ ] Results are displayed properly
- [ ] Error handling works for invalid queries
- [ ] Query explanations are helpful

### **✅ User Interface Working**
- [ ] React app loads without errors
- [ ] All interactive features work
- [ ] Responsive design on different screen sizes
- [ ] Copy and paste functionality works

---

**🎯 If all items are checked, your SQL Assistant LLM is working perfectly for zero-shot prompting!**
