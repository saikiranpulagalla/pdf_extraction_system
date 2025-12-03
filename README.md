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
│   ├── main.py                    # Streamlit UI
│   └── pipeline/
│       ├── pdf_loader.py          # PDF text extraction
│       ├── extractor.py           # LangChain LLM pipeline
│       ├── schema.py              # Pydantic validation
│       ├── model_selector.py      # OpenAI/Gemini fallback
│       └── excel_writer.py        # JSON to Excel converter
├── prompts/
│   └── extraction_prompt.txt      # LLM extraction instructions
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
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
streamlit run app/main.py
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

LangChain orchestrates the extraction:
- Sends text to OpenAI GPT-4o (primary)
- Falls back to Google Gemini on failure
- Uses carefully designed extraction prompt
- Retries up to 3 times on errors

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

**Error: "Failed to parse JSON"**
- Solution: LLM output may be malformed - system will retry automatically

**Error: "PDF appears to be empty or contains only images"**
- Solution: PDF must have extractable text (not scanned images)

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

MIT License - Feel free to use in your projects!

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