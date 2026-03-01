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

# Try to import OpenAI
OPENAI_AVAILABLE = False
openai_client = None
try:
    from openai import OpenAI
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if api_key and api_key != 'your_openai_api_key_here':
        try:
            openai_client = OpenAI(api_key=api_key)
            OPENAI_AVAILABLE = True
            print("✓ OpenAI API enabled")
        except Exception as e:
            print(f"ℹ OpenAI initialization failed: {str(e)}")
            print("ℹ Using rule-based NLP instead")
    else:
        print("ℹ OpenAI API key not configured - using rule-based NLP")
except ImportError:
    print("ℹ OpenAI library not installed - using rule-based NLP")

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
        
        # Try OpenAI first if available
        if OPENAI_AVAILABLE and openai_client:
            try:
                response = self._analyze_with_openai(query, conversation_history)
                if response:
                    return self._convert_types(response)
            except Exception as e:
                print(f"OpenAI error: {e}, falling back to rule-based")
        
        # Fallback to rule-based NLP
        intent = self._classify_intent(query_lower)
        entities = self._extract_entities(query_lower)
        response = self._generate_response(intent, entities, query_lower)
        
        return self._convert_types(response)
    
    def _analyze_with_openai(self, query, conversation_history):
        """Use OpenAI to understand query and generate SQL-like filters"""
        
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
        
        # Build conversation context
        context_messages = []
        if conversation_history:
            for msg in conversation_history[-3:]:  # Last 3 messages for context
                role = "user" if msg.get('type') == 'user' else "assistant"
                context_messages.append({
                    "role": role,
                    "content": msg.get('content', '')[:200]  # Limit length
                })
        
        # Enhanced system prompt
        system_prompt = f"""You are an expert AI data analyst specializing in UPI (Unified Payments Interface) transaction analysis for InsightX.

BUSINESS CONTEXT:
- UPI is India's real-time digital payment system
- Transactions occur 24/7 across multiple merchant categories
- Key business metrics: transaction success rate, fraud detection, peak usage times, category trends
- Important segments: device type (Android/iOS/Web), network quality (5G/4G/WiFi), geographic location

{schema_info}

YOUR TASK:
1. Understand the user's business question (consider Indian business context)
2. Identify the analysis type needed
3. Extract relevant filters and segments
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
- top: Find top performers (categories, states, etc.)
- general: Overview when intent is unclear

RESPONSE FORMAT (JSON only):
{{
    "intent": "average|count|total|comparison|peak_time|fraud|failure_rate|distribution|top|general",
    "entities": {{
        "category": "Food|Entertainment|Grocery|Fuel|Shopping|Utilities|Transport|Healthcare|Other",
        "device": "Android|iOS|Web",
        "network": "5G|4G|3G|WiFi",
        "state": "state name",
        "status": "SUCCESS|FAILURE"
    }},
    "confidence": 0.95
}}

IMPORTANT:
- Only include entities explicitly mentioned in the query
- Use exact values from AVAILABLE VALUES above
- Return valid JSON only (no extra text)
- If unsure, use intent: "general"
"""

        try:
            # Call OpenAI API with optimized settings
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Cost-effective choice
                messages=[
                    {"role": "system", "content": system_prompt},
                    *context_messages,  # Include conversation history
                    {"role": "user", "content": query}
                ],
                temperature=0.2,  # Low temp for consistent, focused responses
                max_tokens=400,   # Reduced from 500 for cost optimization
                response_format={"type": "json_object"}  # Force JSON output
            )
            
            ai_response = response.choices[0].message.content
            
            # Log token usage for monitoring
            usage = response.usage
            print(f"GPT tokens: {usage.prompt_tokens} prompt + {usage.completion_tokens} completion = {usage.total_tokens} total")
            
            try:
                # Parse JSON response
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    parsed = json.loads(ai_response[json_start:json_end])
                    
                    intent = parsed.get('intent', 'general')
                    entities = parsed.get('entities', {})
                    confidence = parsed.get('confidence', 0.8)
                    
                    # Log for debugging
                    print(f"GPT Analysis - Intent: {intent}, Entities: {entities}, Confidence: {confidence}")
                    
                    # Generate response using analytics engine
                    return self._generate_response(intent, entities, query.lower())
                else:
                    print("GPT returned invalid JSON format")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                return None
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
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
                return self._analyze_top(filtered_df)
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
    
    def _analyze_top(self, df):
        """Analyze top performers"""
        top = df.groupby('merchant_category').agg({
            'transaction id': 'count',
            'amount (INR)': 'sum'
        }).reset_index().sort_values('amount (INR)', ascending=False).head(10)
        top.columns = ['category', 'transactions', 'total_amount']
        
        answer = f"🏆 **Top Categories**\n\n"
        for i, row in top.iterrows():
            answer += f"{i+1}. {row['category']}: ₹{row['total_amount']:,.0f}\n"
        
        return {
            'answer': answer,
            'data': {'top': top.to_dict('records')},
            'visualization': {
                'type': 'bar',
                'data': top.to_dict('records'),
                'xKey': 'category',
                'yKey': 'total_amount',
                'title': 'Top Categories by Revenue'
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

