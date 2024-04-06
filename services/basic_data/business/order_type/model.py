from common.model import DataModelBase, Field


class OrderType(DataModelBase, table=True):
    order_type_code: str = Field() 
    order_type_name: str = Field()
    business_type: int = Field() # inbound=1, outbound=2

