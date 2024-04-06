from fastapi_pagination import Params as PaginationParams, paginate
from common.schema import AdvancedOrderField
from database import Session, create_session
from fastapi import APIRouter, Depends
from common.response import Response

from . import schema
from . import model
from . import crud


router = APIRouter()


@router.post("/get_stakeholders", response_model=schema.Response.GetStakeholders)
def get_stakeholders(
    query_params: schema.Request.GetStakeholders,
    order_params: list[AdvancedOrderField],
    pagination_params: PaginationParams,
    db: Session = Depends(create_session),
):
    try:
        return Response(
            True,
            "",
            paginate(
                crud.crud_stakeholder.get_stakeholders(db, query_params, order_params),
                pagination_params,
            ),
        )
    except Exception as e:
        return Response(False, str(e), None)
