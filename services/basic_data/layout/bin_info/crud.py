from common.crud import CRUDBase, Session
from utils import advanced_query_and_sort
from sqlmodel import select

from . import model
from . import schema

from ..bin_spec.model import BinSpec
from ..warehouse_area.model import WarehouseArea


class CRUDBinInfo(CRUDBase[model.BinInfo]):
    def get_by_bin_code(self, db: Session, bin_code: str):
        stmt = select(model.BinInfo).where(model.BinInfo.bin_code == bin_code)
        return db.exec(stmt).all()

    def get_bin_info_by_row_col_and_level(self, db: Session, row: int, col: int, level: int):
        stmt = select(model.BinInfo).where(
            model.BinInfo.row == row, model.BinInfo.col == col, model.BinInfo.level == level
        )
        return db.exec(stmt).all()

    def get_bins_info(self, db: Session, params: schema.Request.GetBinsInfo):

        stmt = advanced_query_and_sort(
            model.BinInfo,
            params,
            {
                "bin_spec": BinSpec,
                "warehouse_area": WarehouseArea,
            },
        )

        return db.exec(stmt).all()


crud_bin_info = CRUDBinInfo(model.BinInfo)
