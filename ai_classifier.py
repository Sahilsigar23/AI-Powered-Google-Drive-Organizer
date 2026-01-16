
import json
import config
import ollama
import google.generativeai as genai
import re
import time

def log_request(filename, prompt):
    with open("ollama_requests.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{time.ctime()}]\n")
        f.write(f"FILE: {filename}\n")
        f.write(f"PROMPT:\n{prompt}\n")
        f.write("-"*40 + "\n")

class AIClassifier:
    def __init__(self):
        # Rule-based keywords (Simple mapping)
        self.rules = {
            "Finance": ["invoice", "receipt", "salary", "tax", "statement", "budget", "expense"],
            "HR": ["resume", "offer letter", "contract", "agreement", "hiring", "onboarding"],
            "Academics": ["thesis", "homework", "assignment", "report", "study", "exam", "grade"],
            "Marketing": ["campaign", "social media", "ad", "flyer", "brochure", "promotion"],
            "Projects": ["project", "timeline", "plan", "roadmap"],
        }
        
        self.use_gemini = config.USE_GEMINI
        self.gemini_model = None
        
        if self.use_gemini:
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            except Exception as e:
                print(f"[System] Warning: Failed to initialize Gemini: {e}. Defaulting to Ollama.")
                self.use_gemini = False

    def classify_file(self, file_name, file_content_snippet):
        """
        Classifies using Rule-based logic first.
        Then tries Gemini (if configured).
        Falls back to Ollama (TinyLlama) on failure.
        """
        # 1. Truncate Content
        if len(file_content_snippet) > config.MAX_TEXT_LENGTH:
            file_content_snippet = file_content_snippet[:config.MAX_TEXT_LENGTH]
            
        full_text = (file_name + " " + file_content_snippet).lower()

        # 2. Rule-Based Classification
        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in full_text:
                    return category, 90, "Rule-Based"

        # 3. AI Classification (Hybrid)
        if self.use_gemini:
            print(f"  [LLM] Using Gemini for classification...")
            cat, conf, method = self._classify_with_gemini(file_name, file_content_snippet)
            if method != "Gemini (Failed)":
                return cat, conf, method
            
            print(f"  [LLM] Gemini failed or low confidence. Falling back to Ollama ({config.MODEL_NAME})...")
        
        # 4. Ollama Fallback
        print(f"  [LLM] Using Ollama ({config.MODEL_NAME}) for classification...")
        return self._classify_with_ollama(file_name, file_content_snippet)

    def _classify_with_gemini(self, file_name, content):
        prompt = f"""Task: Classify text into exactly one category: {', '.join(config.CATEGORIES)}.
Output Format: JSON with keys "category" and "confidence".
Constraint: No chat, no markdown.

Input Text:
{content}
"""
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            result = json.loads(response.text)
            cat = result.get('category', config.FALLBACK_CATEGORY)
            conf = result.get('confidence', 0)
            
            if cat not in config.CATEGORIES: cat = config.FALLBACK_CATEGORY
            if conf < config.CONFIDENCE_THRESHOLD: return config.FALLBACK_CATEGORY, 0, "Gemini (Failed)"

            return cat, conf, "Gemini (Cloud)"
        except Exception as e:
            print(f"  [Error] Gemini Error: {e}")
            return config.FALLBACK_CATEGORY, 0, "Gemini (Failed)"

    def _classify_with_ollama(self, file_name, content):
        prompt = f"""Task: Classify text into exactly one category: {', '.join(config.CATEGORIES)}.
Output Format: JSON with keys "category" and "confidence".
Constraint: No chat, no markdown.

Input Text:
{content}

Response:"""
        
        log_request(file_name, prompt)

        try:
            response = ollama.chat(model=config.MODEL_NAME, messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            content_str = response['message']['content']
            # print(f"  [Debug] AI Raw Output: {content_str[:100]}...")
            
            json_match = re.search(r'\{.*\}', content_str, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                    cat = result.get('category', config.FALLBACK_CATEGORY)
                    conf = result.get('confidence', 0)
                    
                    if cat not in config.CATEGORIES: cat = config.FALLBACK_CATEGORY
                    if conf < config.CONFIDENCE_THRESHOLD: cat = config.FALLBACK_CATEGORY
                    
                    return cat, conf, f"Ollama ({config.MODEL_NAME})"
                except:
                    pass
        except Exception as e:
            print(f"  [Error] Ollama Error: {e}")
            
        return config.FALLBACK_CATEGORY, 0, "Ollama (Failed)"
