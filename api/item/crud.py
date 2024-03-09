from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDItem(CRUDBase[model.Item]):

    def get_by_item_code(self, db: Session, item_code: str):
        stmt = select(model.Item).where(model.Item.item_code == item_code)
        return db.exec(stmt).all()


crud_item = CRUDItem(model.Item)
