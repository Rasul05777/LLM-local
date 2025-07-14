import requests
from config.config import MODEL_NAME, OLLAMA_API_GENERATE, OLLAMA_API_TAGS

class OllamaService:
    def __init__(self):
        self.model_name = MODEL_NAME
    
    def is_model_ready(self):
        try:
            response = requests.get(OLLAMA_API_TAGS, timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            print(f"Available models: {models}")  
            prefix = self.model_name.split(":")[0]
            for model in models:
                name = model.get("name", "")
                if name == self.model_name or name.startswith(prefix):
                    self.model_name = name
                    print(f"Model found: {name}")
                    return True
            print("No matching model found")
            return False
        except requests.RequestException as e:
            print(f"Error checking model readiness: {str(e)}")
            return False
    
    def generate_response(self, prompt):
        try:
            response = requests.post(
                OLLAMA_API_GENERATE,
                json={"model": self.model_name, "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            return response.json().get("response", "No response received.")
        except requests.RequestException as e:
            return f"Error: Failed to get response: {str(e)}"