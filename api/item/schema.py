from common.response import ResponseBase
from pydantic import BaseModel

from . import model


class Item(BaseModel):
    item_code: str
    item_name: str
    base_unit: str


class Request(object):
    class AddItem(Item):
        pass


class Response:
    class AddItem(ResponseBase[model.Item]):
        pass
