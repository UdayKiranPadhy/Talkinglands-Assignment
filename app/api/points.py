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
    points_service: Annotated[PointsService, container.depends(PointsService)],
    latitude: Annotated[Optional[Latitude], Query()] = None,
    longitude: Annotated[Optional[Longitude], Query()] = None,
):
    if not latitude or not longitude:
        response = Response[None].error_response("Latitude and Longitude are required")
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=response.dict(by_alias=True),
        )

    point = points_service.get_point_based_on_latitude_and_longitude(
        latitude, longitude
    )

    if not point:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Point not found")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Point].success_response(point).dict(by_alias=True),
    )


@router.get("/{point_id}", response_model=Response[Point])
async def get_point_by_id(
    points_service: Annotated[PointsService, container.depends(PointsService)],
    point_id: int,
):
    point = points_service.get_point_based_on_point_id(point_id)

    if not point:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Point not found")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Point].success_response(point).dict(by_alias=True),
    )


@router.delete("/{point_id}")
async def delete_point(
    points_service: Annotated[PointsService, container.depends(PointsService)],
    point_id: int,
):
    point = points_service.delete_point(point_id)

    if not point:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Point not found")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[None]
        .success_response("Point deleted successfully")
        .dict(by_alias=True),
    )


@router.post("/", response_model=Response[Point])
async def create_point(
    points_service: Annotated[PointsService, container.depends(PointsService)],
    point_name: str,
    latitude: Latitude,
    longitude: Longitude,
):
    existing_point = points_service.get_point_based_on_latitude_and_longitude(
        latitude, longitude
    )
    if existing_point:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=Response[Point]
            .error_response("Point already exists", existing_point)
            .dict(by_alias=True),
        )

    point = Point(
        id=None, point_name=point_name, latitude=latitude, longitude=longitude
    )
    point = points_service.create_point(point)

    if not point:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=Response[None]
            .error_response("Failed to create point")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=Response[Point].success_response(point).dict(by_alias=True),
    )


@router.put("/{point_id}", response_model=Response[Point])
async def update_point(
    points_service: Annotated[PointsService, container.depends(PointsService)],
    point_id: int,
    point_name: Optional[str] = None,
    latitude: Optional[Latitude] = None,
    longitude: Optional[Longitude] = None,
):
    if not any([point_name, latitude, longitude]):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=Response[None]
            .error_response("At least one field to update is required")
            .dict(by_alias=True),
        )

    if (latitude is None) != (longitude is None):  # One is None and the other isn't
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=Response[None]
            .error_response("Both latitude and longitude must be provided together")
            .dict(by_alias=True),
        )

    updated_point = points_service.update_point(
        point_id, point_name, latitude, longitude
    )

    if not updated_point:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=Response[None]
            .error_response("Point not found")
            .dict(by_alias=True),
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=Response[Point].success_response(updated_point).dict(by_alias=True),
    )
