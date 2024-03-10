from utils import as_advanced_query_and_sort_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from pydantic import BaseModel, Field


from ..bin_spec.model import BinSpec
from ..warehouse_area.model import WarehouseArea


class BinInfo(DataSchemaBase):
    bin_code: str
    bin_spec_name: str = Field(json_schema_extra={"table_field": BinSpec.bin_spec_name})
    warehouse_area_name: str = Field(json_schema_extra={"table_field": WarehouseArea.warehouse_area_name})
    row: int
    col: int
    level: int


class Request:
    class AddBinInfo(BaseModel):
        bin_code: str

        bin_spec_name: str

        warehouse_area_name: str
        row: int
        col: int
        level: int

    @as_advanced_query_and_sort_schema()
    class GetBinInfos(BinInfo):
        pass


class Response:
    class AddBinInfo(ResponseBase[BinInfo]):
        pass

    class GetBinInfos(ResponseBase[BinInfo]):
        pass
