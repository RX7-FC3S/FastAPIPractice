from pydantic import create_model
from sqlmodel import SQLModel
from datetime import datetime


class DataSchemaBase(SQLModel):
    id: int
    create_at: datetime
    create_by: int
    update_at: datetime
    update_by: int

    @classmethod
    def select(cls, include: list[str] | None = None, exclude: list[str] | None = None) -> type[SQLModel]:
        new_definition = {}

        if not include:
            include = []
        if not exclude:
            exclude = []

        for field_name, field_info in cls.model_fields.items():
            if include and exclude:
                if field_name in include and field_name in exclude:
                    raise ValueError("field could not be included and excluded")
                elif field_name in include and field_name not in exclude:
                    new_definition[field_name] = (field_info.annotation, field_info)
                elif field_name in exclude and field_name not in include:
                    pass
                else:
                    new_definition[field_name] = (field_info.annotation, field_info)
            elif include and not exclude:
                if field_name in include:
                    new_definition[field_name] = (field_info.annotation, field_info)
                else:
                    pass
            elif not include and exclude:
                if field_name in exclude:
                    pass
                else:
                    new_definition[field_name] = (field_info.annotation, field_info)
            else:
                new_definition[field_name] = (field_info.annotation, field_info)

        return create_model(f"{cls.__name__}Selected", __base__=SQLModel, **new_definition)
