#!/usr/bin/env python3
"""Debug Gemini empty response issue"""
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

# Test with different model configurations
configs = [
    {"max_output_tokens": 4096, "temperature": 0.1, "timeout": 60},
    {"max_output_tokens": 2048, "temperature": 0.7, "timeout": 120},
    {"temperature": 0.1, "timeout": 60},  # Without max_output_tokens
]

for i, config in enumerate(configs):
    print(f"\n--- Test {i+1}: {config} ---")
    try:
        model = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash',
            google_api_key=google_key,
            **config
        )
        
        response = model.invoke(formatted_prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        print(f"✓ Content length: {len(content)}")
        if content:
            print(f"✓ First 300 chars:\n{content[:300]}")
        else:
            print("✗ EMPTY RESPONSE")
            print(f"Response object: {response}")
            print(f"Response attrs: {dir(response)}")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
