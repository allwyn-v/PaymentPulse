# InsightX - Technical Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                             │
│                         (React Frontend)                             │
│                                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐                │
│  │   Chat UI   │  │ Stats Cards  │  │Visualizations│               │
│  │             │  │              │  │   (Charts)   │               │
│  │ - Messages  │  │ - Metrics    │  │ - Bar        │               │
│  │ - Input     │  │ - Real-time  │  │ - Line       │               │
│  │ - Suggested │  │ - Animated   │  │ - Pie        │               │
│  └─────────────┘  └──────────────┘  └─────────────┘                │
│                            │                                         │
│                            │ HTTP/JSON (Axios)                       │
│                            ▼                                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API
                              │
┌─────────────────────────────┼─────────────────────────────────────────┐
│                             ▼                                         │
│                      FLASK WEB SERVER                                 │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                     API ENDPOINTS                               │ │
│  │                                                                 │ │
│  │  GET  /api/health    - Health check & status                   │ │
│  │  GET  /api/stats     - Overall dataset statistics              │ │
│  │  POST /api/query     - Process natural language query          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                             │                                         │
│                             ▼                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                   QUERY ANALYZER (NLP Engine)                  │ │
│  │                                                                 │ │
│  │  1. Intent Classification                                      │ │
│  │     ├─ Average calculations                                    │ │
│  │     ├─ Comparisons                                            │ │
│  │     ├─ Peak time analysis                                     │ │
│  │     ├─ Failure/Fraud detection                                │ │
│  │     └─ Distribution analysis                                  │ │
│  │                                                                 │ │
│  │  2. Entity Extraction                                          │ │
│  │     ├─ Categories (Food, Entertainment, etc.)                 │ │
│  │     ├─ Devices (iOS, Android, Web)                           │ │
│  │     ├─ Networks (5G, 4G, WiFi)                               │ │
│  │     ├─ States, Age groups, etc.                              │ │
│  │     └─ Temporal filters                                       │ │
│  │                                                                 │ │
│  │  3. Context Management                                         │ │
│  │     └─ Conversation history tracking                          │ │
│  │                                                                 │ │
│  │  4. Response Generation                                        │ │
│  │     ├─ Statistical analysis                                   │ │
│  │     ├─ Insights extraction                                    │ │
│  │     ├─ Visualization selection                                │ │
│  │     └─ Markdown formatting                                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                             │                                         │
│                             ▼                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    DATA ANALYTICS LAYER                        │ │
│  │                      (Pandas/NumPy)                            │ │
│  │                                                                 │ │
│  │  • Filtering & Aggregation                                     │ │
│  │  • Statistical Computations                                    │ │
│  │  • Grouping & Pivoting                                        │ │
│  │  • Time Series Analysis                                        │ │
│  │  • Pattern Recognition                                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                             │                                         │
│                             ▼                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    DATA LAYER (In-Memory)                      │ │
│  │                                                                 │ │
│  │  DataFrame: 250,000 rows × 17 columns                         │ │
│  │  Source: upi_transactions_2024.csv                            │ │
│  └────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. User Input
   │
   ├─→ "What is the average transaction for Food?"
   │
   ▼
2. Frontend Processing
   │
   ├─→ Input validation
   ├─→ Add to message history
   ├─→ Show loading indicator
   │
   ▼
3. API Request (POST /api/query)
   │
   ├─→ { "query": "...", "history": [...] }
   │
   ▼
4. Backend Processing
   │
   ├─→ Intent: "average"
   ├─→ Entities: { category: "Food" }
   ├─→ Filter: df[df['merchant_category'] == 'Food']
   ├─→ Compute: mean(), median(), std()
   ├─→ Generate: response text + visualization data
   │
   ▼
5. API Response
   │
   ├─→ {
   │     "success": true,
   │     "response": {
   │       "answer": "📊 Average Transaction Analysis...",
   │       "data": { "average": 856.34, ... },
   │       "visualization": {
   │         "type": "line",
   │         "data": [...],
   │         "xKey": "hour_of_day",
   │         "yKey": "amount (INR)"
   │       }
   │     }
   │   }
   │
   ▼
6. Frontend Rendering
   │
   ├─→ Display AI message with markdown
   ├─→ Render interactive chart
   ├─→ Auto-scroll to message
   ├─→ Update conversation history
   │
   ▼
7. User sees result with visualization
```

## Component Hierarchy

```
App (Main Application)
│
├── Header
│   ├── Logo & Title
│   └── Status Indicator
│
├── Stats Dashboard
│   ├── StatsCard (Total Transactions)
│   ├── StatsCard (Total Volume)
│   ├── StatsCard (Success Rate)
│   └── StatsCard (Avg Transaction)
│
├── Chat Container
│   │
│   ├── Message List (scrollable)
│   │   └── For each message:
│   │       ├── ChatMessage
│   │       │   ├── Avatar (User/Bot)
│   │       │   ├── Message Bubble
│   │       │   │   ├── Markdown Content
│   │       │   │   └── Timestamp
│   │       │   
│   │       └── Visualization (if present)
│   │           └── Recharts Component
│   │               ├── BarChart
│   │               ├── LineChart
│   │               └── PieChart
│   │
│   ├── Suggested Queries (initial state)
│   │   └── Query Buttons
│   │
│   └── Input Area
│       ├── Textarea
│       └── Send Button
│
└── Footer
    └── Credits & Info
```

## Technology Stack Details

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework |
| Vite | 5.0.8 | Build tool & dev server |
| Tailwind CSS | 3.3.6 | Utility-first CSS |
| Recharts | 2.10.3 | Data visualization |
| Axios | 1.6.2 | HTTP client |
| Lucide React | 0.294.0 | Icon library |
| Framer Motion | 10.16.16 | Animations |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-CORS | 4.0.0 | Cross-origin support |
| Pandas | 2.1.3 | Data manipulation |
| NumPy | 1.26.2 | Numerical computing |
| Python | 3.8+ | Runtime environment |

## Key Algorithms

### 1. Intent Classification
```python
def _classify_intent(self, query):
    # Keywords-based classification
    intents = {
        'average': ['average', 'avg', 'mean'],
        'comparison': ['compare', 'vs', 'versus'],
        'peak_time': ['peak', 'highest', 'busiest'],
        # ... more intents
    }
    
    for intent_type, keywords in intents.items():
        if any(keyword in query for keyword in keywords):
            return intent_type
```

### 2. Entity Extraction
```python
def _extract_entities(self, query):
    entities = {}
    
    # Pattern matching for categories, devices, states, etc.
    for category in categories:
        if category in query:
            entities['category'] = category
    
    # Similar for other entity types
    return entities
```

### 3. Data Filtering
```python
def _apply_filters(self, entities):
    filtered = self.df.copy()
    
    if 'category' in entities:
        filtered = filtered[filtered['merchant_category'] == entities['category']]
    
    # Apply more filters based on entities
    return filtered
```

### 4. Statistical Analysis
```python
def _analyze_average(self, df, entities, query):
    avg_amount = df['amount (INR)'].mean()
    median = df['amount (INR)'].median()
    std_dev = df['amount (INR)'].std()
    
    # Generate insights and visualization data
    return response
```

## Performance Optimizations

1. **Data Loading**: CSV loaded once at startup
2. **In-Memory Processing**: All operations on Pandas DataFrame
3. **Lazy Visualization**: Charts rendered only when needed
4. **Request Debouncing**: Prevents duplicate API calls
5. **Efficient Filtering**: Pandas vectorized operations

## Security Considerations

- CORS restricted to localhost:3000
- No authentication (local development)
- Input validation on backend
- No sensitive data exposure
- Read-only CSV access

## Scalability Notes

For production deployment:
- Add database layer (PostgreSQL/MongoDB)
- Implement caching (Redis)
- Add authentication (JWT)
- Use production WSGI server (Gunicorn)
- Enable rate limiting
- Add monitoring & logging
- Containerize with Docker
- Deploy with Kubernetes

---

**Built for InsightX Hackathon**
