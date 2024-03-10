from common.model import DataModelBase, Field


class WarehouseArea(DataModelBase, table=True):

    warehouse_area_code: str = Field()
    warehouse_area_name: str = Field()
