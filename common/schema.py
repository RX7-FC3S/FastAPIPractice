from sqlmodel import SQLModel
from datetime import datetime


class DataSchemaBase(SQLModel):
    id: int
    create_at: datetime
    create_by: int
    update_at: datetime
    update_by: int
