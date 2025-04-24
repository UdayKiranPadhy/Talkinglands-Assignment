from fastapi import FastAPI
from app.api import points

application = FastAPI()

# Include API router
application.include_router(points.router, prefix="/points")


@application.get("/")
async def root():
    return {"message": "Hello World"}
