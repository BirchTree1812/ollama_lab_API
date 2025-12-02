# schemas.py
from pydantic import BaseModel

class Query(BaseModel):
    prompt: str
    model: str = "gemma3:12b"

class AnalysisResponse(BaseModel):
    analysis: str
    file_info: dict