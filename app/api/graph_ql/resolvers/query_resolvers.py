from typing import Any, Optional
from ariadne import QueryType
from ariadne.types import GraphQLResolveInfo

from app.data import case, record_on_appeal
from app.entities import Case, Court, RecordOnAppeal, User


query = QueryType()


@query.field("case")
def resolve_case(obj: Any, info: GraphQLResolveInfo, id) -> Optional[Case]:
    session = info.context['request'].state.db
    case_data = case.get(session, id)
    if case_data:
        return case_data


@query.field("recordOnAppeal")
def resolve_roa(obj: Any, info: GraphQLResolveInfo, id) -> Optional[RecordOnAppeal]:
    session = info.context['request'].state.db
    roa_data = record_on_appeal.get(session, id)
    if roa_data:
        return roa_data


@query.field("court")
def resolve_court(obj: Any, info: GraphQLResolveInfo, id) -> Optional[Court]:
    return Court.from_id(id)


@query.field("currentuser")
def resolve_current_user(obj: Any, info: GraphQLResolveInfo) -> Optional[User]:
    user = info.context['request'].state.user
    if user:
        return user
