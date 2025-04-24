from fastapi import FastAPI
from app.api import points, polygon

application = FastAPI()

# Include API router
application.include_router(points.router, prefix="/points")
application.include_router(polygon.router, prefix="/polygons")

