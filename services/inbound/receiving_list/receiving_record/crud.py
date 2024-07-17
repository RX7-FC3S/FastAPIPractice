from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDReceivingRecord(CRUDBase[model.ReceivingListDetail]):
    

    def get_receiving_records(
        self,
        db: Session,
        query_params: schema.Request.GetReceivingListDetails,
        order_params: list[AdvancedOrderField],
    ):
        stmt = advanced_query_and_order(
            self.model, query_params, order_params, mappings={}
        )
        return db.exec(stmt).all()


crud_receiving_record = CRUDReceivingRecord(model.ReceivingListDetail)
