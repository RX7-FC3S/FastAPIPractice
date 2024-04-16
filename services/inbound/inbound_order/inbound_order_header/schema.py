from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page


from . import model
from services.basic_data.business.order_type.schema import OrderType
from services.basic_data.business.stakeholder.schema import Stakeholder


class OrderType(OrderType.select(include=["order_type_name"])):
    pass


class Sender(Stakeholder.select(include=["stakeholder_name", "contact", "phone"])):
    pass


class Receiver(Stakeholder.select(include=["stakeholder_name", "contact", "phone"])):
    pass


class InboundOrderHeader(DataSchemaBase):
    inbound_order_number: str
    related_order_number: str
    order_type: OrderType
    sender: Sender
    receiver: Receiver


class Request:
    class AddInboundOrderHeader(InboundOrderHeader):
        pass

    @as_advanced_query_and_order_schema()
    class GetInboundOrderHeaders(InboundOrderHeader):
        pass


class Response:
    class AddInboundOrderHeader(ResponseBase[InboundOrderHeader]):
        pass

    class GetInboundOrderHeaders(ResponseBase[Page[InboundOrderHeader]]):
        pass
