from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDBinSpec(CRUDBase[model.BinSpec]):

    def get_by_name(self, db: Session, bin_spec_name: str):
        stmt = select(model.BinSpec).where(model.BinSpec.bin_spec_name == bin_spec_name)
        return db.exec(stmt).all()

    def get_bin_specs(
        self,
        db: Session,
        query_params: schema.Request.GetBinSpecs,
        order_params: list[AdvancedOrderField],
    ):
        stmt = advanced_query_and_order(model.BinSpec, query_params, order_params)
        return db.exec(stmt).all()

    def get_bin_specs_id_and_name(self, db: Session):
        return db.exec(select(model.BinSpec.id, model.BinSpec.bin_spec_name))


crud_bin_spec = CRUDBinSpec(model.BinSpec)
