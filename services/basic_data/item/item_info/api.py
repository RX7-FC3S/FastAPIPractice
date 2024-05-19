from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud

from services.basic_data.item.item_unit.model import ItemUint
from services.basic_data.item.item_unit.crud import crud_item_unit


router = APIRouter()


@router.post("/add_item_info", response_model=schema.Response.AddItemInfo)
async def add_item_info(params: schema.Request.AddItemInfo, db: Session = Depends(create_session)):
    try:
        db_item = crud.crud_item_info.get_item_by_item_code(db, params.item_code)

        if db_item:
            return Response(False, "Item already exists", db_item[0])

        db_item = crud.crud_item_info.add(db, model.ItemInfo(**params.model_dump()))

        assert db_item.id is not None
        crud_item_unit.add(db, ItemUint(item_id=db_item.id, unit_type=0, unit_name="PCS", conversion_quantity=1))

        return Response(True, "", db_item)

    except Exception as e:
        return Response(False, str(e), None)


@router.post("/get_item_infos", response_model=schema.Response.GetItemInfos)
async def get_item_infos(
    query_params: schema.Request.GetItemInfos,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_item_info.get_item_infos(db, query_params, order_params),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)
