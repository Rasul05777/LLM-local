import requests
import time
from config.config import MODEL_NAME, OLLAMA_API_GENERATE, OLLAMA_API_TAGS, MODEL_CHECK_TIMEOUT

class OllamaService:
    def __init__(self):
        self.model_name = MODEL_NAME
    
    def is_model_ready(self):
        """Проверяет, готова ли модель."""
        for _ in range(MODEL_CHECK_TIMEOUT):
            try:
                response = requests.get(OLLAMA_API_TAGS)
                response.raise_for_status()
                models = response.json().get("models", [])
                return any(model["name"] == self.model_name for model in models)
            except requests.RequestException:
                time.sleep(1)
        return False
    
    def generate_response(self, prompt):
        """Отправляет запрос к модели и возвращает ответ."""
        try:
            response = requests.post(
                OLLAMA_API_GENERATE,
                json={"model": self.model_name, "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            return response.json().get("response", "No response received.")
        except requests.RequestException as e:
            return f"Error: Failed to get response: {str(e)}"