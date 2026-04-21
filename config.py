import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (read from environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Google Sheets Configuration
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Candidate Input (Responses)")

# File Paths
RESUME_FOLDER = os.getenv("RESUME_FOLDER", "resumes/")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "outputs/results.csv")