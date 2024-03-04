from common.model import DataModelBase
from database import create_session
from typing import TypeVar, Generic
from sqlmodel import update

DataModel = TypeVar("DataModel", bound=DataModelBase)


class CRUDBase(Generic[DataModel]):
    def __init__(self, model: type[DataModel]):
        self.model = model

    def add(self, instance: DataModel):
        db = next(create_session())
        db.add(self.model.model_validate(instance))
        db.commit()

    def delete(self, _id: int):
        db = next(create_session())
        db.delete(self.get(_id))
        db.commit()

    def get(self, _id: int):
        db = next(create_session())
        return db.get(self.model, _id)
