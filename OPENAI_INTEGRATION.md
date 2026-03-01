# OpenAI GPT Integration Guide for InsightX

## Step 1: Get Your OpenAI API Key

1. **Create an OpenAI Account:**
   - Go to https://platform.openai.com/signup
   - Sign up with your email or Google/Microsoft account

2. **Generate API Key:**
   - Navigate to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Give it a name (e.g., "InsightX Project")
   - Copy the key immediately (you won't see it again!)

3. **Add Billing:**
   - Go to https://platform.openai.com/account/billing
   - Add a payment method
   - GPT-3.5-turbo costs ~$0.002 per 1K tokens (very affordable!)
   - Set spending limits to control costs

## Step 2: Configure Your Project

1. **Edit the .env file:**
   ```bash
   nano .env
   ```

2. **Replace the placeholder with your actual API key:**
   ```env
   # OpenAI API Key for GPT-4 (optional - falls back to rule-based NLP)
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

3. **Save and restart the backend:**
   ```bash
   # Kill existing backend
   pkill -f "python3 app.py"
   
   # Start fresh
   python3 app.py
   ```

## Step 3: How GPT Integration Works

### Current Architecture:
```
User Query → OpenAI GPT → Intent & Entities → Rule-based Analytics → Response
              (Smart)                            (Accurate)
```

### What GPT Does:
1. **Understands natural language** - handles variations, typos, context
2. **Extracts intent** - determines what type of analysis (average, count, etc.)
3. **Identifies entities** - finds categories, devices, states, etc.
4. **Returns structured JSON** - passes to your analytics engine

### What Your Code Does:
1. **Data filtering** - applies extracted filters to dataset
2. **Statistical analysis** - calculates averages, counts, trends
3. **Visualization** - generates charts
4. **Response formatting** - creates beautiful markdown responses

## Step 4: Customization for UPI Transactions

The current GPT prompt is already optimized for your project! Here's what makes it special:

### Dynamic Schema Injection:
```python
schema_info = f"""
Dataset Schema:
- Total records: {len(self.df)}
- Columns: {', '.join(self.df.columns)}
- Categories: {', '.join(self.df['merchant_category'].unique())}
- States: {', '.join(self.df['sender_state'].unique())}
- Device types: {', '.join(self.df['device_type'].unique())}
- Network types: {', '.join(self.df['network_type'].unique())}
"""
```
This tells GPT exactly what data you have!

### Structured Output:
GPT returns JSON with intent and entities, not free-form text:
```json
{
    "intent": "average",
    "entities": {
        "category": "Food",
        "device": "Android"
    }
}
```

## Step 5: Advanced Customizations

### A. Use GPT-4 for Better Understanding
```python
model="gpt-4o-mini"  # Smarter, slightly more expensive
```

### B. Add Conversation History
The system already supports this! It passes the last 5 messages:
```python
response = analyzer.analyze_query(query, history=messages.slice(-5))
```

### C. Temperature Control
- Current: `temperature=0.3` (consistent, focused)
- For creative insights: `temperature=0.7`
- For deterministic: `temperature=0.0`

### D. Add Business Context
Enhance the system prompt with domain knowledge:
```python
system_prompt = f"""You are an AI data analyst for UPI transaction data in India.

BUSINESS CONTEXT:
- UPI (Unified Payments Interface) is India's instant payment system
- Transactions occur 24/7 across multiple categories
- Key metrics: success rate, fraud detection, peak times
- Important segments: device type (Android/iOS), network (5G/4G/WiFi)

{schema_info}

Your job is to:
1. Understand the user's business question
2. Consider Indian business hours (9 AM - 9 PM peak)
3. Account for festival seasons and weekends
4. Determine what analysis to perform
5. Extract relevant filters

Response format: [same as before]
"""
```

## Step 6: Cost Optimization

### Current Usage:
- Each query: ~500-1000 tokens
- Cost: ~$0.001 - $0.002 per query
- 1000 queries ≈ $1.50

### Optimization Tips:
1. **Use GPT-3.5-turbo** (current) - 10x cheaper than GPT-4
2. **Reduce max_tokens** from 500 to 300
3. **Cache common queries** (already handled by rule-based fallback)
4. **Set token limits** in OpenAI dashboard

## Step 7: Testing GPT Integration

### Test Commands:
```bash
# 1. Check if GPT is enabled
curl -s http://localhost:5000/api/health

# 2. Test complex query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the top performing categories on weekends for iOS users?"}' \
  | python3 -m json.tool

# 3. Test natural variations
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "how much do people spend on food using android phones?"}' \
  | python3 -m json.tool
```

### Expected Output:
```
✓ OpenAI API enabled  <-- You should see this instead of "rule-based NLP"
```

## Step 8: Monitoring & Debugging

### Check OpenAI Usage:
1. Dashboard: https://platform.openai.com/usage
2. See token consumption
3. Monitor costs in real-time

### Debug Mode:
The app already prints errors:
```python
print(f"OpenAI error: {e}, falling back to rule-based")
```

### Fallback System:
If GPT fails, the app automatically uses rule-based NLP - your users never see errors!

## Step 9: Advanced Features

### A. Multi-turn Conversations
GPT can remember context from previous messages:
```python
# Already supported via conversation_history parameter
# Frontend sends last 5 messages for context
```

### B. Sentiment Analysis
Add to system prompt:
```python
"Also detect user sentiment (frustrated/curious/urgent) and adjust response tone."
```

### C. Query Suggestions
Use GPT to generate follow-up questions:
```python
"After answering, suggest 2-3 relevant follow-up questions the user might ask."
```

### D. Insight Generation
Have GPT generate business insights:
```python
"After analysis, provide one actionable business insight based on the data."
```

## Troubleshooting

### Issue: "OpenAI initialization failed"
**Solution:** Check your API key format (should start with `sk-proj-` or `sk-`)

### Issue: "Rate limit exceeded"
**Solution:** Add rate limiting or upgrade your OpenAI tier

### Issue: "Invalid JSON response"
**Solution:** GPT sometimes adds markdown. The code already handles this with:
```python
json_start = ai_response.find('{')
json_end = ai_response.rfind('}') + 1
```

### Issue: High costs
**Solution:** 
- Use GPT-3.5-turbo (current)
- Set max_tokens lower
- Implement query caching
- Add user rate limits

## Best Practices

1. ✅ **Keep your API key secret** - never commit to GitHub
2. ✅ **Set spending limits** - protect against unexpected costs
3. ✅ **Monitor usage** - check dashboard regularly
4. ✅ **Use fallback** - always have rule-based backup (already implemented)
5. ✅ **Validate outputs** - ensure GPT returns proper JSON
6. ✅ **Log errors** - track when GPT fails
7. ✅ **Version control prompts** - treat prompts like code

## Next Steps

1. Get your OpenAI API key
2. Add it to `.env` file
3. Restart backend
4. Test with complex queries
5. Monitor usage and costs
6. Customize system prompt for your use case
7. Add advanced features as needed

## Resources

- OpenAI API Docs: https://platform.openai.com/docs
- Pricing: https://openai.com/pricing
- Best Practices: https://platform.openai.com/docs/guides/prompt-engineering
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits
