# ollama_client.py
import requests
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

timeout_large = int(os.getenv("timeout"))


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> dict:
        """Call Ollama generate API"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": stream},
            timeout=timeout_large
        )
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> list:
        """List available models"""
        response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()
        return [m["name"] for m in response.json().get("models", [])]


# Add streaming option to speed up parsing of CSV files
def generate_stream(self, model: str, prompt: str):
    """Stream response from Ollama"""
    response = requests.post(
        f"{self.base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True,
        timeout=300
    )
    response.raise_for_status()
    
    full_response = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if 'response' in chunk:
                full_response += chunk['response']
    
    return {"response": full_response}