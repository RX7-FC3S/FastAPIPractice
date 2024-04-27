from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema
from services.basic_data.item.item_info.model import ItemInfo


class CRUDItemUnit(CRUDBase[model.ItemUint]):
    def get_item_units_by_item_code(self, db: Session, item_code: str):
        stmt = select(model.ItemUint).join(ItemInfo).where(ItemInfo.item_code == item_code)
        return db.exec(stmt).all()


crud_item_unit = CRUDItemUnit(model.ItemUint)
