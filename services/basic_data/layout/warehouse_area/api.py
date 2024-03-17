from fastapi_pagination import Params as PaginationParams, paginate
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import crud
from . import model
from . import schema

router = APIRouter()


@router.post("/add_warehouse_areas", response_model=schema.Response.AddWarehouseArea, tags=["库区", "增"])
def add_warehouse_area(params: schema.Request.AddWarehouseArea, db: Session = Depends(create_session)) -> Response:
    try:
        db_warehouse_area = crud.crud_warehouse_area.get_by_code(db, params.warehouse_area_code)
        if db_warehouse_area:
            return Response(False, "Warehouse area already exists", db_warehouse_area)

        warehouse_area = model.WarehouseArea(**params.model_dump())
        return Response(True, "", crud.crud_warehouse_area.add(db, warehouse_area))
    except Exception as e:
        return Response(False, str(e), None)


@router.post("/get_warehouse_areas", response_model=schema.Response.GetWarehouseAreas, tags=["库区", "查"])
def get_warehouse_areas(
    query_params: schema.Request.GetWarehouseAreas,
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True, "", paginate(crud.crud_warehouse_area.get_warehouse_areas(db, query_params), pagination_params)
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.get(
    "/get_warehouse_areas_id_and_name",
    response_model=schema.Response.GetWarehouseAreasIdAndName,
    tags=["库区", "用于选择框"],
)
def get_warehouse_areas_id_and_name(db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_warehouse_area.get_warehouse_areas_id_and_name(db))
    except Exception as e:
        return Response(False, str(e), None)
