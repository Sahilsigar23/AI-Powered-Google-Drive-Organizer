
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Drive Config
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# AI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AI_PROVIDER = "ollama" # Default, overridden by USE_GEMINI check in code or config
USE_GEMINI = bool(GEMINI_API_KEY)
MODEL_NAME = "tinyllama"
MAX_TEXT_LENGTH = 800
CONFIDENCE_THRESHOLD = 70

# Categories
CATEGORIES = [
    "HR",
    "Finance",
    "Academics",
    "Projects",
    "Marketing",
    "Personal"
]

FALLBACK_CATEGORY = "Review_Required"
CONFIDENCE_THRESHOLD = 70

# Dry Run
DRY_RUN = os.getenv("DRY_RUN", "False").lower() == "true"
