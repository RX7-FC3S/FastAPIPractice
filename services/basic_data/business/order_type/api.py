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
    "/add_order_type",
    response_model=schema.Response.AddOrderType,
    tags=["订单类型"],
)
def add_order_type(
    params: schema.Request.AddOrderType, db: Session = Depends(create_session)
):
    try:
        return Response(True, "添加订单类型成功", None)
    except Exception as e:
        return Response(False, str(e), None)


@router.post(
    "/get_order_types",
    response_model=schema.Response.GetOrderTypes,
    tags=["订单类型"],
)
def get_order_types(
    query_params: schema.Request.GetOrderTypes,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_order_type.get_order_types(db, query_params, order_params),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)


@router.get(
    "/get_order_types_by_business_type",
    response_model=schema.Response.GetOrderTypesByBusinessType,
    tags=["订单类型"],
)
def get_order_types_by_business_type(
    params: schema.Request.GetOrderTypesByBusinessType = Depends(),
    db: Session = Depends(create_session),
):
    return Response(
        True,
        "",
        crud.crud_order_type.get_order_types_by_business_type(db, params.business_type),
    )
