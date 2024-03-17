from utils import as_advanced_query_and_sort_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel


from ..bin_spec.schema import BinSpec
from ..warehouse_area.schema import WarehouseArea


class BinSpecInBinInfo(BinSpec.select(include=["bin_spec_name"])):
    pass


class WarehouseAreaInBinInfo(WarehouseArea.select(include=["warehouse_area_name"])):
    pass


class BinInfo(DataSchemaBase):
    bin_code: str
    bin_spec: BinSpecInBinInfo
    warehouse_area: WarehouseAreaInBinInfo
    row: int
    col: int
    level: int


class Request:
    class AddBinInfo(SQLModel):
        bin_code: str
        bin_spec_id: int
        warehouse_area_id: int
        row: int
        col: int
        level: int

    class DeleteBinInfo(SQLModel):
        id: int

    @as_advanced_query_and_sort_schema()
    class GetBinsInfo(BinInfo):
        pass


class Response:
    class AddBinInfo(ResponseBase[BinInfo]):
        pass

    class DeleteBinInfo(ResponseBase[BinInfo]):
        pass

    class GetBinsInfo(ResponseBase[Page[BinInfo]]):
        pass
