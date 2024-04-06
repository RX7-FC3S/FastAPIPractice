from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDOrderType(CRUDBase[model.OrderType]):
    def get_order_types(self, db: Session, query_params:schema.Request.GetOrderTypes, order_params:list[AdvancedOrderField]):
        stmt = advanced_query_and_order(model.OrderType, query_params, order_params)
        return db.exec(stmt).all()

crud_order_type = CRUDOrderType(model.OrderType)
