from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDInboundOrderDetail(CRUDBase[model.InboundOrderDetail]):
    def get_inbound_order_details(
        self,
        db: Session,
        query_params: schema.Request.GetInboundOrderDetails,
        order_params: list[AdvancedOrderField],
    ):
        stmt = advanced_query_and_order(
            self.model, query_params, order_params, mappings={}
        )
        return db.exec(stmt).all()


crud_inbound_order_detail = CRUDInboundOrderDetail(model.InboundOrderDetail)
