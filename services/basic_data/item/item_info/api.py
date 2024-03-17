from fastapi_pagination import Params as PaginationParams, paginate
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post("/add_item", response_model=schema.Response.AddItem)
async def add_item(params: schema.Request.AddItem, db: Session = Depends(create_session)):
    try:
        db_item = crud.crud_item.get_by_item_code(db, params.item_code)

        if db_item:
            return Response(False, "Item already exists", db_item)

        return Response(True, "", crud.crud_item.add(db, model.ItemInfo(**params.model_dump())))

    except Exception as e:
        return Response(False, str(e), None)


@router.post("/get_items", response_model=schema.Response.GetItems)
async def get_items(
    query_params: schema.Request.GetItems, pagination_params: PaginationParams, db: Session = Depends(create_session)
):
    try:
        return Response(True, "", paginate(crud.crud_item.get_items(db, query_params), pagination_params))
    except Exception as e:
        return Response(False, str(e), None)
