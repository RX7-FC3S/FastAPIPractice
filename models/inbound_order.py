from common.model import DataModelBase, Field


class InboundOrderHeader(DataModelBase, table=True):
    inbound_order_number: int = Field()
    sender_id: int = Field()
    receiver_id: int = Field()

