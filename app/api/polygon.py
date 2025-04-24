from app.models.polygon import Polygon
from app.models.response import Response
from fastapi import APIRouter
from typing import Annotated, List, Optional, Tuple
from app.services.polygon_service import PolygonService
from fastapi.responses import JSONResponse
from app.di import container
from http import HTTPStatus

router = APIRouter(prefix="", tags=["polygon"])


@router.get("/{polygon_id}", response_model=Response[Polygon])
async def get_polygon_by_id(
    polygon_id: int, 
    polygon_service: Annotated[PolygonService, container.depends(PolygonService)]
):
    existing_polygon = polygon_service.get_polygon_by_id(polygon_id)
    if not existing_polygon:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Polygon not found")
            .dict(by_alias=True),
        )
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Polygon].success_response(existing_polygon).dict(by_alias=True),
    )

@router.post("/")
async def create_polygon(
    polygon_service: Annotated[PolygonService, container.depends(PolygonService)],
    name: str,
    coordinates: List[List[Tuple[float, float]]]
):
    # Create new polygon with only the required fields
    polygon = Polygon(name=name, coordinates=coordinates)
    polygon = polygon_service.create_polygon(polygon)
    
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=Response[Polygon].success_response(polygon).dict(by_alias=True),
    )

@router.put("/{polygon_id}")
async def update_polygon(
    polygon_id: int, 
    polygon_service: Annotated[PolygonService, container.depends(PolygonService)],
    name: Optional[str] = None,
    coordinates: Optional[List[List[Tuple[float, float]]]] = None,
):
    existing_polygon = polygon_service.get_polygon_by_id(polygon_id)
    
    if not existing_polygon:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Polygon not found")
            .dict(by_alias=True),
        )
    
    if name is not None:
        existing_polygon.name = name
    if coordinates is not None:
        existing_polygon.coordinates = coordinates
    
    updated_polygon =  polygon_service.update_polygon(polygon_id, existing_polygon)
    
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Polygon].success_response(updated_polygon).dict(by_alias=True),
    )

@router.delete("/{polygon_id}", status_code=204)
async def delete_polygon(
    polygon_id: int, 
    polygon_service: Annotated[PolygonService, container.depends(PolygonService)],
):
    deleted_polygon = polygon_service.delete_polygon(polygon_id)
    if not deleted_polygon:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Polygon not found")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[str]
        .success_response("Polygon deleted successfully")
        .dict(by_alias=True),
    )