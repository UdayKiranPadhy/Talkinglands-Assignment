from fastapi import APIRouter


router = APIRouter(prefix="")

@router.get("/")
async def get_points():
    """
    Get points
    """
    return {"message": "Get points"}