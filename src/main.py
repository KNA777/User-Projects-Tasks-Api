import sys
import uvicorn
from fastapi import FastAPI, responses
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.api import main_router

app = FastAPI(description="<h1>User Api Project</h1>")

@app.get("/", include_in_schema=False)
async def root():
    return responses.RedirectResponse(url="/docs")

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
