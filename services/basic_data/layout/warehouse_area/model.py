from common.model import DataModelBase
from sqlmodel import Relationship
from typing import Optional
from sqlmodel import Field


class WarehouseArea(DataModelBase, table=True):

    warehouse_area_code: str
    warehouse_area_name: str
