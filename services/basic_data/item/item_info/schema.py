from common.response import ResponseBase
from common.schema import SQLModel, DataSchemaBase


from . import model


class ItemInfo(SQLModel):
    item_code: str
    item_name: str
    base_unit: str


class Request:
    class AddItem(ItemInfo):
        pass

    class GetItem(DataSchemaBase, ItemInfo):
        pass


class Response:
    class AddItem(ResponseBase[model.ItemInfo]):
        pass

    class GetItems(ResponseBase[model.ItemInfo]):
        pass
