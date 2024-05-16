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
    "/add_inbound_order_header",
    response_model=schema.Response.AddInboundOrderHeader,
    tags=["入库订单头"],
)
def add_inbound_order_header(
    params: schema.Request.AddInboundOrderHeader, db: Session = Depends(create_session)
):
    try:
        db_inbound_order_header = (
            crud.crud_inbound_order_header.get_by_inbound_order_number(
                db, params.inbound_order_number
            )
        )
        if db_inbound_order_header:
            return Response(
                False,
                f"入库订单号({params.inbound_order_number})已被使用",
                db_inbound_order_header[0],
            )

        res = crud.crud_inbound_order_header.add(
            db, model.InboundOrderHeader(**params.model_dump())
        )
        print(res)
        return Response(True, "", res)

    except Exception as e:
        return Response(False, str(e), None)


@router.delete(
    "/delete_inbound_order_header",
    response_model=schema.Response.DeleteInboundOrderHeader,
    tags=["入库订单头"],
)
def delete_inbound_order_header(id: int, db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_inbound_order_header.delete(db, id))
    except Exception as e:
        return Response(False, str(e), None)


@router.put(
    "/update_inbound_order_header",
    response_model=schema.Response.UpdateInboundOrderHeader,
)
def update_inbound_order_header(
    params: schema.Request.UpdateInboundOrderHeader,
    db: Session = Depends(create_session),
):
    try:
        print('*'*100)
        return Response(
            True,
            "",
            crud.crud_inbound_order_header.update(
                db, model.InboundOrderHeader(**params.model_dump())
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_inbound_order_headers",
    response_model=schema.Response.GetInboundOrderHeaders,
    tags=["入库订单头"],
)
def get_inbound_order_headers(
    query_params: schema.Request.GetInboundOrderHeaders,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_inbound_order_header.get_inbound_order_headers(
                    db, query_params, order_params
                ),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.get(
    "/get_inbound_order_header_by_id",
    response_model=schema.Response.GetInboundOrderHeaderById,
    tags=["入库订单头"],
)
def get_inbound_order_header_by_id(
    id: int,
    db: Session = Depends(create_session),
):
    try:
        db_inbound_order_header = crud.crud_inbound_order_header.get(db, id)
        if not db_inbound_order_header:
            return Response(False, f"入库订单(id={id})不存在", None)
        return Response(True, "", db_inbound_order_header)
    except Exception as e:
        return Response(False, str(e), None)
