from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import re
from sqlalchemy.orm.attributes import InstrumentedAttribute


class DataModelBase(SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(self) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", self.__name__).lower()

    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: Optional[datetime] = Field(default_factory=datetime.now)
    create_by: Optional[int] = Field(default=0)
    update_at: Optional[datetime] = Field(default_factory=datetime.now)
    update_by: Optional[int] = Field(default=0)

    def link(self, schema_field_name: str, model_field: InstrumentedAttribute):
        self.model_fields[schema_field_name].json_schema_extra = {"sqlmodel_field": model_field}.__dict__
