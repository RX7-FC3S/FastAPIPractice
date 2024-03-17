from common.model import DataModelBase
from sqlmodel import Relationship
from typing import Optional
from sqlmodel import Field

from ..bin_spec.model import BinSpec
from ..warehouse_area.model import WarehouseArea


class BinInfo(DataModelBase, table=True):
    bin_code: str = Field()

    bin_spec_id: int = Field(foreign_key="bin_spec.id")
    bin_spec: BinSpec = Relationship(back_populates="bin_list")

    warehouse_area_id: int = Field(foreign_key="warehouse_area.id")
    warehouse_area: WarehouseArea = Relationship()

    row: int = Field()
    col: int = Field()
    level: int = Field()
