from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud

from services.basic_data.item.item_info.crud import crud_item_info
from services.basic_data.item.item_unit.crud import crud_item_unit
from services.inbound.receiving_list.receiving_list_header.crud import (
    crud_receiving_list_header,
)

router = APIRouter()


@router.post(
    "/add_receiving_list_detail",
    response_model=schema.Response.AddReceivingListDetail,
    tags=["收货单"],
)
def add_receiving_list_detail(
    params: schema.Request.AddReceivingListDetail, db: Session = Depends(create_session)
):
    try:
        db_receiving_list_header = crud_receiving_list_header.get(
            db, params.receiving_list_header_id
        )

        if not db_receiving_list_header:
            return Response(
                False,
                f"入库订单(id={params.receiving_list_header_id})不存在",
                None,
            )

        db_receiving_list_details = sorted(
            db_receiving_list_header.receiving_list_details, key=lambda x: x.seq
        )

        last_seq = db_receiving_list_details[-1].seq if db_receiving_list_details else 0
        db_item_info = crud_item_info.get(db, params.item_info_id)

        if not db_item_info:
            return Response(
                False,
                f"物料(id={params.item_info_id})不存在",
                None,
            )

        receiving_list_detail = model.ReceivingListDetail(
            seq=last_seq + 1,
            **params.model_dump(exclude_none=True),
        )

        return Response(
            True, "", crud.crud_receiving_list_detail.add(db, receiving_list_detail)
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.delete(
    "/delete_receiving_list_detail",
    response_model=schema.Response.DeleteReceivingListDetail,
    tags=["收货单"],
)
def delete_receiving_list_detail(id: int, db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_receiving_list_detail.delete(db, id))
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_receiving_list_details",
    response_model=schema.Response.GetReceivingListDetails,
    tags=["收货单"],
)
def get_receiving_list_details(
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
                crud.crud_receiving_list_detail.get_receiving_list_details(
                    db, query_params, order_params
                ),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_receiving_list_details_without_header",
    response_model=schema.Response.GetReceivingListDetailsWithoutHeader,
    tags=["收货单"],
)
def get_receiving_list_details_without_header(
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
                crud.crud_receiving_list_detail.get_receiving_list_details(
                    db, query_params, order_params
                ),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)