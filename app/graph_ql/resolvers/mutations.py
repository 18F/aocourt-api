from ariadne import MutationType
from pydantic import parse_obj_as
from app.data import case
from app.schemas import Case

mutation = MutationType()


@mutation.field("sealCase")
def resolve_seal_case(obj, info, caseId, sealed):
    session = info.context['request'].state.db
    modified_case = case.set_sealed(session, caseId, sealed)
    if modified_case is not None:
        return parse_obj_as(Case, modified_case)


@mutation.field("createAppealCase")
def create_appeal_case(obj, info, caseId, recievingCourtId=None):
    session = info.context['request'].state.db
    original_case = case.get(session, id=caseId)
    if original_case is None:
        raise ValueError(f"Could not find case with id: {caseId}")

    modified_case = case.create_appeal_case(session, caseId, recievingCourtId)
    if modified_case is not None:
        return parse_obj_as(Case, modified_case)
