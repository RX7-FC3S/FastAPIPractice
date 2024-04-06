from common.schema import AdvancedOrderField
from utils import advanced_query_and_order
from common.crud import CRUDBase, Session
from sqlmodel import select

from . import model
from . import schema


class CRUDXxxx(CRUDBase):
    pass

crud_item = CRUDXxxx(model.Xxxx)
