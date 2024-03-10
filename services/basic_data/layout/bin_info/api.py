from fastapi import APIRouter, Depends
from database import Session, create_session
from common.response import Response

from . import model
from . import crud
from . import schema

router = APIRouter()


@router.get("/get_bin_infos", response_model=schema.Response.GetBinInfos)
async def get_bin_infos(params: schema.Request.GetBinInfos, db: Session = Depends(create_session)):

    return Response(True, "", crud.crud_bin_info.get_bin_infos(db, params))
