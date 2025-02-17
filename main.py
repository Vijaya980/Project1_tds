

from fastapi import FastAPI, HTTPException, Query
from utils import read_file, write_file, list_files
from agent import execute_task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() #lifespan=lifespan)

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
        logger.error(f"File not found: {path}")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail="Error reading file: " + str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)