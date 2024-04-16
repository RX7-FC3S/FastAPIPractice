from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page


class OrderType(DataSchemaBase):
    order_type_code: str
    order_type_name: str
    business_type: int


class Request:
    class AddOrderType(OrderType):
        pass

    @as_advanced_query_and_order_schema()
    class GetOrderTypes(OrderType):
        pass


class Response:
    class AddOrderType(ResponseBase[OrderType]):
        pass

    class GetOrderTypes(ResponseBase[Page[OrderType]]):
        pass
