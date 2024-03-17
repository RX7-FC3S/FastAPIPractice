from fastapi_pagination import Params as PaginationParams, paginate
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post("/add_bin_spec", response_model=schema.Response.AddBinSpec, tags=["库位规格", "增"])
async def add_bin_spec(params: schema.Request.AddBinSpec, db: Session = Depends(create_session)):
    try:
        db_bin_spec = crud.crud_bin_spec.get_by_name(db, params.bin_spec_name)

        if db_bin_spec:
            return Response(False, "BinSpec already exists", db_bin_spec)

        return Response(True, "", crud.crud_bin_spec.add(db, model.BinSpec(**params.model_dump())))

    except Exception as e:
        return Response(False, str(e), None)


@router.post("/get_bin_specs", response_model=schema.Response.GetBinSpecs, tags=["库位规格", "查"])
async def get_bin_specs(
    query_params: schema.Request.GetBinSpecs, pagination_params: PaginationParams, db: Session = Depends(create_session)
):
    try:
        return Response(True, "", paginate(crud.crud_bin_spec.get_bin_specs(db, query_params), pagination_params))
    except Exception as e:
        return Response(False, str(e), None)


@router.get(
    "/get_bin_specs_id_and_name", response_model=schema.Response.GetBinSpecsIdAndName, tags=["库位规格", "用于选择框"]
)
async def add_item(db: Session = Depends(create_session)):
    return Response(True, "", crud.crud_bin_spec.get_bin_specs_id_and_name(db))
