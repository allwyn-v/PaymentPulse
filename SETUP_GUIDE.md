# InsightX - Setup & Usage Guide

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Pandas (data analysis)
- NumPy (numerical computing)

### Step 2: Install Node.js Dependencies
```bash
npm install
```

This installs:
- React & React DOM
- Vite (build tool)
- Tailwind CSS (styling)
- Recharts (charts)
- Axios (API calls)
- Lucide React (icons)

### Step 3: Run the Application
```bash
# Option A: Use the convenience script
./run.sh

# Option B: Run manually in separate terminals
# Terminal 1:
python app.py

# Terminal 2:
npm run dev
```

## 🌐 Access the Application

Once running:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 💬 Sample Conversations

### Example 1: Basic Query
```
You: What is the average transaction amount for Food category?

AI: 📊 Average Transaction Analysis

The average transaction amount for Food is ₹856.34.

Key Insights:
- Total transactions analyzed: 15,234
- Median amount: ₹742.50
- Standard deviation: ₹445.23
- Amount range: ₹50.00 - ₹8,500.00

[Interactive chart showing hourly breakdown]
```

### Example 2: Comparison Query
```
You: Compare iOS vs Android performance

AI: 📱 Device Comparison: Android vs iOS

Transaction Volume:
- Android: 187,450 transactions (74.9%)
- iOS: 62,550 transactions (25.1%)

Average Transaction Amount:
- Android: ₹1,795.23
- iOS: ₹1,812.45

Success Rate:
- Android: 95.2%
- iOS: 96.8%

[Interactive bar chart comparing both platforms]
```

### Example 3: Time-Based Analysis
```
You: Show me peak hours for Entertainment transactions

AI: ⏰ Peak Time Analysis

For transactions for Entertainment:

Peak Hour: 19:00 with 2,345 transactions
Peak Day: Saturday with 18,234 transactions

Additional Insights:
- Weekend vs Weekday: 42,123 vs 38,901
- Most active period: Evening (5 PM - 9 PM)

[Interactive line chart showing hourly distribution]
```

### Example 4: Risk Analysis
```
You: What is the fraud rate?

AI: 🚨 Fraud Analysis

Total flagged transactions: 2,145 (0.86% of all transactions)

Key Insights:
- Average flagged amount: ₹3,245.67
- Average normal amount: ₹1,785.34
- Difference: ₹1,460.33

Top Categories with Fraud Flags:
- Shopping: 567 cases
- Entertainment: 432 cases
- Other: 298 cases
- Fuel: 234 cases
- Food: 187 cases

[Interactive bar chart showing fraud by category]
```

## 🎯 Query Categories

### 1. Descriptive Queries
- "What is the average transaction amount?"
- "How many transactions are in the dataset?"
- "What is the total transaction volume?"
- "Show me the distribution of transactions by category"

### 2. Temporal Analysis
- "What are the peak hours for transactions?"
- "Show me the busiest day of the week"
- "Compare weekend vs weekday transactions"
- "What time has the highest transaction volume?"

### 3. Comparative Analysis
- "Compare iOS vs Android"
- "Show the difference between 5G and WiFi"
- "Compare P2P vs P2M transactions"
- "Which network type performs better?"

### 4. User Segmentation
- "Show transactions for 26-35 age group"
- "What are the top states by transaction volume?"
- "Analyze transactions from Delhi"
- "Show the distribution by age group"

### 5. Risk & Operations
- "What is the failure rate?"
- "Show me fraud-flagged transactions"
- "Which category has the highest failure rate?"
- "What percentage of transactions are successful?"

### 6. Top/Bottom Analysis
- "Show me the top 10 states"
- "What are the highest transaction amounts?"
- "Top categories by revenue"
- "Which merchant category has the most transactions?"

## 🎨 UI Features

### Chat Interface
- **Auto-scrolling**: Automatically scrolls to latest message
- **Typing indicators**: Shows when AI is processing
- **Markdown support**: Bold text, lists, and formatting
- **Timestamps**: Each message shows time sent

### Visualizations
- **Bar Charts**: For comparisons and distributions
- **Line Charts**: For trends over time
- **Pie Charts**: For proportional data
- **Interactive Tooltips**: Hover over charts for details

### Stats Dashboard
- **Real-time metrics**: Updated from live data
- **Color-coded cards**: Different colors for different metrics
- **Hover effects**: Interactive card animations

### Suggested Queries
- **One-click questions**: Pre-written queries to get started
- **Contextual suggestions**: Based on conversation state
- **Easy exploration**: Discover what you can ask

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Python Dependencies Issue
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Node Dependencies Issue
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CSV File Not Found
- Ensure `upi_transactions_2024.csv` is in the project root
- Check file permissions: `chmod 644 upi_transactions_2024.csv`

## 📊 Dataset Statistics

- **Total Transactions**: 250,000
- **Date Range**: January 1, 2024 - December 31, 2024
- **Transaction Types**: P2P, P2M, Bill Payment, Recharge
- **Categories**: 9 (Food, Entertainment, Grocery, etc.)
- **States**: 10+ major Indian states
- **Device Types**: Android, iOS, Web
- **Network Types**: 5G, 4G, 3G, WiFi

## 🔐 Security Notes

- API runs locally (no external exposure by default)
- No authentication required (local development)
- CORS enabled for localhost:3000
- CSV data loaded in-memory (no database required)

## 📈 Performance

- Query response time: ~100-500ms
- Dataset loading time: ~2-3 seconds
- Frontend build time: ~10-15 seconds
- Memory usage: ~500MB (with dataset loaded)

## 🎓 Learning Resources

### Understanding the Code

**Backend (`app.py`):**
- `QueryAnalyzer` class: Main NLP engine
- `_classify_intent()`: Determines query type
- `_extract_entities()`: Finds filters in query
- `_generate_response()`: Creates answer with data

**Frontend (`src/App.jsx`):**
- State management with React hooks
- API communication with Axios
- Real-time updates and animations
- Component composition

**Visualizations (`src/components/Visualization.jsx`):**
- Recharts library integration
- Dynamic chart type selection
- Custom tooltips and styling

## 🚀 Next Steps

1. **Explore**: Try the suggested queries
2. **Experiment**: Ask your own questions
3. **Analyze**: Look at the generated visualizations
4. **Extend**: Add new features (see README.md)

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Check error messages in browser console
4. Verify backend logs in terminal

---

**Happy Analyzing! 📊✨**
