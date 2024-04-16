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
    tags=["增", "入库订单"],
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
                False, "Inbound order header already exists", db_inbound_order_header
            )

        return Response(
            True,
            "",
            crud.crud_inbound_order_header.add(
                db, model.InboundOrderHeader(**params.model_dump())
            ),
        )

    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_inbound_order_headers",
    response_model=schema.Response.GetInboundOrderHeaders,
    tags=["查", "入库订单"],
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
