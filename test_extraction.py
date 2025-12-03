#!/usr/bin/env python3
"""Test Gemini extraction with actual prompt"""
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

google_key = os.getenv('GOOGLE_API_KEY')

# Load and escape prompt
prompt_path = Path('prompts/extraction_prompt.txt')
prompt_text = prompt_path.read_text(encoding='utf-8')

placeholder = "__DOCUMENT_TEXT_PLACEHOLDER__"
prompt_text = prompt_text.replace("{document_text}", placeholder)
prompt_text = prompt_text.replace("{", "{{").replace("}", "}}")
prompt_text = prompt_text.replace(placeholder, "{document_text}")

# Create template
template = PromptTemplate(
    template=prompt_text,
    input_variables=["document_text"]
)

# Test with simple document
test_doc = """
John Doe
Born: January 1, 1990
Software Engineer
Skills: Python, JavaScript, React
"""

formatted_prompt = template.format(document_text=test_doc)
print(f"Prompt length: {len(formatted_prompt)} chars")
print(f"First 300 chars:\n{formatted_prompt[:300]}")
print("\n---\n")

# Test with Gemini
try:
    model = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        google_api_key=google_key,
        temperature=0.1,
        max_output_tokens=4096
    )
    print('✓ Model initialized')
    
    response = model.invoke(formatted_prompt)
    print(f'✓ Response type: {type(response).__name__}')
    print(f'✓ Content length: {len(response.content)}')
    print(f'✓ Content:\n{response.content[:1000]}')
    
except Exception as e:
    import traceback
    print(f'✗ Error: {type(e).__name__}: {str(e)}')
    traceback.print_exc()
