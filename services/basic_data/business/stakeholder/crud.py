from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDStakeholder(CRUDBase[model.Stakeholder]):
    def get_stakeholders(self, db:Session,query_params: schema.Request.GetStakeholders, order_params: list[AdvancedOrderField]):
        stmt = advanced_query_and_order(model.Stakeholder, query_params, order_params)
        return db.exec(stmt).all()

crud_stakeholder = CRUDStakeholder(model.Stakeholder)
