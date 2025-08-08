import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Search as SearchIcon,
  Code as CodeIcon,
  TableChart as TableIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  ContentCopy as CopyIcon,
  PlayArrow as PlayIcon
} from '@mui/icons-material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [databaseInfo, setDatabaseInfo] = useState(null);
  const [examples, setExamples] = useState([]);
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    fetchHealthStatus();
    fetchDatabaseInfo();
    fetchExamples();
  }, []);

  const fetchHealthStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setHealthStatus(response.data);
    } catch (error) {
      console.error('Health check failed:', error);
    }
  };

  const fetchDatabaseInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/database-info`);
      setDatabaseInfo(response.data);
    } catch (error) {
      console.error('Failed to fetch database info:', error);
    }
  };

  const fetchExamples = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/examples`);
      setExamples(response.data.examples);
    } catch (error) {
      console.error('Failed to fetch examples:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        query: query.trim()
      });

      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'An error occurred while processing your query.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const formatData = (data) => {
    if (!data || data.length === 0) return 'No data found.';
    
    const columns = Object.keys(data[0]);
    const rows = data.map(row => columns.map(col => row[col]));
    
    return { columns, rows };
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          🔍 SQL Assistant LLM
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Ask questions in natural language and get SQL results instantly!
        </Typography>
        
        {/* Health Status */}
        {healthStatus && (
          <Box sx={{ mt: 2 }}>
            <Chip
              label={`API: ${healthStatus.status}`}
              color={healthStatus.assistant_ready ? 'success' : 'error'}
              size="small"
              sx={{ mr: 1 }}
            />
            <Chip
              label={`Gemini API: ${healthStatus.api_key_configured ? 'Ready' : 'Not Configured'}`}
              color={healthStatus.api_key_configured ? 'success' : 'warning'}
              size="small"
            />
          </Box>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* Main Query Section */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              <SearchIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Ask Your Question
            </Typography>
            
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                multiline
                rows={3}
                variant="outlined"
                placeholder="e.g., How many customers signed up in July?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
                sx={{ mb: 2 }}
              />
              
              <Button
                type="submit"
                variant="contained"
                size="large"
                disabled={loading || !query.trim()}
                startIcon={loading ? <CircularProgress size={20} /> : <PlayIcon />}
                sx={{ mb: 2 }}
              >
                {loading ? 'Processing...' : 'Execute Query'}
              </Button>
            </form>

            {/* Error Display */}
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}

            {/* Results Display */}
            {result && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  📊 Results ({result.row_count} rows)
                </Typography>
                
                {/* SQL Query */}
                <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Generated SQL:
                    </Typography>
                    <Tooltip title="Copy SQL">
                      <IconButton size="small" onClick={() => copyToClipboard(result.sql)}>
                        <CopyIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                  <SyntaxHighlighter language="sql" style={tomorrow} customStyle={{ margin: 0 }}>
                    {result.sql}
                  </SyntaxHighlighter>
                </Paper>

                {/* Explanation */}
                <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: 'blue.50' }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    💡 Explanation:
                  </Typography>
                  <Typography variant="body2">
                    {result.explanation}
                  </Typography>
                </Paper>

                {/* Data Table */}
                {result.data && result.data.length > 0 && (
                  <Paper elevation={1} sx={{ overflow: 'auto' }}>
                    <Box sx={{ p: 2 }}>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        📋 Query Results:
                      </Typography>
                      <Box sx={{ overflow: 'auto', maxHeight: 400 }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                          <thead>
                            <tr style={{ backgroundColor: '#f5f5f5' }}>
                              {Object.keys(result.data[0]).map((column) => (
                                <th key={column} style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>
                                  {column}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {result.data.map((row, index) => (
                              <tr key={index}>
                                {Object.values(row).map((value, colIndex) => (
                                  <td key={colIndex} style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {String(value)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </Box>
                    </Box>
                  </Paper>
                )}
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Examples */}
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              💡 Quick Examples
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {examples.map((example, index) => (
                <Card key={index} variant="outlined" sx={{ cursor: 'pointer' }}>
                  <CardContent sx={{ py: 1, px: 2 }}>
                    <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                      {example.query}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {example.description}
                    </Typography>
                  </CardContent>
                  <CardActions sx={{ py: 0, px: 2, pb: 1 }}>
                    <Button
                      size="small"
                      onClick={() => handleExampleClick(example.query)}
                      startIcon={<PlayIcon />}
                    >
                      Try This
                    </Button>
                  </CardActions>
                </Card>
              ))}
            </Box>
          </Paper>

          {/* Database Info */}
          {databaseInfo && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                <TableIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Database Schema
              </Typography>
              
              {Object.entries(databaseInfo.schema).map(([tableName, columns]) => (
                <Accordion key={tableName} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle2">
                      {tableName} ({columns.length} columns)
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {columns.map((column) => (
                        <Chip
                          key={column}
                          label={column}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
