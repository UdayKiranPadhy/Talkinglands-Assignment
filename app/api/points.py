from app.models.response import Response
from fastapi import APIRouter, Query
from typing import Annotated, Optional
from app.models.point import Latitude, Longitude, Point
from app.services.points_service import PointsService
from app.di import container
from fastapi.responses import JSONResponse
from http import HTTPStatus

router = APIRouter(prefix="", tags=["points"])


@router.get("/", response_model=Response[Point])
async def get_point_based_on_latitude_and_longitude(
    points_service: Annotated[
        PointsService, container.depends(PointsService)
    ],
    latitude: Annotated[Optional[Latitude], Query()] = None,
    longitude: Annotated[Optional[Longitude], Query()] = None,
):
    if not latitude or not longitude:
        response = Response[None].error_response(
            "Latitude and Longitude are required"
        )
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=response.dict(by_alias=True),
        )
    
    
    point = points_service.get_point_based_on_latitude_and_longitude(latitude, longitude)
    
    if not point:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None].error_response("Hub not found").dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Point].success_response(point).dict(by_alias=True),
    )