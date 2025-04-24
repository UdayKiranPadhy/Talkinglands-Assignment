from fastapi import APIRouter


router = APIRouter(prefix="")

@router.get("/")
async def get_polygon():
    """
    Get polygon
    """
    return {"message": "Get polygon"}