from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import crud
from . import model
from . import schema

from ..bin_spec.crud import crud_bin_spec
from ..warehouse_area.crud import crud_warehouse_area

router = APIRouter()


@router.post(
    "/add_bin_info", response_model=schema.Response.AddBinInfo, tags=["库位信息"]
)
def add_bin_info(
    params: schema.Request.AddBinInfo, db: Session = Depends(create_session)
):
    try:
        db_bin_info = crud.crud_bin_info.get_by_bin_code(db, params.bin_code)

        if db_bin_info:
            return Response(
                False, f"BinInfo(bin_code:{params.bin_code}) already exists", None
            )
        db_bin_info = crud.crud_bin_info.get_bin_info_by_row_col_and_level(
            db, params.row, params.col, params.level
        )

        if db_bin_info:
            return Response(
                False,
                f"BinInfo(row:{params.row}, col:{params.col}, level:{params.level}) already exists",
                None,
            )
        db_bin_spec = crud_bin_spec.get(db, params.bin_spec_id)
        if not db_bin_spec:
            return Response(
                False, f"BinSpec(id:{params.bin_spec_id}) does not exists", None
            )
        db_warehouse_area = crud_warehouse_area.get(db, params.warehouse_area_id)
        if not db_warehouse_area:
            return Response(
                False,
                f"WarehouseArea(id:{params.warehouse_area_id}) does not exists",
                None,
            )

        bin = model.BinInfo(**params.model_dump())

        return Response(True, "", crud.crud_bin_info.add(db, bin))

    except Exception as e:
        return Response(False, str(e), None)


@router.delete(
    "/delete_bin_info", response_model=schema.Response.DeleteBinInfo, tags=["库位信息"]
)
def delete_bin_info(
    params: schema.Request.DeleteBinInfo, db: Session = Depends(create_session)
):
    try:
        return Response(True, "", crud.crud_bin_info.delete(db, params.id))
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_bin_infos", response_model=schema.Response.GetBinInfos, tags=["库位信息"]
)
async def get_bin_infos(
    query_params: schema.Request.GetBinInfos,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    return Response(
        True,
        "",
        paginate(
            crud.crud_bin_info.get_bin_infos(db, query_params, order_params),
            pagination_params,
        ),
    )
