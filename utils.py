from pydantic import BaseModel, create_model
from typing import Optional, Union, TypeVar, Generic, Any
from datetime import datetime
from copy import deepcopy
from enum import Enum

from sqlmodel import SQLModel, select
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel.sql.expression import Select, SelectOfScalar


def schema_optionalize(
    include: Optional[list[str]] = None,
    exclude: Optional[list[str]] = None,
):
    """Return a decorator to make model fields optional"""

    if exclude is None:
        exclude = []

    # Create the decorator
    def decorator(cls: type[BaseModel]) -> type[BaseModel]:
        new_field_definitions = {}
        fields = cls.model_fields

        if include is None:
            fields = fields.items()
        else:
            # Create iterator for specified fields
            fields = ((field_name, fields[field_name]) for field_name in include if field_name in fields)
            # Fields in 'include' that are not in the model are simply ignored, as in BaseModel.dict
        for field_name, field_info in fields:
            if field_name in exclude or not field_info.is_required:
                new_field_definitions[field_name] = (field_name, field_info)
                continue
            else:
                # # Update pydantic ModelField to not required
                assert field_info.annotation is not None
                new_field_type = Optional[field_info.annotation]
                field_info.default = None
                new_field_info = deepcopy(field_info)
                new_field_definitions[field_name] = (new_field_type, new_field_info)
        return create_model(
            f"Optional{cls.__name__}",
            __base__=cls,
            **new_field_definitions,
        )

    return decorator


class AdvanceQueryLogic(Enum):
    LESS = "<"
    LESS_OR_EQUAL = "<="
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_OR_EQUAL = ">="
    GREATER = ">"
    IN = "@"
    NOT_IN = "*"
    LIKE = "%"
    NOT_LIKE = "!%"
    LEFT_LIKE = "%_"
    RIGHT_LIKE = "_%"


class AdvancedSortOrder(Enum):
    ASCENDING = "<"
    DESCENDING = ">"


FieldValueType = TypeVar("FieldValueType")
FieldNameEnumType = TypeVar("FieldNameEnumType", bound=Enum)


class AdvanceQueryField(BaseModel, Generic[FieldValueType]):
    logic: AdvanceQueryLogic
    value: FieldValueType


class AdvancedSortField(BaseModel, Generic[FieldNameEnumType]):
    field: FieldNameEnumType
    order: AdvancedSortOrder


def as_advanced_query_and_sort_schema():
    def decorator(cls: type[BaseModel]) -> type[BaseModel]:
        new_field_definitions = {}
        fields = cls.model_fields

        # 添加高级查询字段
        for field_name, field_info in fields.items():
            assert field_info.annotation is not None
            new_field_type = Optional[AdvanceQueryField[field_info.annotation]]
            field_info.default = None
            new_field_info = deepcopy(field_info)
            new_field_definitions[field_name] = (new_field_type, new_field_info)

        # 添加高级排序字段
        sort_field_type = Optional[
            list[
                AdvancedSortField[
                    Enum("FieldNameEnum", {field_name: field_name for field_name in cls.model_fields.keys()})  # type: ignore
                ]
            ]
        ]

        new_field_definitions["sort__"] = (sort_field_type, [])

        return create_model(
            f"{cls.__name__}ForAdvanceQuery",
            __base__=cls,
            **new_field_definitions,
        )

    return decorator


def advanced_query_and_sort(model: SQLModel, params: BaseModel) -> SelectOfScalar:

    stmt: SelectOfScalar = select()

    not_none_params = params.model_dump(exclude_none=True).items()

    for model_field_name in model.model_fields.keys():
        """将主表内所有字段都加入到 select 语句中"""
        stmt = stmt.add_columns(getattr(model, model_field_name))

    for schema_field_name, schema_field_info in params.model_fields.items():

        table_field = None

        if schema_field_name not in model.model_fields.keys():
            """将不在主表内的字段添加到 select 语句中（sort__字段除外，因为其是排序条件而不是查询条件。）"""
            if schema_field_name == "sort__":
                continue

            """获取不在主表内的字段对应于主表的字段"""
            try:
                if not schema_field_info.json_schema_extra:
                    raise ValueError(f"table_field not found in 'json_schema_extra' of '{schema_field_name}'")

                table_field = schema_field_info.json_schema_extra["table_field"]

            except Exception as e:
                raise e

            stmt = stmt.add_columns(table_field)

        if schema_field_name in not_none_params:
            """将不为空的查询条件添加到 where 语句中"""
            logic = not_none_params[schema_field_name]["logic"]
            value = not_none_params[schema_field_name]["value"]

            field_for_query: InstrumentedAttribute = getattr(model, field_name, None)

            if not field_for_query:
                field_for_query: InstrumentedAttribute = table_field

            """将 where 条件添加到 select 语句中"""
            if logic == AdvanceQueryLogic.LESS:
                stmt = stmt.where(field_for_query < value)
            if logic == AdvanceQueryLogic.LESS_OR_EQUAL:
                stmt = stmt.where(field_for_query <= value)
            if logic == AdvanceQueryLogic.EQUAL:
                stmt = stmt.where(field_for_query == value)
            if logic == AdvanceQueryLogic.NOT_EQUAL:
                stmt = stmt.where(field_for_query != value)
            if logic == AdvanceQueryLogic.GREATER_OR_EQUAL:
                stmt = stmt.where(field_for_query >= value)
            if logic == AdvanceQueryLogic.GREATER:
                stmt = stmt.where(field_for_query > value)
            if logic == AdvanceQueryLogic.IN:
                stmt = stmt.where(field_for_query.in_(value.split(",")))
            if logic == AdvanceQueryLogic.NOT_IN:
                stmt = stmt.where(field_for_query.notin_(value.split(",")))
            if logic == AdvanceQueryLogic.LIKE:
                stmt = stmt.where(field_for_query.like(f"%%{value}%%"))
            if logic == AdvanceQueryLogic.NOT_LIKE:
                stmt = stmt.where(field_for_query.notlike(f"%%{value}%%"))
            if logic == AdvanceQueryLogic.LEFT_LIKE:
                stmt = stmt.where(field_for_query.like(f"%%{value}"))
            if logic == AdvanceQueryLogic.RIGHT_LIKE:
                stmt = stmt.where(field_for_query.like(f"{value}%%"))

    return stmt
