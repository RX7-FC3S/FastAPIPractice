from common.model import DataModelBase, Field
from sqlmodel import Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.basic_data.item.item_unit.model import ItemUnit

class ItemInfo(DataModelBase, table=True):
    item_code: str = Field()
    item_name: str = Field()

    item_units: list['ItemUnit'] = Relationship()