from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import upload
import uvicorn
import os

app = FastAPI(title="ASTRA MVP", description="Heuristic + RAG Explainability System")

# Include routes
app.include_router(upload.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/index.html")
async def index_html():
    return FileResponse("static/index.html")

@app.get("/static/index.html")
async def static_index_html():
    return FileResponse("static/index.html")

@app.get("/analysis.html")
async def analysis_html():
    return FileResponse("static/analysis.html")

@app.get("/static/analysis.html")
async def static_analysis_html():
    return FileResponse("static/analysis.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
