from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from common.model import DataModelBase

if TYPE_CHECKING:
    from services.inbound.receiving_list.receiving_list_header.model import ReceivingListHeader
    from services.basic_data.item.item_info.model import ItemInfo
    from services.basic_data.item.item_unit.model import ItemUnit


class ReceivingListDetail(DataModelBase, table=True):
    receiving_list_header_id: int = Field(nullable=False, foreign_key="receiving_list_header.id")
    receiving_list_header: "ReceivingListHeader" = Relationship(back_populates="receiving_list_details")
    
    seq: int = Field(nullable=False)

    item_info_id: int = Field(nullable=False, foreign_key="item_info.id")
    item_info: "ItemInfo" = Relationship()

    item_unit_id: int = Field(nullable=False, foreign_key="item_unit.id")
    item_unit: "ItemUnit" = Relationship()

    quantity: int = Field(nullable=False)