from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from common.model import DataModelBase

if TYPE_CHECKING:
    from services.inbound.inbound_order.inbound_order_header.model import InboundOrderHeader
    from services.basic_data.item.item_info.model import ItemInfo


class InboundOrderDetail(DataModelBase, table=True):
    inbound_order_header_id: int = Field(nullable=False, foreign_key="inbound_order_header.id")
    inbound_order_header: "InboundOrderHeader" = Relationship(back_populates="inbound_order_details")
    
    seq: int = Field(nullable=False)

    item_id: int = Field(nullable=False, foreign_key="item_info.id")
    item: "ItemInfo" = Relationship()

    quantity_of_pieces: int = Field(nullable=False)
    quantity_of_carton: Optional[int] = None
    quantity_of_pallet: Optional[int] = None

    pallet_number: Optional[str] = None
    carton_number: Optional[str] = None
