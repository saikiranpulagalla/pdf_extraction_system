#!/usr/bin/env python3
"""Quick test of Gemini API"""
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import os

google_key = os.getenv('GOOGLE_API_KEY')
print(f'Google API Key present: {bool(google_key)}')
if google_key:
    print(f'Key (first 20 chars): {google_key[:20]}...')

try:
    model = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        google_api_key=google_key,
        temperature=0.1,
        max_output_tokens=4096
    )
    print('✓ Model initialized successfully')
    
    response = model.invoke('Say hello with one word only')
    print(f'✓ Response type: {type(response).__name__}')
    if hasattr(response, 'content'):
        print(f'✓ Content: "{response.content}"')
        print(f'✓ Content length: {len(response.content)}')
    else:
        print(f'✓ Response: {response}')
except Exception as e:
    import traceback
    print(f'✗ Error: {type(e).__name__}: {str(e)}')
    traceback.print_exc()
