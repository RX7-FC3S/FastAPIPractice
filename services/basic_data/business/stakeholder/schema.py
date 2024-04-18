from utils import as_advanced_query_and_order_schema
from common.response import ResponseBase
from common.schema import DataSchemaBase
from fastapi_pagination import Page


from enum import Enum


class Stakeholder(DataSchemaBase):
    stakeholder_code: str
    stakeholder_name: str
    company: str
    contact: str
    phone: str
    email: str
    address: str
    country: str

    is_sender: bool
    is_receiver: bool



class Request:
    class AddStakeholder(Stakeholder):
        pass
    @as_advanced_query_and_order_schema()
    class GetStakeholders(Stakeholder):
        pass
class Response:
    class AddStakeholder(ResponseBase[Stakeholder]):
        pass
    class GetStakeholders(ResponseBase[Page[Stakeholder]]):
        pass

