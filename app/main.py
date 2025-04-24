from fastapi import FastAPI
from app.api import points, polygon

app = FastAPI()

# Include API router
app.include_router(points.router, prefix="/points")
app.include_router(polygon.router, prefix="/polygon")


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Make sure to bind to 0.0.0.0 to allow external connections
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)