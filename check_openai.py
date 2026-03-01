#!/usr/bin/env python3
"""
Quick check to see if OpenAI is configured correctly
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("  OpenAI Configuration Check")
print("="*70 + "\n")

# Check API key
api_key = os.getenv('OPENAI_API_KEY', '')

if not api_key or api_key == 'your_openai_api_key_here':
    print("❌ OpenAI API Key: NOT CONFIGURED")
    print("\nTo fix:")
    print("1. Get your API key from: https://platform.openai.com/api-keys")
    print("2. Edit .env file: nano .env")
    print("3. Set: OPENAI_API_KEY=sk-proj-xxxxx...")
    print("4. Restart backend: python3 app.py\n")
else:
    # Mask the key for security
    masked = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else api_key[:10] + "..."
    print(f"✓ OpenAI API Key: FOUND ({masked})")
    
    # Try to import and test
    try:
        from openai import OpenAI
        print("✓ OpenAI library: INSTALLED")
        
        try:
            client = OpenAI(api_key=api_key)
            print("✓ OpenAI client: INITIALIZED")
            
            # Quick test (this costs ~$0.0001)
            print("\nTesting connection...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'test'"}],
                max_tokens=5
            )
            print("✓ OpenAI API: WORKING")
            print(f"  Response: {response.choices[0].message.content}")
            
            print("\n" + "="*70)
            print("  🎉 SUCCESS! OpenAI is configured correctly!")
            print("="*70)
            print("\nYou can now:")
            print("• Start backend: python3 app.py")
            print("• Run tests: python3 test_openai.py")
            print("• Use the chatbot at: http://localhost:3000\n")
            
        except Exception as e:
            print(f"❌ OpenAI connection failed: {str(e)}")
            print("\nPossible issues:")
            print("• Invalid API key")
            print("• No billing configured")
            print("• Network connectivity issue")
            print(f"\nCheck: https://platform.openai.com/account/api-keys\n")
            
    except ImportError:
        print("❌ OpenAI library: NOT INSTALLED")
        print("\nTo fix:")
        print("  pip install openai\n")

print()
