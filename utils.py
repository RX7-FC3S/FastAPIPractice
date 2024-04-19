from common.schema import (
    AdvancedQueryLogic,
    AdvancedQueryField,
    AdvancedOrderField,
    OrderDirection,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlmodel.main import FieldInfo, SQLModelMetaclass
from pydantic import BaseModel, create_model
from typing import Optional, Callable, Any, overload
from sqlmodel import SQLModel, select
from pydantic import BaseModel
from datetime import datetime


def get_deepest_field_type(field_info) -> str:
    field_type = field_info["schema"]["type"]
    if field_type in ["default", "nullable"]:
        field_type = get_deepest_field_type(field_info["schema"])
    return field_type


def create_advanced_query_and_order_model(cls: type[BaseModel]):
    """
    this is used in the decorate function as_advanced_query_and_order_schema to recurse the cls and make its fields be optional
    if KeyError: '__qualname__' occurs, see https://github.com/pydantic/pydantic/issues/8633
    """

    new_definition: dict[str, tuple[Optional[Any], FieldInfo]] = {}

    model_fields: dict[str, dict] = cls.__pydantic_core_schema__["schema"]["fields"]  # type: ignore

    for field_name, field_info in model_fields.items():
        field_type = field_info["schema"]["type"]
        if field_type == "model":
            new_definition[field_name] = (
                Optional[
                    create_advanced_query_and_order_model(field_info["schema"]["cls"])
                ],
                FieldInfo(default=None),
            )
        else:
            new_definition[field_name] = (
                (
                    Optional[
                        AdvancedQueryField[eval(get_deepest_field_type(field_info))]
                    ]
                    if field_info["schema"]["type"]
                    in ["str", "int", "float", "bool", "datetime"]
                    else field_info["schema"]["strict_schema"]["python_schema"]["cls"]
                ),
                FieldInfo(default=None),
            )
    return create_model(f"{cls.__name__}ForQuery", __base__=None, **new_definition)  # type: ignore


def as_advanced_query_and_order_schema() -> Callable[[type[SQLModel]], SQLModel]:
    def wrapper(cls: type[SQLModel]) -> SQLModel:
        return create_advanced_query_and_order_model(cls)

    return wrapper


def advanced_query_and_order(
    master_model: SQLModelMetaclass,
    query_params: SQLModel,
    order_params: list[AdvancedOrderField],
    statement: Select | SelectOfScalar | None = None,
    mappings: dict[str, SQLModelMetaclass] | None = None,
) -> Select | SelectOfScalar:
    if statement is None:
        stmt: Select | SelectOfScalar = select(master_model)
    else:
        stmt = statement

    if mappings is not None:
        for _, join_model in mappings.items():
            stmt = stmt.join(join_model)
    else:
        pass

    def add_where_clause(params: dict, model: SQLModelMetaclass = master_model):
        nonlocal stmt

        for k, v in params.items():
            if "logic" not in v and "value" not in v:
                # 如果 v 中没有 logic 和 value 则需要再次遍历
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

    add_where_clause(query_params.model_dump(exclude_none=True))

    for order_condition in order_params:

        model_field: InstrumentedAttribute

        if "." not in order_condition.field:
            model_field = getattr(master_model, order_condition.field)
        else:
            model_name, field_name = order_condition.field.split(".")
            if mappings is None or mappings[model_name] is None:
                raise KeyError(f"'{model_name}' is not in mappings")
            else:
                model_field = getattr(mappings[model_name], field_name)

        if order_condition.order == OrderDirection.ASCENDING:
            stmt = stmt.order_by(model_field)
        else:
            stmt = stmt.order_by(model_field.desc())

    return stmt
