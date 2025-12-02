# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from schemas import Query
from processors import process_csv_content
from ollama_client import OllamaClient
import requests
from dotenv import load_dotenv, dotenv_values
import pandas as pd 

app = FastAPI(title="Ollama CSV Analyzer")
ollama = OllamaClient()
load_dotenv()



@app.get("/")
async def root():
    return {
        "message": "Ollama CSV Analysis API",
        "endpoints": {
            "POST /generate": "Generate text with Ollama",
            "POST /analyze_csv": "Upload and analyze CSV files"
        }
    }

@app.post("/generate")
async def generate_text(query: Query):
    """Generate text using Ollama"""
    try:
        result = ollama.generate(query.model, query.prompt)
        return {"response": result["response"]}
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Cannot connect to Ollama. Is it running?"
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_csv")
async def analyze_csv(
    file: UploadFile = File(...),
    prompt: str = "Analyze this CSV data:",
    model: str = "gemma3:12b"
):
    """Upload and analyze a CSV file"""
    
    # Validate file type
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="Only CSV files are supported"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Process CSV (pure function from processors.py)
        csv_data = process_csv_content(content)
        
        # Combine user prompt with data context
        full_prompt = f"{prompt}\n\n{csv_data['summary']}"
        
        # Call Ollama
        result = ollama.generate(model, full_prompt)
        
        return {
            "analysis": result["response"],
            "file_info": {
                "filename": file.filename,
                "rows": csv_data["rows"],
                "columns": csv_data["columns"],
                "column_names": csv_data["column_names"]
            }
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)