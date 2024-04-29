from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud

from services.inbound.inbound_order.inbound_order_header.crud import crud_inbound_order_header
from services.basic_data.item.item_info.crud import crud_item

router = APIRouter()


@router.post(
    "/add_inbound_order_detail",
    response_model=schema.Response.AddInboundOrderDetail,
    tags=["入库订单", "入库订单明细", "增"],
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

        db_item = crud_item.get(db, params.item_id)
        if not db_item:
            return Response(
                False,
                f"物料(id={params.item_id})不存在",
                None,
            )
        inbound_order_detail = model.InboundOrderDetail(**params.model_dump())
        return Response(True, "", crud.crud_inbound_order_detail.add(db, inbound_order_detail))
    except Exception as e:
        return Response(False, str(e), None)
