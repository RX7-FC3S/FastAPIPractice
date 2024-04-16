from common.model import DataModelBase, Field
from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship

if TYPE_CHECKING:
    from services.inbound.inbound_order.inbound_order_header.model import InboundOrderHeader
    from services.basic_data.item.item_info.model import ItemInfo

class InboundOrderDetail(DataModelBase, table=True):
    inbound_order_header_id: int = Field(
        nullable=False, foreign_key="inbound_order_header.id"
    )
    inbound_order_header: 'InboundOrderHeader' = Relationship(
        back_populates="order_details"
    )
    seq: int = Field(nullable=False)

    item_id: int = Field(nullable=False, foreign_key="item_info.id")
    item: 'ItemInfo' = Relationship()

    quantity_of_base_unit: int = Field(nullable=False)
    quantity_of_carton: Optional[int] = None
    quantity_of_pallet: Optional[int] = None