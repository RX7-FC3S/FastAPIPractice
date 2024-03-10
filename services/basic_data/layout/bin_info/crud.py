from common.crud import CRUDBase, Session
from sqlmodel import select
from utils import advanced_query_and_sort

from . import model
from . import schema

from ..bin_spec.model import BinSpec
from ..warehouse_area.model import WarehouseArea


class CRUDBinInfo(CRUDBase[model.BinInfo]):
    def get_bin_infos(self, db: Session, params: schema.Request.GetBinInfos):
        stmt = advanced_query_and_sort(model.BinInfo, params)
        return db.exec(stmt)


crud_bin_info = CRUDBinInfo(model.BinInfo)
