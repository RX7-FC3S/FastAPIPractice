from common.model import DataModelBase, Field
from sqlmodel import Relationship
from typing import Optional

from services.basic_data.business.order_type.model import OrderType
from services.basic_data.business.stakeholder.model import Stakeholder


class InboundOrderHeader(DataModelBase, table=True):

    inbound_order_number: str = Field(nullable=False, unique=True, max_length=16)
    related_order_number: Optional[str] = Field(max_length=16)

    order_type_id: int = Field(nullable=False, foreign_key="order_type.id")
    order_type: OrderType = Relationship()

    sender_id: int = Field(nullable=False, foreign_key="stakeholder.id")
    sender: Stakeholder = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': '[InboundOrderHeader.sender_id]',
        }
    )
    receiver_id: int = Field(nullable=False, foreign_key="stakeholder.id")
    receiver: Stakeholder = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': '[InboundOrderHeader.receiver_id]'
        }
    )
