"""
InsightX Backend - Conversational AI for UPI Transaction Analysis
Flask API with intelligent query processing and data analytics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Try to import Gemini
GEMINI_AVAILABLE = False
gemini_client = None
try:
    import google.generativeai as genai
    gemini_api_key = os.getenv('GEMINI_API_KEY', '').strip()
    if gemini_api_key and gemini_api_key != 'your-gemini-api-key-here':
        try:
            genai.configure(api_key=gemini_api_key)
            gemini_client = genai.GenerativeModel('gemini-2.0-flash')
            GEMINI_AVAILABLE = True
            print("✓ Gemini API enabled")
        except Exception as e:
            print(f"ℹ Gemini initialization failed: {str(e)}")
            print("ℹ Using rule-based NLP instead")
    else:
        print("ℹ Gemini API key not configured - using rule-based NLP")
except ImportError:
    print("ℹ Gemini library not installed - using rule-based NLP")


# Load transaction data
df = None

def load_data():
    global df
    try:
        df = pd.read_csv('upi_transactions_2024.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"✓ Loaded {len(df)} transactions")
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False


class QueryAnalyzer:
    """Advanced NLP query analyzer for business intelligence queries"""
    
    def __init__(self, df):
        self.df = df
    
    def _convert_types(self, obj):
        """Convert numpy/pandas types to native Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {k: self._convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
        
    def analyze_query(self, query, conversation_history=None):
        """Main query analysis pipeline"""
        query_lower = query.lower()
        
        # Try Gemini if available
        if GEMINI_AVAILABLE and gemini_client:
            try:
                response = self._analyze_with_gemini(query, conversation_history)
                if response:
                    return self._convert_types(response)
            except Exception as e:
                print(f"Gemini error: {e}, falling back to rule-based")
        
        # Fallback to rule-based NLP
        intent = self._classify_intent(query_lower)
        entities = self._extract_entities(query_lower)
        response = self._generate_response(intent, entities, query_lower)
        
        return self._convert_types(response)
    
    def _analyze_with_gemini(self, query, conversation_history):
        """Use Gemini to understand query and generate analysis"""
        
        # Get dataset schema with real-time stats
        total_records = len(self.df)
        categories = sorted(self.df['merchant_category'].unique())
        devices = sorted(self.df['device_type'].unique())
        networks = sorted(self.df['network_type'].unique())
        
        schema_info = f"""
UPI TRANSACTION DATASET:
- Total Records: {total_records:,} transactions
- Date Range: {self.df['timestamp'].min().date()} to {self.df['timestamp'].max().date()}
- Available Columns: transaction_id, timestamp, amount, merchant_category, device_type, 
  network_type, sender_state, transaction_status, fraud_flag, hour_of_day, day_of_week, is_weekend

AVAILABLE VALUES:
- Categories ({len(categories)}): {', '.join(categories)}
- Devices ({len(devices)}): {', '.join(devices)}
- Networks ({len(networks)}): {', '.join(networks)}
- Transaction Status: SUCCESS, FAILURE
- Fraud Flag: 0 (normal), 1 (flagged)
"""
        
        # Enhanced system prompt for Gemini
        system_prompt = f"""You are an advanced AI data analyst for PaymentPulse UPI transaction analytics.

BUSINESS CONTEXT:
- UPI is India's real-time digital payment system
- Transactions occur 24/7 across multiple merchant categories
- Key business metrics: transaction success rate, fraud detection, peak usage times, category trends
- Important segments: device type (Android/iOS/Web), network quality (5G/4G/WiFi), geographic location, states

{schema_info}

YOUR TASK:
1. INFER INTENT from even vague queries - don't default to "general" too easily
2. Extract dimension from context clues
3. Make reasonable assumptions about what user wants
4. Return ONLY a valid JSON response (no markdown, no explanations)

ANALYSIS TYPES:
- average: Calculate mean transaction amounts
- count: Count number of transactions  
- total: Sum of transaction amounts
- comparison: Compare two segments (e.g., iOS vs Android, 5G vs WiFi)
- peak_time: Identify busiest hours/days
- fraud: Analyze fraud-flagged transactions
- failure_rate: Calculate transaction failure rates
- distribution: Show breakdown across categories/segments
- top: Find top performers by dimension (categories, states, devices, etc.)
- general: ONLY use this if query is completely generic (like "tell me about transactions", "overview", "summary")

INFERENCE RULES:
1. "highest", "best", "top" → intent: top
2. "average", "mean", "typical" → intent: average
3. "total", "sum", "altogether" → intent: total
4. "how many", "count", "number" → intent: count
5. "when", "time", "hour", "day" → intent: peak_time
6. "compare", "vs", "versus", "difference" → intent: comparison
7. "fail", "error", "unsuccessful" → intent: failure_rate
8. "fraud", "suspicious", "flagged" → intent: fraud
9. "breakdown", "split", "spread" → intent: distribution
10. "states", "regions", "geography" mentioned → dimension: state
11. "android", "ios", "phones" mentioned → dimension: device
12. "5g", "4g", "wifi", "network" mentioned → dimension: network
13. "categories", "merchants", "food", "shopping" mentioned → dimension: category

EXAMPLES:
- "Tell me about Food" → intent: distribution, dimension: category
- "Anything about states?" → intent: top, dimension: state
- "How's Android doing?" → intent: comparison OR distribution, dimension: device
- "What's highest?" → intent: top (guess dimension based on context, default: category)
- "Give me insights" → intent: general (truly generic)
- "Show me differences" → intent: comparison

RESPONSE FORMAT (JSON only):
{{
    "intent": "average|count|total|comparison|peak_time|fraud|failure_rate|distribution|top|general",
    "dimension": "category|state|device|network|none",
    "entities": {{
        "category": "Food|Entertainment|Grocery|Fuel|Shopping|Utilities|Transport|Healthcare|Other",
        "device": "Android|iOS|Web",
        "network": "5G|4G|3G|WiFi",
        "state": "state name",
        "status": "SUCCESS|FAILURE"
    }},
    "confidence": 0.95
}}

IMPORTANT INSTRUCTIONS:
- ACTIVELY INFER intent - use the INFERENCE RULES above
- Only use intent: "general" if query is TRULY vague with NO context clues
- For ambiguous dimension, prefer: category > state > device > network
- If user says "highest" without context, assume they want to see what's highest (top intent)
- Context matters - "Food" alone means distribution analysis of Food category
- Be confident in reasonable inferences - don't bail to "general" too easily
- Return valid JSON only (no extra text)
"""

        try:
            # Build conversation context
            conversation = []
            if conversation_history:
                for msg in conversation_history[-3:]:  # Last 3 messages
                    role = "user" if msg.get('type') == 'user' else "model"
                    conversation.append({
                        "role": role,
                        "parts": [{"text": msg.get('content', '')[:200]}]
                    })
            
            # Add current query
            conversation.append({
                "role": "user",
                "parts": [{"text": query}]
            })
            
            # Call Gemini API
            response = gemini_client.generate_content(
                contents=conversation,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 500,
                }
            )
            
            ai_response = response.text
            
            # Parse JSON response
            try:
                import json as json_lib
                # Extract JSON from response
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    parsed = json_lib.loads(ai_response[json_start:json_end])
                    intent = parsed.get('intent', 'general')
                    entities = parsed.get('entities', {})
                    dimension = parsed.get('dimension', 'category')
                    
                    if not intent:
                        intent = 'general'
                    
                    # Add dimension to entities for dynamic analysis
                    if dimension and dimension != 'none':
                        entities['dimension'] = dimension
                    
                    # Generate response based on parsed intent
                    return self._generate_response(intent, entities, query.lower())
                else:
                    print(f"Failed to extract JSON from Gemini response: {ai_response}")
                    return None
                    
            except json_lib.JSONDecodeError as e:
                print(f"Failed to parse Gemini response: {ai_response}")
                return None
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    def _classify_intent(self, query):
        """Classify user intent with flexible matching"""
        intents = {
            'average': ['average', 'avg', 'mean', 'typical'],
            'total': ['total', 'sum', 'aggregate', 'all'],
            'count': ['count', 'how many', 'number of'],
            'peak_time': ['peak', 'highest', 'busiest', 'when'],
            'comparison': ['compare', 'vs', 'versus', 'difference'],
            'failure_rate': ['fail', 'failure', 'error', 'unsuccessful'],
            'fraud': ['fraud', 'suspicious', 'flagged'],
            'distribution': ['distribution', 'breakdown', 'split'],
            'top': ['top', 'best', 'leading', 'highest'],
        }
        
        intent_scores = {}
        for intent_type, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in query)
            if score > 0:
                intent_scores[intent_type] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return 'general'
    
    def _extract_entities(self, query):
        """Extract relevant entities from query"""
        entities = {}
        
        # Categories
        categories = {
            'Food': ['food', 'restaurant', 'dining'],
            'Entertainment': ['entertainment', 'movie', 'gaming'],
            'Grocery': ['grocery', 'supermarket'],
            'Fuel': ['fuel', 'petrol', 'gas'],
            'Shopping': ['shopping', 'shop', 'retail'],
        }
        for cat, variations in categories.items():
            if any(var in query for var in variations):
                entities['category'] = cat
                break
        
        # Devices
        devices = {
            'Android': ['android'],
            'iOS': ['ios', 'iphone'],
            'Web': ['web', 'browser'],
        }
        for device, variations in devices.items():
            if any(var in query for var in variations):
                entities['device'] = device
                break
        
        # Networks
        networks = {
            '5G': ['5g'],
            '4G': ['4g'],
            'WiFi': ['wifi'],
        }
        for network, variations in networks.items():
            if any(var in query for var in variations):
                entities['network'] = network
                break
        
        # Status
        if any(word in query for word in ['success', 'successful']):
            entities['status'] = 'SUCCESS'
        elif any(word in query for word in ['fail', 'failure', 'failed']):
            entities['status'] = 'FAILURE'
        
        # States - check if query mentions states
        if any(word in query for word in ['state', 'states', 'state-wise', 'statewise']):
            entities['dimension'] = 'state'
        elif any(word in query for word in ['device', 'devices']):
            entities['dimension'] = 'device'
        
        return entities
    
    def _generate_response(self, intent, entities, query):
        """Generate intelligent response with data analysis"""
        
        try:
            filtered_df = self._apply_filters(entities)
            
            if len(filtered_df) == 0:
                return {
                    'answer': "I couldn't find any transactions matching your criteria.",
                    'data': {},
                    'visualization': None
                }
            
            # Route to appropriate analysis
            if intent == 'average':
                return self._analyze_average(filtered_df, entities)
            elif intent == 'total':
                return self._analyze_total(filtered_df, entities)
            elif intent == 'count':
                return self._analyze_count(filtered_df)
            elif intent == 'peak_time':
                return self._analyze_peak_time(filtered_df)
            elif intent == 'comparison':
                return self._analyze_comparison(filtered_df, query)
            elif intent == 'failure_rate':
                return self._analyze_failure_rate(filtered_df)
            elif intent == 'fraud':
                return self._analyze_fraud(filtered_df)
            elif intent == 'distribution':
                return self._analyze_distribution(filtered_df)
            elif intent == 'top':
                return self._analyze_top(filtered_df, entities)
            else:
                return self._general_analysis(filtered_df)
                
        except Exception as e:
            return {
                'answer': f"I encountered an error: {str(e)}",
                'data': {},
                'visualization': None
            }
    
    def _apply_filters(self, entities):
        """Apply filters based on extracted entities"""
        filtered = self.df.copy()
        
        if 'category' in entities:
            filtered = filtered[filtered['merchant_category'] == entities['category']]
        if 'device' in entities:
            filtered = filtered[filtered['device_type'] == entities['device']]
        if 'network' in entities:
            filtered = filtered[filtered['network_type'] == entities['network']]
        if 'status' in entities:
            filtered = filtered[filtered['transaction_status'] == entities['status']]
        
        return filtered
    
    def _analyze_average(self, df, entities):
        """Analyze average transaction amounts"""
        avg_amount = df['amount (INR)'].mean()
        context = ' for ' + entities.get('category', 'transactions')
        
        answer = f"📊 **Average Transaction Amount{context}**\n\n"
        answer += f"The average amount is **₹{avg_amount:,.2f}**\n\n"
        answer += f"- Total transactions: {len(df):,}\n"
        answer += f"- Median: ₹{df['amount (INR)'].median():,.2f}\n"
        answer += f"- Range: ₹{df['amount (INR)'].min():,.2f} - ₹{df['amount (INR)'].max():,.2f}"
        
        hourly = df.groupby('hour_of_day')['amount (INR)'].mean().reset_index()
        
        return {
            'answer': answer,
            'data': {'average': round(avg_amount, 2)},
            'visualization': {
                'type': 'line',
                'data': hourly.to_dict('records'),
                'xKey': 'hour_of_day',
                'yKey': 'amount (INR)',
                'title': 'Average Amount by Hour'
            }
        }
    
    def _analyze_total(self, df, entities):
        """Calculate total amounts"""
        total = df['amount (INR)'].sum()
        count = len(df)
        avg = df['amount (INR)'].mean()
        
        answer = f"💰 **Total Transaction Volume**\n\n"
        answer += f"Total: **₹{total:,.2f}**\n\n"
        answer += f"- Transactions: {count:,}\n"
        answer += f"- Average: ₹{avg:,.2f}"
        
        return {
            'answer': answer,
            'data': {'total': round(total, 2)},
            'visualization': None
        }
    
    def _analyze_count(self, df):
        """Count transactions"""
        count = len(df)
        
        answer = f"📊 **Transaction Count**\n\n"
        answer += f"Total transactions: **{count:,}**"
        
        return {
            'answer': answer,
            'data': {'count': count},
            'visualization': None
        }
    
    def _analyze_peak_time(self, df):
        """Analyze peak transaction times"""
        hourly = df.groupby('hour_of_day').size().reset_index(name='count')
        peak_hour = hourly.loc[hourly['count'].idxmax()]
        
        answer = f"⏰ **Peak Time Analysis**\n\n"
        answer += f"Peak hour: **{int(peak_hour['hour_of_day'])}:00** with {int(peak_hour['count']):,} transactions"
        
        return {
            'answer': answer,
            'data': {'peak_hour': int(peak_hour['hour_of_day'])},
            'visualization': {
                'type': 'bar',
                'data': hourly.to_dict('records'),
                'xKey': 'hour_of_day',
                'yKey': 'count',
                'title': 'Transaction Volume by Hour'
            }
        }
    
    def _analyze_comparison(self, df, query):
        """Compare different segments"""
        if 'android' in query and 'ios' in query:
            android = df[df['device_type'] == 'Android']
            ios = df[df['device_type'] == 'iOS']
            
            answer = f"📱 **Device Comparison**\n\n"
            answer += f"Android: {len(android):,} transactions (₹{android['amount (INR)'].mean():,.2f} avg)\n"
            answer += f"iOS: {len(ios):,} transactions (₹{ios['amount (INR)'].mean():,.2f} avg)"
            
            comp_data = [
                {'device': 'Android', 'count': len(android), 'avg': android['amount (INR)'].mean()},
                {'device': 'iOS', 'count': len(ios), 'avg': ios['amount (INR)'].mean()}
            ]
        else:
            # Compare by category
            cat_stats = df.groupby('merchant_category').size().reset_index(name='count')
            answer = f"📊 **Category Comparison**\n\n"
            for _, row in cat_stats.head(5).iterrows():
                answer += f"{row['merchant_category']}: {row['count']:,}\n"
            comp_data = cat_stats.to_dict('records')
        
        return {
            'answer': answer,
            'data': {'comparison': comp_data},
            'visualization': {
                'type': 'bar',
                'data': comp_data[:8],
                'xKey': 'device' if 'device' in comp_data[0] else 'merchant_category',
                'yKey': 'count',
                'title': 'Comparison'
            }
        }
    
    def _analyze_failure_rate(self, df):
        """Analyze transaction failure rates"""
        total = len(df)
        failures = len(df[df['transaction_status'] != 'SUCCESS'])
        rate = (failures / total * 100) if total > 0 else 0
        
        answer = f"⚠️ **Failure Rate Analysis**\n\n"
        answer += f"Failure rate: **{rate:.2f}%** ({failures:,} out of {total:,} transactions)"
        
        return {
            'answer': answer,
            'data': {'failure_rate': round(rate, 2)},
            'visualization': None
        }
    
    def _analyze_fraud(self, df):
        """Analyze fraud-flagged transactions"""
        flagged = len(df[df['fraud_flag'] == 1])
        total = len(df)
        rate = (flagged / total * 100) if total > 0 else 0
        
        answer = f"🚨 **Fraud Analysis**\n\n"
        answer += f"Flagged transactions: **{flagged:,}** ({rate:.2f}% of total)"
        
        return {
            'answer': answer,
            'data': {'fraud_count': flagged},
            'visualization': None
        }
    
    def _analyze_distribution(self, df):
        """Analyze distribution across dimensions"""
        dist = df.groupby('merchant_category').size().reset_index(name='count').sort_values('count', ascending=False)
        
        answer = f"📈 **Distribution**\n\n"
        for _, row in dist.head(5).iterrows():
            pct = (row['count'] / len(df)) * 100
            answer += f"{row['merchant_category']}: {row['count']:,} ({pct:.1f}%)\n"
        
        return {
            'answer': answer,
            'data': {'distribution': dist.to_dict('records')},
            'visualization': {
                'type': 'pie',
                'data': dist.head(8).to_dict('records'),
                'xKey': 'merchant_category',
                'yKey': 'count',
                'title': 'Distribution by Category'
            }
        }
    
    def _analyze_top(self, df, entities=None):
        """Analyze top performers by category, state, or device"""
        if entities is None:
            entities = {}
        
        dimension = entities.get('dimension', 'category')
        
        if dimension == 'state':
            # Analyze by state
            if 'sender_state' in df.columns:
                top = df.groupby('sender_state').agg({
                    'transaction id': 'count',
                    'amount (INR)': 'sum'
                }).reset_index().sort_values('amount (INR)', ascending=False).head(10)
                top.columns = ['state', 'transactions', 'total_amount']
                top['rank'] = range(1, len(top) + 1)
                
                answer = f"🏆 **Top 10 States by Transaction Volume**\n\n"
                for _, row in top.iterrows():
                    answer += f"{int(row['rank'])}. {row['state']}: ₹{row['total_amount']:,.0f} ({int(row['transactions'])} transactions)\n"
                
                return {
                    'answer': answer,
                    'data': {'top': top.to_dict('records')},
                    'visualization': {
                        'type': 'bar',
                        'data': top.to_dict('records'),
                        'xKey': 'state',
                        'yKey': 'total_amount',
                        'title': 'Top States by Transaction Volume'
                    }
                }
        
        elif dimension == 'device':
            # Analyze by device
            top = df.groupby('device_type').agg({
                'transaction id': 'count',
                'amount (INR)': 'sum'
            }).reset_index().sort_values('amount (INR)', ascending=False).head(10)
            top.columns = ['device', 'transactions', 'total_amount']
            top['rank'] = range(1, len(top) + 1)
            
            answer = f"📱 **Top Devices by Transaction Volume**\n\n"
            for _, row in top.iterrows():
                answer += f"{int(row['rank'])}. {row['device']}: ₹{row['total_amount']:,.0f} ({int(row['transactions'])} transactions)\n"
            
            return {
                'answer': answer,
                'data': {'top': top.to_dict('records')},
                'visualization': {
                    'type': 'bar',
                    'data': top.to_dict('records'),
                    'xKey': 'device',
                    'yKey': 'total_amount',
                    'title': 'Top Devices by Transaction Volume'
                }
            }
        
        else:
            # Default: Analyze by category
            top = df.groupby('merchant_category').agg({
                'transaction id': 'count',
                'amount (INR)': 'sum'
            }).reset_index().sort_values('amount (INR)', ascending=False).head(10)
            top.columns = ['category', 'transactions', 'total_amount']
            top['rank'] = range(1, len(top) + 1)
            
            answer = f"🏆 **Top Categories by Transaction Volume**\n\n"
            for _, row in top.iterrows():
                answer += f"{int(row['rank'])}. {row['category']}: ₹{row['total_amount']:,.0f} ({int(row['transactions'])} transactions)\n"
            
            return {
                'answer': answer,
                'data': {'top': top.to_dict('records')},
                'visualization': {
                    'type': 'bar',
                    'data': top.to_dict('records'),
                    'xKey': 'category',
                    'yKey': 'total_amount',
                    'title': 'Top Categories by Transaction Volume'
                }
            }
    
    def _general_analysis(self, df):
        """General overview"""
        total_txns = int(len(df))
        total_amount = float(df['amount (INR)'].sum())
        avg_amount = float(df['amount (INR)'].mean())
        
        answer = f"📊 **Transaction Overview**\n\n"
        answer += f"- Total Transactions: {total_txns:,}\n"
        answer += f"- Total Volume: ₹{total_amount:,.2f}\n"
        answer += f"- Average Amount: ₹{avg_amount:,.2f}"
        
        return {
            'answer': answer,
            'data': {
                'total_transactions': total_txns,
                'total_volume': round(total_amount, 2),
                'average_amount': round(avg_amount, 2)
            },
            'visualization': None
        }


# Global query analyzer instance
analyzer = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_loaded': df is not None,
        'total_transactions': len(df) if df is not None else 0
    })


@app.route('/api/query', methods=['POST'])
def process_query():
    """Process natural language query"""
    global analyzer
    
    try:
        data = request.json
        query = data.get('query', '')
        conversation_history = data.get('history', [])
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if analyzer is None:
            return jsonify({'error': 'Data not loaded'}), 500
        
        # Process query
        response = analyzer.analyze_query(query, conversation_history)
        
        return jsonify({
            'success': True,
            'query': query,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall dataset statistics"""
    try:
        if df is None:
            return jsonify({'error': 'Data not loaded'}), 500
        
        stats = {
            'total_transactions': int(len(df)),
            'total_volume': float(df['amount (INR)'].sum()),
            'avg_transaction': float(df['amount (INR)'].mean()),
            'success_rate': float((df['transaction_status'] == 'SUCCESS').sum() / len(df) * 100),
            'fraud_rate': float((df['fraud_flag'] == 1).sum() / len(df) * 100),
            'categories': df['merchant_category'].nunique(),
            'states': df['sender_state'].nunique(),
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting InsightX Backend...")
    
    if load_data():
        analyzer = QueryAnalyzer(df)
        print("✓ Query analyzer initialized")
        print(f"✓ Ready to analyze {len(df):,} transactions")
        app.run(debug=True, port=5000)
    else:
        print("✗ Failed to start: Could not load data")

