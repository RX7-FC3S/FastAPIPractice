from common.crud import CRUDBase, Session
from utils import advanced_query_and_sort
from sqlmodel import select

from . import model
from . import schema


class CRUDItem(CRUDBase[model.ItemInfo]):

    def get_by_item_code(self, db: Session, item_code: str):
        stmt = select(model.ItemInfo).where(model.ItemInfo.item_code == item_code)
        return db.exec(stmt).all()

    def get_items(self, db: Session, params: schema.Request.GetItems):
        stmt = advanced_query_and_sort(model.ItemInfo, params)
        return db.exec(stmt).all()


crud_item = CRUDItem(model.ItemInfo)
