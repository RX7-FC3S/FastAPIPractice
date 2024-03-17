from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Optional, TypeVar, Generic, Callable
from sqlmodel.sql.expression import SelectOfScalar
from pydantic import BaseModel, create_model
from sqlmodel import SQLModel, select
from sqlmodel.main import FieldInfo, SQLModelMetaclass
from pydantic import BaseModel
from datetime import datetime
from copy import deepcopy
from enum import Enum


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


class AdvancedQueryLogic(Enum):
    LESS = "<"
    LESS_OR_EQUAL = "<="
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_OR_EQUAL = ">="
    GREATER = ">"
    IN = "@"
    NOT_IN = "!@"
    LIKE = "%"
    NOT_LIKE = "!%"
    LEFT_LIKE = "%_"
    RIGHT_LIKE = "_%"
    IS_NULL = "_"
    NOT_NULL = "!_"


class AdvancedSortOrder(Enum):
    ASCENDING = "<"
    DESCENDING = ">"


FieldValueType = TypeVar("FieldValueType")
FieldNameEnumType = TypeVar("FieldNameEnumType", bound=Enum)


class AdvancedQueryField(BaseModel, Generic[FieldValueType]):
    logic: AdvancedQueryLogic
    value: FieldValueType


class AdvancedSortField(BaseModel, Generic[FieldNameEnumType]):
    field: FieldNameEnumType
    order: AdvancedSortOrder


def get_deepest_field_type(field_info) -> str:
    field_type = field_info["schema"]["type"]
    if field_type in ["default", "nullable"]:
        field_type = get_deepest_field_type(field_info["schema"])
    return field_type


def create_advanced_query_and_sort_model(cls: type[SQLModel]) -> SQLModel:
    """
    this is used in the decorate function as_advanced_query_and_sort_schema to recurse the cls and make its fields be optional
    if KeyError: '__qualname__' occurs, see https://github.com/pydantic/pydantic/issues/8633
    """
    new_definition = {}
    model_fields = cls.__pydantic_core_schema__["schema"]["fields"]  # type: ignore
    for field_name, field_info in model_fields.items():  # type: ignore
        field_type = field_info["schema"]["type"]
        if field_type == "model":
            new_definition[field_name] = (
                Optional[create_advanced_query_and_sort_model(field_info["schema"]["cls"])],  # type: ignore
                FieldInfo(default=None),
            )
        else:
            new_definition[field_name] = (
                Optional[AdvancedQueryField[eval(get_deepest_field_type(field_info))]],
                FieldInfo(default=None),
            )
    return create_model(f"{cls.__name__}Optional", __base__=cls, **new_definition)


def as_advanced_query_and_sort_schema() -> Callable[[type[SQLModel]], SQLModel]:
    def wrapper(cls: type[SQLModel]) -> SQLModel:
        return create_advanced_query_and_sort_model(cls)

    return wrapper


def advanced_query_and_sort(
    master_model: SQLModelMetaclass, params: SQLModel, mappings: dict[str, SQLModelMetaclass] | None = None
) -> SelectOfScalar:
    stmt: SelectOfScalar = select(master_model)

    if mappings is not None:
        for _, join_model in mappings.items():
            stmt = stmt.join(join_model)
    else:
        pass

    def add_where_clause(params: dict, model: SQLModelMetaclass = master_model):
        nonlocal stmt

        for k, v in params.items():
            if "logic" not in v and "value" not in v:
                """不包含 logic 和 value 的 value 需要继续遍历"""
                if mappings is None or mappings[k] is None:
                    raise KeyError(f"'{k}' is not in mappings")
                else:
                    add_where_clause(v, mappings[k])

            else:
                field: InstrumentedAttribute = getattr(model, k)
                logic = v["logic"]
                value = v["value"]

                """将 where 条件添加到 select 语句中"""
                if logic == AdvancedQueryLogic.LESS:
                    stmt = stmt.where(field < value)
                if logic == AdvancedQueryLogic.LESS_OR_EQUAL:
                    stmt = stmt.where(field <= value)
                if logic == AdvancedQueryLogic.EQUAL:
                    stmt = stmt.where(field == value)
                if logic == AdvancedQueryLogic.NOT_EQUAL:
                    stmt = stmt.where(field != value)
                if logic == AdvancedQueryLogic.GREATER_OR_EQUAL:
                    stmt = stmt.where(field >= value)
                if logic == AdvancedQueryLogic.GREATER:
                    stmt = stmt.where(field > value)
                if logic == AdvancedQueryLogic.IN:
                    stmt = stmt.where(field.in_(value.split(",")))
                if logic == AdvancedQueryLogic.NOT_IN:
                    stmt = stmt.where(field.notin_(value.split(",")))
                if logic == AdvancedQueryLogic.LIKE:
                    stmt = stmt.where(field.like(f"%%{value}%%"))
                if logic == AdvancedQueryLogic.NOT_LIKE:
                    stmt = stmt.where(field.notlike(f"%%{value}%%"))
                if logic == AdvancedQueryLogic.LEFT_LIKE:
                    stmt = stmt.where(field.like(f"%%{value}"))
                if logic == AdvancedQueryLogic.RIGHT_LIKE:
                    stmt = stmt.where(field.like(f"{value}%%"))
                if logic == AdvancedQueryLogic.IS_NULL:
                    stmt = stmt.where(field == None)
                if logic == AdvancedQueryLogic.NOT_NULL:
                    stmt = stmt.where(field != None)
                else:
                    pass

    add_where_clause(params.model_dump(exclude_none=True))
    return stmt
