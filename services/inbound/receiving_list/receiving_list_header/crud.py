from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select, alias

from . import model
from . import schema

from services.basic_data.business.order_type.model import OrderType
from services.basic_data.business.stakeholder.model import Stakeholder


class CRUDReceivingListHeader(CRUDBase[model.ReceivingListHeader]):
    def get_by_inbound_order_number(self, db: Session, receiving_list_number: str):
        stmt = select(self.model).where(
            self.model.receiving_list_number == receiving_list_number
        )
        return db.exec(stmt).all()

    def get_receiving_list_headers(
        self,
        db: Session,
        query_params: schema.Request.GetReceivingListHeaders,
        order_params: list[AdvancedOrderField],
    ):
    
        stmt = advanced_query_and_order(
            self.model,
            query_params,
            order_params,
            mappings={"order_type": OrderType},
        )        
        return db.exec(stmt).all()


crud_receiving_list_header = CRUDReceivingListHeader(model.ReceivingListHeader)
