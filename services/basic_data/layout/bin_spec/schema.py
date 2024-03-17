from utils import as_advanced_query_and_sort_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page
from sqlmodel import SQLModel

from . import model


class BinSpecIdAndName(SQLModel):
    id: int
    bin_spec_name: str


class BinSpec(DataSchemaBase):
    bin_spec_name: str

    length: int
    width: int
    height: int

    weight_capacity: int
    volume_capacity: int

    pieces_capacity: int
    carton_capacity: int
    pallet_capacity: int


class Request:
    class AddBinSpec(BinSpec):
        pass

    @as_advanced_query_and_sort_schema()
    class GetBinSpecs(BinSpec):
        pass

    class GetBinSpecsIdAndName(SQLModel):
        pass


class Response:
    class AddBinSpec(ResponseBase[BinSpec]):
        pass

    class GetBinSpecs(ResponseBase[Page[BinSpec]]):
        pass

    class GetBinSpecsIdAndName(ResponseBase[list[BinSpecIdAndName]]):
        pass
