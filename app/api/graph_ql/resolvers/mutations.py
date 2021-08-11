from ariadne import MutationType
from app.core.enums import CaseStatus
from app.data import case, record_on_appeal
from app.entities import AppellateCase, Court

mutation = MutationType()


@mutation.field("sealCase")
def resolve_seal_case(obj, info, caseId, sealed):
    session = info.context['request'].state.db
    original_case = case.get(session, id=caseId)
    if original_case is None:
        return
    original_case.seal(sealed)
    case.add(session, original_case)
    session.commit()
    return original_case


@mutation.field("createAppealCase")
def create_appeal_case(obj, info, caseId, recievingCourtId=None):
    session = info.context['request'].state.db
    original_case = case.get(session, id=caseId)
    if original_case is None:
        raise ValueError(f"Could not find case with id: {caseId}")

    modified_case = AppellateCase.from_district_case(original_case)

    if modified_case is not None:
        original_case.status = CaseStatus.on_appeal
        case.add(session, original_case)
        case.add(session, modified_case)
        session.commit()
        return modified_case


@mutation.field("createRecordOnAppeal")
def create_roa(obj, info, caseId):
    session = info.context['request'].state.db
    original_case = case.get(session, id=caseId)
    if original_case is None:
        raise ValueError(f"Could not find case with id: {caseId}")

    roa = original_case.create_record_on_appeal()

    if roa is not None:
        case.add(session, original_case)
        record_on_appeal.add(session, roa)
        session.commit()
        return roa


@mutation.field("sendRecordOnAppeal")
def send_roa(obj, info, recordOnAppealId, receivingCourtId):
    session = info.context['request'].state.db
    roa = record_on_appeal.get(session, id=recordOnAppealId)
    if roa is None:
        raise ValueError(f"Could not find record on appeal with id: {recordOnAppealId}")
    receivingCourt = Court.from_id(receivingCourtId)
    if receivingCourt is None:
        raise ValueError(f"Could not find court with id: {receivingCourtId}")
    roa.send_to_court(receivingCourt)
    record_on_appeal.add(session, roa)
    session.commit()
    return roa
