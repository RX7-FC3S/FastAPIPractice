from common.schema import DataSchemaBase
from common.model import DataModelBase
from typing import TypeVar, Generic
from sqlmodel import Session

DataModel = TypeVar("DataModel", bound=DataModelBase)
DataSchema = TypeVar("DataSchema", bound=DataSchemaBase)


class CRUDBase(Generic[DataModel]):
    def __init__(self, model: type[DataModel]):
        self.model = model

    def add(self, db: Session, instance: DataModel) -> DataModel:
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def delete(self, db: Session, _id: int):
        db.delete(self.get(db, _id))
        db.commit()

    def get(self, db: Session, _id: int):
        return db.get(self.model, _id)
