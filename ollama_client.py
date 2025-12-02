# ollama_client.py
import requests

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> dict:
        """Call Ollama generate API"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": stream},
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> list:
        """List available models"""
        response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        response.raise_for_status()
        return [m["name"] for m in response.json().get("models", [])]