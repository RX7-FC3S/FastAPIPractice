from pydantic import BaseModel
from datetime import datetime


class DataSchemaBase(BaseModel):
    id: int
    create_at: datetime
    create_by: int
    update_at: datetime
    update_by: int
