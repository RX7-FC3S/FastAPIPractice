from common.crud import CRUDBase, Session
from sqlmodel import select
from utils import advanced_query_and_sort
from . import model
from . import schema


class CRUDItem(CRUDBase[model.BinSpec]):

    def get_by_name(self, db: Session, bin_spec_name: str):
        stmt = select(model.BinSpec).where(model.BinSpec.bin_spec_name == bin_spec_name)
        return db.exec(stmt).all()

    def get_bin_specs(self, db: Session, params: schema.Request.GetBinSpecs):
        # stmt = select(model.BinSpec)
        stmt = advanced_query_and_sort(model.BinSpec, params)
        return db.exec(stmt).all()


crud_bin_spec = CRUDItem(model.BinSpec)
