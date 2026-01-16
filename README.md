
# AI-Powered Google Drive Organizer

An intelligent Python script that organizes your Google Drive files into categories (HR, Finance, Academics, Projects, Marketing, Personal) using AI.

## Features
- **Auto-Organization**: Scans and moves files into categorized folders.
- **AI Classification**: Uses local LLM (TinyLlama via Ollama) to understand file context.
  - **TinyLlama**: A lightweight (~600MB) model optimized for low-resource environments.
  - **Rule-Based Fallback**: Uses keyword matching for high speed and accuracy on common files.
- **Content Extraction**: Reads PDFs, Google Docs, and Sheets.
- **Safety First**: "Review_Required" folder for low-confidence (<70%) matches.
- **Dry Run Mode**: Preview changes without moving files.

## Setup

### 1. Prerequisites
- Python 3.8+
- Google Cloud Project with Drive API enabled.
- Gemini API Key.

### 2. Installation
1. Clone this repository (or copy files).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
1. **Google Credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Enable **Google Drive API**.
   - Create OAuth 2.0 Credentials (Desktop App).
   - Download `credentials.json` and place it in the project root.

2. **Environment Variables**:
   - Create a `.env` file in the root:
     ```ini
     GEMINI_API_KEY=your_gemini_key_here
     DRY_RUN=True
     ```

## Usage

### Dry Run (Recommended First)
Check what *would* happen without moving files:
```bash
python main.py
```
(Ensure `DRY_RUN=True` in `.env` or `config.py`)

### Live Run
To actually move files, set `DRY_RUN=False` in `.env` and run:
```bash
python main.py
```

### First Run Auth
On the first run, a browser window will open asking you to log in to your Google Account. Grant the permissions to allow the script to manage your Drive files.

## Project Structure
- `main.py`: Entry point. Orchestrates scanning and organizing.
- `drive_service.py`: Handles Google Drive API interactions.
- `ai_classifier.py`: Sends text to Gemini for classification.
- `text_extractor.py`: reads PDFs and Docs.
- `config.py`: Settings and constants.

## Limitations
- **Processing Time**: Large files or many files may take time due to API rate limits.
- **Image Scanning**: Currently OCR for images is not implemented (placeholder logic).
- **Google Sheets**: Extracts as CSV text, which might be messy for complex sheets.

## Future Improvements
- Add OCR for scanned documents/images.
- Implement a watchdog for real-time organization.
- Add a web UI for logs and manual reviews.
