from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post("/add_bin_spec", response_model=schema.Response.AddBinSpec)
async def add_bin_spec(params: schema.Request.AddBinSpec, db: Session = Depends(create_session)):
    try:
        db_bin_spec = crud.crud_bin_spec.get_by_name(db, params.bin_spec_name)

        if db_bin_spec:
            return Response(False, "BinSpec already exists", db_bin_spec)

        return Response(True, "", crud.crud_bin_spec.add(db, model.BinSpec(**params.model_dump())))

    except Exception as e:
        return Response(False, str(e), None)


@router.get("/get_bin_specs", response_model=schema.Response.GetBinSpecs)
async def get_bin_specs(params: schema.Request.GetBinSpecs, db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_bin_spec.get_bin_specs(db, params))
    except Exception as e:
        return Response(False, str(e), None)
