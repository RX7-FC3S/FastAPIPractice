from common.schema import DataSchemaBase
from common.model import DataModelBase
from typing import TypeVar, Generic
from sqlmodel import Session, update

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
        db_record = self.get(db, _id)
        if db_record is None:
            raise Exception(f"数据不存在(id:{_id})")

        db.delete(db_record)
        db.commit()
        return db_record

    def update(self, db: Session, instance: DataModel) -> DataModel:
        if instance.id is None:
            raise Exception(f"id不能为空")
        
        db_record = self.get(db, instance.id)
        
        if db_record is None:
            raise Exception(f"数据不存在(id:{instance.id})")
        
        for key in instance.model_fields:
            if key == 'create_at': continue
            setattr(db_record, key,  getattr(instance, key))

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return db_record


    def get(self, db: Session, _id: int):
        return db.get(self.model, _id)
