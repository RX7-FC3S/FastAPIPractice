from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post(
    "/add_receiving_list_header",
    response_model=schema.Response.AddReceivingListHeader,
    tags=["收货单"],
)
def add_receiving_list_header(
    params: schema.Request.AddReceivingListHeader, db: Session = Depends(create_session)
):
    try:
        db_receiving_list_header = (
            crud.crud_receiving_list_header.get_by_inbound_order_number(
                db, params.receiving_list_number
            )
        )
        if db_receiving_list_header:
            return Response(
                False,
                f"入库订单号({params.receiving_list_number})已被使用",
                db_receiving_list_header[0],
            )

        res = crud.crud_receiving_list_header.add(
            db, model.ReceivingListHeader(**params.model_dump())
        )
        print(res)
        return Response(True, "", res)

    except Exception as e:
        return Response(False, str(e), None)


@router.delete(
    "/delete_receiving_list_header",
    response_model=schema.Response.DeleteReceivingListHeader,
    tags=["收货单"],
)
def delete_receiving_list_header(id: int, db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_receiving_list_header.delete(db, id))
    except Exception as e:
        return Response(False, str(e), None)


@router.put(
    "/update_receiving_list_header",
    response_model=schema.Response.UpdateReceivingListHeader,
    tags=["收货单"],
)
def update_receiving_list_header(
    params: schema.Request.UpdateReceivingListHeader,
    db: Session = Depends(create_session),
):
    try:
        print("*" * 100)
        return Response(
            True,
            "",
            crud.crud_receiving_list_header.update(
                db, model.ReceivingListHeader(**params.model_dump())
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_receiving_list_headers",
    response_model=schema.Response.GetReceivingListHeaders,
    tags=["收货单"],
)
def get_receiving_list_headers(
    query_params: schema.Request.GetReceivingListHeaders,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_receiving_list_header.get_receiving_list_headers(
                    db, query_params, order_params
                ),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.get(
    "/get_receiving_list_header_by_id",
    response_model=schema.Response.GetReceivingListHeaderById,
    tags=["收货单"],
)
def get_receiving_list_header_by_id(
    id: int,
    db: Session = Depends(create_session),
):
    try:
        db_receiving_list_header = crud.crud_receiving_list_header.get(db, id)
        if not db_receiving_list_header:
            return Response(False, f"入库订单(id={id})不存在", None)
        return Response(True, "", db_receiving_list_header)
    except Exception as e:
        return Response(False, str(e), None)
