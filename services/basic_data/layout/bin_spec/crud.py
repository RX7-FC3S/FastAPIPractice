from common.crud import CRUDBase, Session
from utils import advanced_query_and_sort
from sqlmodel import select

from . import model
from . import schema


class CRUDBinSpec(CRUDBase[model.BinSpec]):

    def get_by_name(self, db: Session, bin_spec_name: str):
        stmt = select(model.BinSpec).where(model.BinSpec.bin_spec_name == bin_spec_name)
        return db.exec(stmt).all()

    def get_bin_specs(self, db: Session, params: schema.Request.GetBinSpecs):
        stmt = advanced_query_and_sort(model.BinSpec, params, {})
        return db.exec(stmt).all()

    def get_bin_specs_id_and_name(self, db: Session):
        return db.exec(select(model.BinSpec.id, model.BinSpec.bin_spec_name))


crud_bin_spec = CRUDBinSpec(model.BinSpec)
