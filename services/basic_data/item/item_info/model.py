from common.model import DataModelBase, Field


class ItemInfo(DataModelBase, table=True):

    item_code: str = Field()
    item_name: str = Field()
    base_unit: str = Field()
