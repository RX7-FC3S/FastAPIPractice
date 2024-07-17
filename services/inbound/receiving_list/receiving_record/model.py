from common.model import DataModelBase
from sqlmodel import Field, Relationship
from services.inbound.receiving_list.receiving_list_detail.model import (
    ReceivingListDetail,
)
from typing import Optional


class ReceivingRecord(DataModelBase, table=True):
    receiving_list_detail_id: int = Field(
        nullable=False, foreign_key="receiving_list_detail.id"
    )
    receiving_list_detail: "ReceivingListDetail" = Relationship()

    receiving_quantity: int = Field(nullable=False)
    remark: Optional[str] = Field(nullable=True, default=None)
