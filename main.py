
import os
import time
import config
from drive_service import DriveService
from text_extractor import TextExtractor
from ai_classifier import AIClassifier
from folder_manager import FolderManager

def main():
    print("Starting AI-Powered Google Drive Organizer...")
    
    if config.USE_GEMINI:
        print("[SYSTEM] LLM Provider: Gemini (Cloud) with Fallback to Ollama")
    else:
        print(f"[SYSTEM] LLM Provider: Ollama ({config.MODEL_NAME} - Local)")
    
    # 1. Initialize Services
    try:
        drive_service = DriveService()
        if not drive_service.service:
            print("Failed to initialize Google Drive Service. Exiting.")
            return
    except Exception as e:
        print(f"Error initializing Drive Service: {e}")
        return

    classifier = AIClassifier()
    folder_manager = FolderManager(drive_service)
    extractor = TextExtractor()

    # 2. Fetch Files
    print("Fetching files from Google Drive Root...")
    files = drive_service.list_files()
    print(f"Found {len(files)} files.")

    for file in files:
        file_id = file['id']
        file_name = file['name']
        mime_type = file['mimeType']
        
        # Skip folders
        if mime_type == 'application/vnd.google-apps.folder':
            print(f"  [Skipping] Folder: {file_name}")
            continue
            
        print(f"\nProcessing: {file_name} ({mime_type})")
        time.sleep(4) # Rate limit handling for Free Tier (15 RPM)

        # 3. Extract Text
        content_text = ""
        if mime_type == 'application/pdf':
            print("  Downloading and extracting PDF text...")
            file_content = drive_service.download_file(file_id)
            if file_content:
                content_text = extractor.extract_from_pdf(file_content)
        
        elif mime_type == 'application/vnd.google-apps.document':
            print("  Exporting Google Doc content...")
            file_content = drive_service.export_file(file_id, 'text/plain')
            if file_content:
                 content_text = extractor.extract_from_bytes(file_content)
        
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
             print("  Exporting Google Sheet content...")
             # CSV export for sheets could be better, or just rely on name if content fails
             file_content = drive_service.export_file(file_id, 'text/csv')
             if file_content:
                 content_text = extractor.extract_from_bytes(file_content)
        
        else:
            print("  Skipping content extraction (unsupported type), using filename only.")
            content_text = ""

        # 4. Classify
        print(f"  Classifying...")
        category, confidence, method = classifier.classify_file(file_name, content_text)
        print(f"  Result: {category} (Confidence: {confidence}%) [Method: {method}]")

        # 5. Determine Action
        target_category = category
        if confidence < config.CONFIDENCE_THRESHOLD:
            print(f"  Low confidence (<{config.CONFIDENCE_THRESHOLD}). Flagging for review.")
            target_category = config.FALLBACK_CATEGORY

        # 6. Move File
        target_folder_id = folder_manager.get_target_folder_id(target_category)
        if target_folder_id:
            msg = "Moved" if not config.DRY_RUN else "Would move"
            success = drive_service.move_file(file_id, target_folder_id)
            if success:
                print(f"  [SUCCESS] {msg} to '{target_category}'")
            else:
                print(f"  [FAIL] Failed to move file.")
        else:
            print(f"  [FAIL] Could not get target folder ID.")

    print("\nOrganization Complete.")

if __name__ == "__main__":
    main()
