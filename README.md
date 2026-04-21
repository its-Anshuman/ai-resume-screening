# AI Resume Screening & Referral System

An automated resume screening and evaluation system that uses AI to analyze and score candidate resumes against job descriptions.

## Features

- 📋 Fetch candidates from Google Sheets
- 📥 Download resumes from Google Drive links
- 🤖 AI-powered resume evaluation using Groq/OpenAI
- 📊 Similarity scoring based on job description
- 💾 Export results to CSV
- 🎯 Categorize candidates (Shortlist/Maybe/Reject)
- 🎨 Interactive Streamlit web interface

## Prerequisites

- Python 3.8+
- Google Cloud credentials (for Sheets & Drive API)
- API keys for: Groq, OpenAI, Hugging Face

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai_resume_screening.git
cd ai_resume_screening
```

### 2. Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=sk_your_actual_key
   HF_TOKEN=hf_your_actual_token
   GROQ_API_KEY=gsk_your_actual_key
   GOOGLE_SHEET_NAME=Your Sheet Name
   ```

### 5. Configure Google Credentials

1. Create a [Google Cloud Project](https://console.cloud.google.com/)
2. Enable APIs: Google Sheets API & Google Drive API
3. Create a Service Account and download JSON key
4. Save as `service_account.json` in project root
5. **Important**: `.env` and `service_account.json` are in `.gitignore` - never commit them!

### 6. Run the Application

**Streamlit UI:**
```bash
streamlit run app.py
```

**Command Line:**
```bash
python main.py
```

## Project Structure

```
ai_resume_screening/
├── app.py                    # Streamlit web UI
├── main.py                   # Main pipeline
├── config.py                 # Configuration (reads from .env)
├── download_resume.py        # Google Drive downloader
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions
├── src/
│   ├── ingestion.py          # Google Sheets fetcher
│   ├── parser.py             # PDF text extraction
│   ├── llm_evaluator.py      # AI resume evaluation
│   ├── scoring.py            # Similarity & scoring
│   └── utils.py              # Helper functions
├── data/                     # Input data
├── resumes/                  # Downloaded resumes (not in git)
└── outputs/                  # Results CSV (not in git)
```

## Configuration

All settings are in `.env`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk_...` |
| `HF_TOKEN` | Hugging Face token | `hf_...` |
| `GROQ_API_KEY` | Groq API key | `gsk_...` |
| `GOOGLE_SHEET_NAME` | Google Sheet name | `Candidate Input (Responses)` |
| `RESUME_FOLDER` | Resume storage directory | `resumes/` |
| `OUTPUT_FILE` | Results CSV path | `outputs/results.csv` |

## Security Notes

⚠️ **Never commit these files:**
- `.env` - Contains API keys
- `service_account.json` - Google credentials
- `resumes/` - Downloaded resumes

These are in `.gitignore` for your safety.

## API Keys

Get free API keys from:

- **Groq**: https://console.groq.com
- **OpenAI**: https://platform.openai.com/api-keys
- **Hugging Face**: https://huggingface.co/settings/tokens

## How It Works

1. **Ingestion**: Fetches candidate list from Google Sheets
2. **Download**: Downloads resumes from Google Drive links
3. **Parsing**: Extracts text from PDF resumes
4. **Evaluation**: Uses LLM (Groq/OpenAI) to evaluate fit
5. **Scoring**: Combines LLM score with semantic similarity
6. **Output**: Exports ranked candidates to CSV

## Troubleshooting

### Missing API Key Error
- Ensure `.env` file exists in project root
- Check all required keys are set in `.env`
- Verify keys are valid and active

### Google Credentials Error
- Verify `service_account.json` exists
- Ensure Google Sheets & Drive APIs are enabled
- Check service account has access to your sheet

### Model Download Issues
- First run downloads ML models automatically
- Ensure internet connection is stable
- Hugging Face token helps with faster downloads

## License

[Add your license]

## Author

[Your Name/Organization]

## Contributing

Feel free to submit issues and enhancement requests!
