
import fitz  # PyMuPDF
import io

class TextExtractor:
    @staticmethod
    def extract_from_pdf(file_content):
        """Extracts text from PDF bytes."""
        try:
            text = ""
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""

    @staticmethod
    def extract_from_bytes(file_content):
        """Simple text extraction from bytes (for txt files)."""
        try:
            return file_content.decode('utf-8')
        except:
            return ""
