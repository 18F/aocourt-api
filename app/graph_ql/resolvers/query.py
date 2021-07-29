from typing import Any, Optional
from ariadne import QueryType
from ariadne.types import GraphQLResolveInfo
from pydantic import parse_obj_as
from app.data_service import case
from app.schemas import Case, Court
from app.core.courts import courts


query = QueryType()


@query.field("case")
def resolve_case(obj: Any, info: GraphQLResolveInfo, id) -> Optional[Case]:
    session = info.context['request'].state.db
    case_data = case.get(session, id)
    if case_data:
        return parse_obj_as(Case, case_data)


@query.field("court")
def resolve_court(obj: Any, info: GraphQLResolveInfo, id) -> Optional[Court]:
    court = courts.get(id)
    if court:
        court['id'] = id
        return Court(**court)
