# ⚛️ React Frontend for SQL Assistant LLM

## 🎯 Overview

This document describes the React frontend implementation for the SQL Assistant LLM project. The frontend provides a modern, responsive web interface for testing zero-shot prompting capabilities with natural language to SQL conversion.

## 🚀 Features

### ✅ **Modern React Interface**
- **Material-UI Design**: Beautiful, professional UI components
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Instant feedback and loading states
- **Interactive Elements**: Clickable examples and copy functionality

### ✅ **Zero-Shot Prompting Interface**
- **Natural Language Input**: Large text area for queries
- **One-Click Examples**: Pre-built example queries to test
- **SQL Display**: Syntax-highlighted SQL code with copy button
- **Results Table**: Formatted data display with scrolling
- **Query Explanations**: Plain English explanations of SQL queries

### ✅ **Database Schema Explorer**
- **Expandable Tables**: Click to see table columns
- **Column Chips**: Visual representation of database structure
- **Sample Data**: Quick access to database information

### ✅ **Health Monitoring**
- **API Status**: Real-time API health indicators
- **Gemini API Status**: Shows if API key is configured
- **Error Handling**: Graceful error display and recovery

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend Framework** | React.js 18 | Modern UI development |
| **UI Library** | Material-UI (MUI) | Professional components |
| **HTTP Client** | Axios | API communication |
| **Syntax Highlighting** | react-syntax-highlighter | SQL code display |
| **Styling** | Emotion (MUI) | CSS-in-JS styling |
| **Build Tool** | Create React App | Development and build |

## 📁 Project Structure

```
frontend/
├── build/                    # Production build
├── public/                   # Static assets
├── src/
│   ├── App.js               # Main React component
│   ├── index.js             # React entry point
│   └── package.json         # Dependencies
└── package.json             # Project configuration
```

## 🔧 API Integration

### **Backend Communication**
The React app communicates with the Flask API server:

```javascript
const API_BASE_URL = 'http://localhost:5001/api';

// Health check
const healthStatus = await axios.get(`${API_BASE_URL}/health`);

// Process query
const response = await axios.post(`${API_BASE_URL}/query`, {
  query: naturalLanguageQuery
});

// Get database info
const dbInfo = await axios.get(`${API_BASE_URL}/database-info`);

// Get examples
const examples = await axios.get(`${API_BASE_URL}/examples`);
```

### **API Endpoints**
- `POST /api/query` - Process natural language queries
- `GET /api/database-info` - Get database schema and sample data
- `GET /api/examples` - Get example queries
- `GET /api/health` - Health check and status

## 🎨 UI Components

### **Main Interface**
- **Header**: Project title and health status chips
- **Query Input**: Large text area with placeholder
- **Execute Button**: Loading state with spinner
- **Results Section**: SQL, explanation, and data table

### **Sidebar**
- **Quick Examples**: Clickable example queries
- **Database Schema**: Expandable table information
- **Column Display**: Visual chip representation

### **Results Display**
- **SQL Code**: Syntax-highlighted with copy button
- **Explanation**: Plain English query description
- **Data Table**: Scrollable results with headers

## 🚀 Getting Started

### **1. Install Dependencies**
```bash
cd frontend
npm install
```

### **2. Build for Production**
```bash
npm run build
```

### **3. Start the Full Stack**
```bash
# From project root
python3 start_react_app.py
```

### **4. Access the Application**
Open your browser to: http://localhost:5001

## 💡 Usage Examples

### **Testing Zero-Shot Prompting**

1. **Basic Query**
   ```
   Input: "How many customers signed up in July?"
   Output: SELECT COUNT(*) FROM customers WHERE signup_date LIKE '2025-07%'
   ```

2. **Complex Query**
   ```
   Input: "Show total sales per customer"
   Output: SELECT c.name, SUM(o.amount) as total_sales FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name
   ```

3. **Filtering Query**
   ```
   Input: "Show me all orders above $1000"
   Output: SELECT * FROM orders WHERE amount > 1000
   ```

### **Interactive Features**

- **Click Examples**: One-click to populate query field
- **Copy SQL**: Click copy button to copy generated SQL
- **Expand Schema**: Click to see table columns
- **Real-time Results**: Instant feedback and loading states

## 🎯 Zero-Shot Testing

### **What to Test**

1. **Natural Language Understanding**
   - Try different phrasings for the same query
   - Test complex multi-table queries
   - Verify date handling and filtering

2. **SQL Generation Accuracy**
   - Check if JOINs are used correctly
   - Verify aggregation functions (COUNT, SUM, AVG)
   - Test WHERE clause generation

3. **Error Handling**
   - Try invalid queries
   - Test edge cases
   - Verify error messages

4. **User Experience**
   - Test responsive design
   - Verify copy functionality
   - Check loading states

### **Example Test Cases**

| Natural Language | Expected SQL | Test Purpose |
|------------------|--------------|--------------|
| "How many customers signed up in July?" | `SELECT COUNT(*) FROM customers WHERE signup_date LIKE '2025-07%'` | Basic counting and date filtering |
| "Show me all orders above $1000" | `SELECT * FROM orders WHERE amount > 1000` | Numeric filtering |
| "What's the average order amount?" | `SELECT AVG(amount) FROM orders` | Aggregation functions |
| "List customers who made orders in March" | `SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.order_date LIKE '2025-03%'` | JOIN operations |
| "Show total sales per customer" | `SELECT c.name, SUM(o.amount) as total_sales FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name` | Complex aggregations |

## 🔧 Development

### **Local Development**
```bash
cd frontend
npm start
```

### **Building for Production**
```bash
npm run build
```

### **Customization**

#### **Styling**
- Edit `src/App.js` for component styling
- Modify Material-UI theme in `src/index.js`
- Add custom CSS as needed

#### **API Configuration**
- Update `API_BASE_URL` in `src/App.js`
- Modify API endpoints as needed
- Add new API calls for additional features

#### **Components**
- Add new React components in `src/`
- Import Material-UI components as needed
- Extend functionality with additional features

## 🐛 Troubleshooting

### **Common Issues**

1. **Port Conflicts**
   ```
   Error: Port 5000 is in use
   Solution: Use port 5001 or change in api.py
   ```

2. **API Connection**
   ```
   Error: Cannot connect to API
   Solution: Ensure Flask server is running
   ```

3. **Build Errors**
   ```
   Error: npm build fails
   Solution: Check dependencies and try npm install
   ```

4. **CORS Issues**
   ```
   Error: CORS policy blocks requests
   Solution: Ensure Flask-CORS is properly configured
   ```

### **Debugging**

1. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Check Network tab for API calls

2. **Check Server Logs**
   - Monitor Flask server output
   - Look for Python errors
   - Verify API responses

3. **Test API Directly**
   ```bash
   curl http://localhost:5001/api/health
   curl http://localhost:5001/api/examples
   ```

## 🎉 Benefits for Zero-Shot Testing

### **Visual Feedback**
- **Real-time Results**: See SQL generation instantly
- **Syntax Highlighting**: Easy to read generated SQL
- **Data Visualization**: Clear table display of results

### **User Experience**
- **Intuitive Interface**: Natural language input
- **Quick Examples**: One-click testing
- **Copy Functionality**: Easy SQL sharing

### **Comprehensive Testing**
- **Multiple Interfaces**: React, Streamlit, and CLI
- **Error Handling**: Robust error display
- **Health Monitoring**: System status indicators

### **Educational Value**
- **Schema Explorer**: Understand database structure
- **Query Explanations**: Learn what SQL does
- **Interactive Learning**: Hands-on testing

## 🔮 Future Enhancements

- [ ] **Query History**: Save and replay previous queries
- [ ] **Export Results**: Download data as CSV/Excel
- [ ] **Charts**: Visualize query results
- [ ] **Voice Input**: Speech-to-text for queries
- [ ] **Query Templates**: Pre-built complex queries
- [ ] **Multi-database Support**: Switch between databases
- [ ] **User Authentication**: Multi-user support
- [ ] **Query Analytics**: Track usage patterns

---

**🎯 The React frontend provides an excellent interface for testing zero-shot prompting capabilities with a modern, professional web application!**
