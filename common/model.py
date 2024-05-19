from sqlmodel import SQLModel, Field, TIMESTAMP, text
from sqlalchemy.orm import declared_attr
from utils import datetime_now
from datetime import datetime
from typing import Optional
import re


class DataModelBase(SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(self) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", self.__name__).lower()

    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: Optional[datetime] = Field(
        default=None, sa_type=TIMESTAMP(timezone=True), sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    create_by: Optional[int] = Field(default=0)
    update_at: Optional[datetime] = Field(default_factory=datetime_now)
    update_by: Optional[int] = Field(default=0)
