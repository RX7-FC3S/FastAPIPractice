from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud

from services.inbound.receiving_list.receiving_list_detail.crud import (
    crud_receiving_list_detail,
)

from .schema import RequestAddReceivingRecord, RequestAddReceivingRecords


router = APIRouter()


@router.post("/add_receiving_record", response_model=schema.Response.AddReceivingRecord)
def add_receiving_record(
    params: RequestAddReceivingRecord, db: Session = Depends(create_session)
):
    try:
        db_receiving_list_detail = crud_receiving_list_detail.get(db, params.id)
        if not db_receiving_list_detail:
            return Response(False, f"收货单明细(id={params.id})不存在", None)

        receiving_record = model.ReceivingRecord(
            receiving_list_detail_id=params.id,
            receiving_quantity=params.receiving_quantity,
        )
        db.add(receiving_record)
        db.commit()

        return Response(True, "收货成功!", None)
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_receiving_records",
    response_model=schema.Response.GetReceivingListDetails,
    tags=["收货记录"],
)
def get_receiving_records(
    query_params: schema.Request.GetReceivingListDetails,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_receiving_record.get_receiving_records(
                    db, query_params, order_params
                ),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)
