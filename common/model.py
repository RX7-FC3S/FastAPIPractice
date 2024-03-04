from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class DataModelBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    create_at: Optional[datetime] = Field(default_factory=datetime.now)
    create_by: Optional[int] = Field(default=0)
    update_at: Optional[datetime] = Field(default_factory=datetime.now)
    update_by: Optional[int] = Field(default=0)
