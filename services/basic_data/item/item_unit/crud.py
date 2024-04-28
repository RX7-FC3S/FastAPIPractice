from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model


class CRUDItemUnit(CRUDBase[model.ItemUint]):
    def get_item_units_by_item_id(self, db: Session, item_id: int):
        stmt = select(self.model).where(self.model.item_id == item_id)
        return db.exec(stmt).all()


crud_item_unit = CRUDItemUnit(model.ItemUint)
