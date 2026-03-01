# PaymentPulse - Conversational AI for UPI Transaction Analysis

![InsightX Banner](https://img.shields.io/badge/InsightX-AI%20Analytics-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw2IDhIMTBWMTRINkwxMiAyMkwxOCAxNEgxNFY4SDE4TDEyIDJaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==)

A premier hackathon project for **InsightX by Techfest, IIT Bombay** - Building a conversational AI system that democratizes data access for digital payment analytics.

## 🎯 Project Overview

PaymentPulse transforms complex UPI transaction data into actionable insights through natural language conversations. Business leaders can now query 250,000+ transactions without writing a single line of SQL!

### Key Features

✨ **Natural Language Processing** - Ask questions in plain English
- "What's the average transaction amount for Food category?"
- "Compare iOS vs Android performance"
- "Show me peak hours for Entertainment transactions"

📊 **Intelligent Analytics Engine**
- Real-time statistical analysis
- Pattern recognition and trend detection
- Comparative analysis across multiple dimensions
- Risk and operational metrics

🎨 **Beautiful Modern UI**
- Responsive chat interface with glassmorphism design
- Interactive data visualizations (charts, graphs, pie charts)
- Real-time typing indicators and animations
- Mobile-friendly responsive design

🧠 **Context-Aware AI**
- Maintains conversation context
- Handles follow-up questions
- Provides explainable insights with supporting statistics
- Graceful handling of ambiguous queries

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React UI      │ ←──→ │   Flask API      │ ←──→ │  CSV Dataset    │
│  (Frontend)     │      │   (Backend)      │      │  (250K rows)    │
│                 │      │                  │      │                 │
│ - Chat Interface│      │ - NLP Processing │      │ - Transactions  │
│ - Visualizations│      │ - Query Analysis │      │ - User Data     │
│ - Stats Display │      │ - Data Analytics │      │ - Metadata      │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

### Tech Stack

**Backend:**
- Flask (Python web framework)
- Pandas (Data analysis)
- NumPy (Numerical computing)
- Custom NLP engine for query parsing

**Frontend:**
- React 18 (UI framework)
- Vite (Build tool)
- Tailwind CSS (Styling)
- Recharts (Data visualization)
- Axios (API communication)
- Lucide React (Icons)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
cd /path/to/insighx2
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install
```

4. **Set up environment variables** (Optional)
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key if you want LLM integration
```

### Running the Application

**Option 1: Run both servers separately**

Terminal 1 - Backend:
```bash
python app.py
```

Terminal 2 - Frontend:
```bash
npm run dev
```

**Option 2: Use the convenience script**
```bash
chmod +x run.sh
./run.sh
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📖 Usage Examples

### Sample Queries

**Descriptive & Temporal Analysis:**
```
- "What is the average transaction amount for Food category?"
- "Show me peak hours for Entertainment transactions"
- "What are the busiest days of the week?"
```

**Comparative Analysis:**
```
- "Compare iOS vs Android transaction performance"
- "Show me the difference between 5G and WiFi success rates"
- "Compare weekend vs weekday transaction patterns"
```

**User Segmentation:**
```
- "What's the transaction distribution by age group?"
- "Show me top 5 states by transaction volume"
- "Analyze transactions for 26-35 age group"
```

**Risk & Operational Metrics:**
```
- "What is the overall failure rate?"
- "Show me transactions flagged for fraud"
- "Which categories have the highest failure rates?"
```

## 🎯 Data Dimensions

The system analyzes transactions across multiple dimensions:

### Transaction Attributes
- **ID**: Unique transaction identifier
- **Timestamp**: Date and time of transaction
- **Type**: P2P, P2M, Bill Payment, Recharge
- **Amount**: Transaction value in INR
- **Status**: SUCCESS or FAILURE

### Merchant & Category
- **Categories**: Food, Entertainment, Grocery, Fuel, Shopping, Utilities, Transport, Healthcare, Other
- **Merchant Type**: Various business categories

### User Demographics
- **Age Groups**: 18-25, 26-35, 36-45, 46-55, 56+
- **States**: Delhi, Maharashtra, Karnataka, Tamil Nadu, Gujarat, etc.
- **Banks**: SBI, HDFC, ICICI, Axis, PNB, etc.

### Technical Attributes
- **Device Type**: Android, iOS, Web
- **Network Type**: 5G, 4G, 3G, WiFi
- **Fraud Flag**: Binary indicator for suspicious transactions

### Temporal Attributes
- **Hour of Day**: 0-23
- **Day of Week**: Monday-Sunday
- **Weekend Flag**: Binary indicator

## 📊 API Endpoints

### `GET /api/health`
Check API health status
```json
{
  "status": "healthy",
  "data_loaded": true,
  "total_transactions": 250000
}
```

### `GET /api/stats`
Get overall dataset statistics
```json
{
  "total_transactions": 250000,
  "total_volume": 450000000.00,
  "avg_transaction": 1800.50,
  "success_rate": 95.5,
  "fraud_rate": 0.8
}
```

### `POST /api/query`
Process natural language query
```json
{
  "query": "What's the average transaction for Food?",
  "history": []
}
```

Response:
```json
{
  "success": true,
  "query": "What's the average transaction for Food?",
  "response": {
    "answer": "Markdown formatted response...",
    "data": { "average": 856.34, "total_transactions": 15234 },
    "visualization": {
      "type": "bar",
      "data": [...],
      "xKey": "hour_of_day",
      "yKey": "amount (INR)",
      "title": "Average Amount by Hour"
    }
  }
}
```

## 🧠 Query Intelligence

The system uses a sophisticated NLP pipeline:

1. **Intent Classification** - Identifies query type (average, comparison, trend, etc.)
2. **Entity Extraction** - Extracts filters (category, device, state, age group)
3. **Context Management** - Maintains conversation history
4. **Response Generation** - Creates human-readable insights with statistics
5. **Visualization Selection** - Chooses appropriate chart type

### Supported Intents
- Average calculations
- Total/sum aggregations
- Count queries
- Peak time analysis
- Comparisons (devices, networks, categories)
- Trend analysis
- Failure rate calculations
- Fraud detection
- Distribution analysis
- Top/bottom performers
- Percentage calculations

## 🎨 UI Features

### Modern Design Elements
- **Glassmorphism** - Frosted glass aesthetic with backdrop blur
- **Gradient Backgrounds** - Dynamic animated gradients
- **Smooth Animations** - Fade-ins, slide-ups, and transitions
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Dark Mode** - Easy on the eyes with blue-tinted dark theme

### Interactive Components
- **Chat Interface** - Real-time conversation with AI
- **Suggested Queries** - One-click question templates
- **Live Stats Dashboard** - Key metrics at a glance
- **Interactive Charts** - Hover tooltips and smooth animations
- **Status Indicators** - Real-time connection status

## 🔧 Development

### Project Structure
```
insighx2/
├── app.py                      # Flask backend
├── upi_transactions_2024.csv   # Dataset
├── requirements.txt            # Python dependencies
├── package.json                # Node dependencies
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind CSS config
├── index.html                 # HTML entry point
├── src/
│   ├── main.jsx               # React entry point
│   ├── App.jsx                # Main App component
│   ├── index.css              # Global styles
│   └── components/
│       ├── ChatMessage.jsx    # Message bubble component
│       ├── Visualization.jsx  # Chart component
│       ├── StatsCard.jsx      # Stats display component
│       └── SuggestedQueries.jsx # Query suggestions
└── README.md
```

### Adding New Features

**To add a new query intent:**
1. Add intent keywords to `_classify_intent()` in `app.py`
2. Create analysis method (e.g., `_analyze_new_intent()`)
3. Add routing in `_generate_response()`

**To add a new visualization type:**
1. Add chart type to `Visualization.jsx`
2. Import required Recharts component
3. Implement rendering logic in `renderChart()`

## 🚧 Future Enhancements

- [ ] OpenAI GPT-4 integration for advanced NLP
- [ ] Real-time data streaming support
- [ ] Export insights to PDF/Excel
- [ ] Advanced ML models for anomaly detection
- [ ] Multi-language support
- [ ] Voice input capability
- [ ] Custom dashboard builder
- [ ] Data filtering UI
- [ ] Scheduled reports
- [ ] User authentication

## 📝 License

This project is built for the InsightX Hackathon by Techfest, IIT Bombay.

## 🙏 Acknowledgments

- **Techfest, IIT Bombay** - For organizing InsightX hackathon
- **React & Vite** - Modern frontend tooling
- **Flask** - Lightweight Python web framework
- **Recharts** - Beautiful data visualization library
- **Tailwind CSS** - Utility-first CSS framework

## 📧 Support

For questions or issues, please open an issue on the repository or contact the development team.

---

**Built with ❤️ for InsightX Hackathon**

*Democratizing data access through conversational AI*
