from common.crud import CRUDBase, Session
from utils import advanced_query_and_sort
from sqlmodel import select

from . import model
from . import schema


class CRUDWarehouseArea(CRUDBase[model.WarehouseArea]):

    def get_by_code(self, db: Session, warehouse_area_code: str):
        stmt = select(model.WarehouseArea).where(model.WarehouseArea.warehouse_area_code == warehouse_area_code)
        return db.exec(stmt).all()

    def get_warehouse_areas(self, db: Session, params: schema.Request.GetWarehouseAreas):
        stmt = advanced_query_and_sort(model.WarehouseArea, params, {})
        return db.exec(stmt).all()

    def get_warehouse_areas_id_and_name(self, db: Session):
        stmt = select(model.WarehouseArea.id, model.WarehouseArea.warehouse_area_name)
        return db.exec(stmt).all()


crud_warehouse_area = CRUDWarehouseArea(model.WarehouseArea)
