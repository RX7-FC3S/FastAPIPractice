from utils import as_advanced_query_and_sort_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model


class WarehouseAreaIdAndName(SQLModel):
    id: int
    warehouse_area_name: str


class WarehouseArea(DataSchemaBase):
    warehouse_area_code: str
    warehouse_area_name: str


class Request:
    class AddWarehouseArea(SQLModel):
        pass

    @as_advanced_query_and_sort_schema()
    class GetWarehouseAreas(WarehouseArea):
        pass

    class GetWarehouseAreasIdAndName(SQLModel):
        pass


class Response:
    class AddWarehouseArea(ResponseBase[model.WarehouseArea]):
        pass

    class GetWarehouseAreas(ResponseBase[Page[model.WarehouseArea]]):
        pass

    class GetWarehouseAreasIdAndName(ResponseBase[list[WarehouseAreaIdAndName]]):
        pass
