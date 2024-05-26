from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from common.model import DataModelBase


from services.basic_data.business.order_type.model import OrderType
from services.basic_data.business.stakeholder.model import Stakeholder

if TYPE_CHECKING:
    from services.inbound.receiving_list.receiving_list_detail.model import (
        ReceivingListDetail,
    )


class ReceivingListHeader(DataModelBase, table=True):

    receiving_list_number: str = Field(nullable=False, unique=True, max_length=16)
    related_order_number: Optional[str] = Field(max_length=16)

    order_type_id: int = Field(nullable=False, foreign_key="order_type.id")
    order_type: OrderType = Relationship()

    sender_id: int = Field(nullable=False, foreign_key="stakeholder.id")
    sender: Stakeholder = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[ReceivingListHeader.sender_id]",
        }
    )
    receiver_id: int = Field(nullable=False, foreign_key="stakeholder.id")
    receiver: Stakeholder = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReceivingListHeader.receiver_id]"}
    )

    receiving_list_details: list["ReceivingListDetail"] = Relationship()
