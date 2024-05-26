from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select, Sequence

from . import model


class CRUDItemUnit(CRUDBase[model.ItemUnit]):

    def get_item_units(self, db: Session, query_params, order_params):
        stmt = advanced_query_and_order(model.ItemUnit, query_params, order_params)
        return db.exec(stmt).all()

    def get_item_units_by_item_info_id(self, db: Session, item_info_id: int):
        stmt = select(self.model).where(self.model.item_info_id == item_info_id)
        return db.exec(stmt).all()

    def get_item_base_unit_by_item_info_id(
        self, db: Session, item_info_id: int
    ) -> model.ItemUnit | None:
        stmt = select(self.model).where(
            self.model.item_info_id == item_info_id, self.model.unit_type == 0
        )
        return db.exec(stmt).first()


crud_item_unit = CRUDItemUnit(model.ItemUnit)
