"""
InsightX Demo Script
Run this to see example queries and responses
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def print_query(query):
    print(f"🙋 USER: {query}")
    print("-" * 80)

def print_response(response):
    if response.get('success'):
        answer = response['response']['answer']
        print(f"🤖 AI:\n{answer}\n")
        
        if response['response'].get('visualization'):
            viz = response['response']['visualization']
            print(f"📊 Visualization: {viz['type'].upper()} chart - {viz['title']}")
    else:
        print(f"❌ Error: {response.get('error', 'Unknown error')}")
    print("-" * 80)

def test_api(query):
    """Send query to API and print response"""
    print_query(query)
    
    try:
        response = requests.post(
            f"{API_BASE}/query",
            json={"query": query, "history": []},
            timeout=30
        )
        
        if response.status_code == 200:
            print_response(response.json())
        else:
            print(f"❌ API Error: Status {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend is running (python app.py)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)  # Pause between queries

def main():
    print_header("InsightX Demo - Conversational AI for Transaction Analytics")
    
    # Check API health
    print("Checking API health...")
    try:
        health = requests.get(f"{API_BASE}/health", timeout=5)
        if health.status_code == 200:
            data = health.json()
            print(f"✅ API is healthy!")
            print(f"   - Total transactions: {data['total_transactions']:,}")
            print(f"   - Data loaded: {data['data_loaded']}")
        else:
            print("❌ API is not responding correctly")
            return
    except:
        print("❌ Cannot connect to API. Please run: python app.py")
        return
    
    # Demo queries
    queries = [
        # Basic analytics
        "What is the average transaction amount for Food category?",
        
        # Peak time analysis
        "Show me peak hours for Entertainment transactions",
        
        # Comparison
        "Compare iOS vs Android transaction performance",
        
        # Network analysis
        "Compare 5G vs WiFi performance",
        
        # Failure analysis
        "What is the failure rate across different categories?",
        
        # Fraud analysis
        "Show me transactions flagged for fraud",
        
        # Top performers
        "What are the top 5 states by transaction volume?",
        
        # Age group analysis
        "Show the distribution of transactions by age group",
        
        # Count query
        "How many transactions are in the Grocery category?",
        
        # Percentage query
        "What percentage of transactions are successful?",
    ]
    
    print_header("Running Demo Queries")
    print("This will demonstrate various types of questions you can ask...\n")
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}/{len(queries)}]")
        test_api(query)
        
        if i < len(queries):
            print("\nNext query in 2 seconds...")
            time.sleep(2)
    
    print_header("Demo Complete!")
    print("You can now open http://localhost:3000 to try your own queries!")
    print("\nSome ideas to try:")
    print("  • Compare weekend vs weekday patterns")
    print("  • Analyze specific states or age groups")
    print("  • Find trends over different time periods")
    print("  • Investigate failure patterns")
    print("  • Explore fraud indicators")

if __name__ == "__main__":
    main()
