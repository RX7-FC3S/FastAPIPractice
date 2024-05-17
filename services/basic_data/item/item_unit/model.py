from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from common.model import DataModelBase

if TYPE_CHECKING:
    from services.basic_data.item.item_info.model import ItemInfo


class ItemUint(DataModelBase, table=True):
    item_id: int = Field(foreign_key="item_info.id")
    item: "ItemInfo" = Relationship(back_populates='item_units')

    unit_type: int  # pcs = 0, ctn = 1, plt = 2
    unit_name: str
    
    conversion_quantity: int