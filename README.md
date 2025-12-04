# AI-Powered PDF Extraction System

A production-ready application that extracts structured data from 1-2 page PDFs using LangChain, OpenAI GPT-4o (primary), and Google Gemini (fallback).

## 🎯 Features

- **Zero Hardcoded Keys**: LLM auto-detects all fields and relationships
- **100% Content Extraction**: No data loss - captures everything in the PDF
- **Automatic Fallback**: OpenAI → Google Gemini on failure
- **Flexible JSON Structure**: Auto-groups related information logically
- **Production-Ready**: Retry logic, error handling, and validation
- **Excel Export**: Clean, formatted Excel with comments column
- **Streamlit UI**: Easy upload and download interface

## 🏗️ Architecture

```
User Upload PDF → Streamlit UI → PDF Text Extraction → LangChain Pipeline
→ OpenAI GPT-4o (Primary) / Gemini (Fallback) → Structured JSON
→ Validation & Cleaning → Excel Export → Download
```

## 📁 Project Structure

```
pdf-extraction-system/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Main entry point
│   ├── streamlit_app.py           # Streamlit UI for PDF extraction
│   └── pipeline/
│       ├── __init__.py
│       ├── pdf_loader.py          # PDF text extraction using pdfplumber
│       ├── extractor.py           # LangChain LLM pipeline with retry logic
│       ├── schema.py              # Pydantic validation schemas
│       ├── model_selector.py      # OpenAI/Gemini model fallback logic
│       ├── excel_writer.py        # JSON to Excel converter
│       └── __pycache__/
├── prompts/
│   └── extraction_prompt.txt      # LLM extraction instructions & format
├── tests/
│   ├── __init__.py
│   ├── test_extractor.py          # Tests for LLM extraction pipeline
│   ├── test_pdf_loader.py         # Tests for PDF text extraction
│   ├── test_schema.py             # Tests for validation schemas
│   ├── test_model_selector.py     # Tests for model selection logic
│   └── test_excel_writer.py       # Tests for Excel generation
├── .env.example                   # Example environment file
├── .gitignore                     # Git ignore rules
├── pyproject.toml                 # Project metadata and dependencies
├── requirements.txt               # Python package dependencies
├── main.py                        # Legacy entry point (use app/main.py)
├── test_extraction.py             # Manual extraction tests
├── test_gemini.py                 # Gemini model tests
├── test_gemini_configs.py         # Gemini configuration tests
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/saikiranpulagalla/pdf_extraction_system.git
cd pdf-extraction-system
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-gemini-key-here
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://ai.google.dev/

### 5. Run Application

```bash
streamlit run app/streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Upload PDF**: Click "Choose a PDF file" and select your 1-2 page PDF
2. **Configure**: Optionally adjust model settings in the sidebar
3. **Extract**: Click "🚀 Extract Data" button
4. **Review**: View the extracted JSON data
5. **Download**: Click "📥 Download Excel File" to get the formatted Excel

## 🔧 Configuration

### Model Settings

You can customize the models in the sidebar:

- **Primary Model**: `gpt-4o` (recommended), `gpt-4o-mini`, `gpt-4-turbo`
- **Fallback Model**: `gemini-2.5-flash` (recommended), `gemini-1.5-pro`
- **Temperature**: 0.0 (focused) to 1.0 (creative)

### Environment Variables

Available in `.env`:

```env
OPENAI_API_KEY=          # Required for OpenAI
GOOGLE_API_KEY=          # Required for Gemini
PRIMARY_MODEL=gpt-4o     # Default OpenAI model
FALLBACK_MODEL=gemini-2.5-flash  # Default Gemini model
TEMPERATURE=0.1          # Default temperature
MAX_PDF_PAGES=2          # Maximum PDF pages
MAX_RETRIES=3            # Maximum retry attempts
```

## 🧪 Testing

Run tests:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app

# Run specific test
pytest tests/test_extractor.py -v
```

## 📊 Output Format

### JSON Structure

The extracted data follows this flexible structure:

```json
{
  "Basic Details": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "Education Details": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "MIT",
      "year": "2020",
      "comments": "Graduated with honors"
    }
  ],
  "Career Details": [
    {
      "position": "Senior Software Engineer",
      "company": "Tech Corp",
      "duration": "2020 - Present",
      "responsibilities": "Led team of 5 engineers...",
      "comments": "Promoted twice"
    }
  ],
  "Skills": [
    {
      "skill_category": "Programming Languages",
      "skills_list": ["Python", "JavaScript", "Java"]
    }
  ]
}
```

### Excel Format

The Excel file contains 4 columns:

| Section | Key | Value | Comments |
|---------|-----|-------|----------|
| Basic Details | name | John Doe | |
| Education Details #1 | degree | Bachelor of Science... | Graduated with honors |

## 🔍 How It Works

### 1. PDF Text Extraction

Uses `pdfplumber` to extract text with formatting preservation:
- Handles 1-2 page PDFs
- Cleans excessive whitespace
- Preserves line breaks and structure

### 2. LLM Processing

LangChain orchestrates the extraction with robust error handling:
- Sends text to OpenAI GPT-4o (primary)
- Logs response preview (first 1000 chars) for debugging
- Validates response is not empty before parsing
- Falls back to Google Gemini on any failure
- Retries up to 3 times with exponential backoff (2-10 seconds)
- Includes response snippet in error messages for troubleshooting

### 3. Structured Output

LLM returns JSON with:
- Auto-detected keys (no hardcoding)
- Logical grouping (Basic, Education, Career, etc.)
- Flexible order
- Comments for context

### 4. Validation & Cleaning

Pydantic schemas validate:
- JSON structure integrity
- Data completeness
- Type correctness
- Required fields

### 5. Excel Export

Converts JSON to formatted Excel:
- Hierarchical structure
- Color-coded sections
- Auto-sized columns
- Comments column

## 🛠️ Development

### Project Dependencies

- **LangChain**: LLM orchestration and chains
- **OpenAI**: Primary extraction model
- **Google Gemini**: Fallback extraction model
- **pdfplumber**: PDF text extraction
- **Pydantic**: Schema validation
- **pandas/openpyxl**: Excel generation
- **Streamlit**: Web UI
- **tenacity**: Retry logic

### Adding New Features

1. **Custom Prompt**: Edit `prompts/extraction_prompt.txt`
2. **New Extractors**: Add to `app/pipeline/`
3. **Additional Models**: Update `model_selector.py`
4. **UI Changes**: Modify `app/main.py`

## 🐛 Troubleshooting

### Common Issues

**Error: "No API keys available"**
- Solution: Set `OPENAI_API_KEY` or `GOOGLE_API_KEY` in `.env`

**Error: "PDF has no pages"**
- Solution: Ensure PDF is not corrupted and has content

**Error: "Failed to parse JSON from LLM response"**
- Solution: System automatically logs response preview for debugging. Check that:
  - API keys are valid and have sufficient quota
  - Internet connection is stable
  - Model endpoints are accessible
  - LLM will retry up to 3 times automatically, then fallback to alternate model

**Error: "Empty LLM response"**
- Solution: Model returned no content. This often indicates:
  - Rate limiting or temporary API issues
  - Invalid API key or insufficient quota
  - Network connectivity problem
  - System automatically retries with fallback model

**Error: "PDF appears to be empty or contains only images"**
- Solution: PDF must have extractable text (not scanned images)

### Debug Mode

The system logs LLM response previews to help troubleshoot extraction failures:

- **Response Preview**: First 1000 characters of LLM response printed before parsing
- **Error Details**: Failed responses include a snippet of the actual content
- **Retry Information**: Console shows which model is being used and retry attempts

Example console output:
```
LLM response preview (len=2048): '{"Basic Details": {...}}'
Extraction attempt failed with openai: Failed to parse JSON from LLM response: Expecting value...
Attempting fallback to Gemini...
```

For full debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing issues for solutions
- Review troubleshooting section

## 🎓 Credits

Built with:
- [LangChain](https://langchain.com/)
- [OpenAI](https://openai.com/)
- [Google Gemini](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)

---

**Made with ❤️ for intelligent document processing**
