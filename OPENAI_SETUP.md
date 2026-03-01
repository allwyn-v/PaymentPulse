# OpenAI Integration Setup

## Why Add OpenAI?

The chatbot now supports **two modes**:

### 1. Rule-Based NLP (Default - No API Key Required)
- Works offline
- Handles predefined patterns
- Fast and free
- Good for common queries

### 2. OpenAI GPT (Optional - Requires API Key)
- Understands any natural language query
- More flexible and intelligent
- Handles complex, ambiguous questions
- Learns from context

## How to Enable OpenAI

### Step 1: Get API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-...`)

### Step 2: Add to Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Restart Backend

```bash
# Kill existing backend
pkill -f "python3 app.py"

# Start again
python3 app.py
```

You should see: `✓ OpenAI API enabled`

## Example Queries That Work Better with OpenAI

### Complex Natural Language
- "Can you tell me which payment method people prefer on weekends in Mumbai?"
- "I want to understand the transaction behavior of millennials"
- "Are there any suspicious patterns in high-value transactions?"

### Ambiguous Queries
- "What's happening with transactions lately?"
- "Show me something interesting about the data"
- "Any anomalies I should know about?"

### Multi-dimensional Analysis
- "Compare iOS users in Delhi with Android users in Mumbai"
- "What's different about weekend shopping vs weekday grocery?"

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.001 per query (very cheap)
- **GPT-4**: ~$0.03 per query (more expensive)
- Rule-based mode: **FREE**

Current implementation uses GPT-3.5-turbo (most cost-effective).

## Fallback System

The system automatically:
1. Tries OpenAI first (if configured)
2. Falls back to rule-based NLP if:
   - No API key provided
   - API call fails
   - Rate limit exceeded
   - Invalid response

This ensures **the chatbot always works**, even without OpenAI!

## Testing

```bash
# Without OpenAI (rule-based)
# Just don't set OPENAI_API_KEY

# With OpenAI
# Set OPENAI_API_KEY in .env and restart

# Test both modes with the same query to compare
```

## Security Note

**Never commit your .env file with API keys!**
The `.gitignore` already excludes it, but always verify.

---

**You can use the chatbot without OpenAI - it works great with rule-based NLP too!**
