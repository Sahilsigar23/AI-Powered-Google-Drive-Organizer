
import google.generativeai as genai
import config
import os

def list_models():
    if not config.GEMINI_API_KEY:
        print("GEMINI_API_KEY not found.")
        return

    genai.configure(api_key=config.GEMINI_API_KEY)
    
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
