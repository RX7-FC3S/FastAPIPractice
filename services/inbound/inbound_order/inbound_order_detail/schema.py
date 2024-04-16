from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel
from typing import Optional, TYPE_CHECKING



from . import model

if TYPE_CHECKING:
    from services.basic_data.item.item_info.schema import ItemInfo
    from ..inbound_order_header.schema import InboundOrderHeader    

class InboundOrderDetail(DataSchemaBase):
    inbound_order_header: 'InboundOrderHeader'
    seq: int
    item: 'ItemInfo'

    quantity_of_base_unit: int
    quantity_of_carton: Optional[int] = None
    quantity_of_pallet: Optional[int] = None


class Request:
    pass

class Response:
    pass
