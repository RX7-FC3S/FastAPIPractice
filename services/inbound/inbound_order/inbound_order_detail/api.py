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
from services.inbound.inbound_order.inbound_order_header.crud import crud_inbound_order_header

router = APIRouter()


@router.post(
    "/add_inbound_order_detail",
    response_model=schema.Response.AddInboundOrderDetail,
    tags=["入库订单", "入库订单明细"],
)
def add_inbound_order_detail(params: schema.Request.AddInboundOrderDetail, db: Session = Depends(create_session)):
    try:
        db_inbound_order_header = crud_inbound_order_header.get(db, params.inbound_order_header_id)

        if not db_inbound_order_header:
            return Response(
                False,
                f"入库订单(id={params.inbound_order_header_id})不存在",
                None,
            )

        db_inbound_order_details = db_inbound_order_header.inbound_order_details
        current_seq = (len(db_inbound_order_details) if db_inbound_order_details else 0) + 1

        db_item = crud_item_info.get(db, params.item_id)

        if not db_item:
            return Response(
                False,
                f"物料(id={params.item_id})不存在",
                None,
            )

        assert db_item.id is not None
        db_item_base_unit = crud_item_unit.get_item_base_unit_bu_item_id(db, db_item.id)
        current_item_unit = crud_item_unit.get(db, params.item_id)
        assert current_item_unit and db_item_base_unit is not None
        quantity_of_pieces = (
            params.quantity
            if params.item_id == db_item_base_unit.id
            else current_item_unit.conversion_quantity * params.quantity
        )

        inbound_order_detail = model.InboundOrderDetail(
            seq=current_seq,
            **params.model_dump(exclude_none=True),
            quantity_of_pieces=quantity_of_pieces,
        )

        return Response(True, "", crud.crud_inbound_order_detail.add(db, inbound_order_detail))
    except Exception as e:
        return Response(False, str(e), None)


@router.delete("/delete_inbound_order_detail", response_model=schema.Response.DeleteInboundOrderDetail)
def delete_inbound_order_detail(id: int, db: Session = Depends(create_session)):
    try:
        return Response(True, "", crud.crud_inbound_order_detail.delete(db, id))
    except Exception as e:
        return Response(False, str(e), None)


@router.post("/get_inbound_order_details", response_model=schema.Response.GetInboundOrderDetails)
def get_inbound_order_details(
    query_params: schema.Request.GetInboundOrderDetails,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_inbound_order_detail.get_inbound_order_details(db, query_params, order_params),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)
