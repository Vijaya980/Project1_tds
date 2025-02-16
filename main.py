# /// script
# dependencies = [
#   "fastapi",
#   "requests",
#   "python-dotenv",
#   "uvicorn",
#   "python-dotenv",
#   "beautifulsoup4",
#   "markdown",
#   "requests<3",
#   "duckdb",
#   "numpy",
#   "python-dateutil",
#   "docstring-parser",
#   "httpx",
#   "scikit-learn",
#   "pydantic",
# ]
# ///



from fastapi import FastAPI, HTTPException, Query
from utils import read_file, write_file, list_files
from agent import execute_task
import logging
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel



import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Define request model for /v1/completions
class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int
    
    
@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    """Simulated LLM completion API"""
    try:
        # Dummy response for now
        response_text = f"Generated text based on: {request.prompt}"
        return {"status": "success", "response": response_text}
    except Exception as e:
        logger.error(f"Error processing completion request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))



@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English")):
    try:
        result = execute_task(task)
        return {"status": "success", "output": result}
    except ValueError as e:
        logger.error(f"Error executing task: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@app.get("/read")
async def read_file_api(path: str = Query(..., description="Path to the file")):
    try:
        content = read_file(path)
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading file: " + str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)