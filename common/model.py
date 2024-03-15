from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import re


class DataModelBase(SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(self) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", self.__name__).lower()

    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: Optional[datetime] = Field(default_factory=datetime.now)
    create_by: Optional[int] = Field(default=0)
    update_at: Optional[datetime] = Field(default_factory=datetime.now)
    update_by: Optional[int] = Field(default=0)
