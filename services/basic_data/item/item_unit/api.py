from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud

router = APIRouter()


@router.post("/add_item_unit", response_model=schema.Response.AddItemUnit, tags=["物料单位", "增"])
def add_item_unit(params: schema.Request.AddItemUnit, db: Session = Depends(create_session)):
    return crud.crud_item_unit.add(db, model.ItemUint(**params.model_dump()))


@router.post("/get_item_units", response_model=schema.Response.GetItemUnits)
def get_item_units(
    query_params: schema.Request.GetItemUnits,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):

    return Response(
        True,
        "",
        paginate(
            crud.crud_item_unit.get_item_units(
                db,
                query_params,
                order_params,
            ),
            pagination_params,
        ),
    )


@router.get("/get_item_units_by_item_id", response_model=schema.Response.GetItemUnitsByItemId)
def get_item_units_by_item_id(item_id: int, db: Session = Depends(create_session)):
    try:
        return Response(
            True,
            "",
            crud.crud_item_unit.get_item_units_by_item_id(db, item_id),
        )
    except Exception as e:
        return Response(False, str(e), None)
