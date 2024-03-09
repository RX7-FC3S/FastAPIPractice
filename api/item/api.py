from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import create_session
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post("/add_item", response_model=schema.Response.AddItem)
async def add_item(params: schema.Request.AddItem, db: Session = Depends(create_session)):
    db_item = crud.crud_item.get_by_item_code(db, params.item_code)

    if db_item:
        return Response(False, "Item already exists", db_item)

    return Response(True, "", crud.crud_item.add(db, model.Item(**params.model_dump())))
