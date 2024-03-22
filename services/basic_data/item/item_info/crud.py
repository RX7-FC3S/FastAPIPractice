from common.schema import AdvancedOrderField
from common.crud import CRUDBase, Session
from utils import advanced_query_and_order
from sqlmodel import select

from . import model
from . import schema


class CRUDItem(CRUDBase[model.ItemInfo]):

    def get_by_item_code(self, db: Session, item_code: str):
        stmt = select(model.ItemInfo).where(model.ItemInfo.item_code == item_code)
        return db.exec(stmt).all()

    def get_items(self, db: Session, query_params: schema.Request.GetItems, order_params: list[AdvancedOrderField]):
        stmt = advanced_query_and_order(model.ItemInfo, query_params, order_params)
        return db.exec(stmt).all()


crud_item = CRUDItem(model.ItemInfo)
