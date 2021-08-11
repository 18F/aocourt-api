from typing import List, Optional

from ariadne import ObjectType
from app.entities import RecordOnAppeal, RecordOnAppealDocketEntry, Court


record_on_appeal = ObjectType("RecordOnAppeal")
record_on_appeal_docket_entry = ObjectType("RecordOnAppealDocketEntry")
record_on_appeal_docket_entry.set_alias("sequenceNumber", "sequence_no")


@record_on_appeal.field("docketEntries")
def resolve_docket_entries(obj: RecordOnAppeal, *_) -> List[RecordOnAppealDocketEntry]:
    return obj.docket_entries


@record_on_appeal.field("court")
def resolve_court(obj: RecordOnAppeal, *_) -> Optional[Court]:
    if obj.court:
        return Court.from_id(obj.court)


@record_on_appeal.field("receivingCourt")
def resolve_receivingCourt(obj: RecordOnAppeal, *_) -> Optional[Court]:
    if obj.receiving_court:
        return Court.from_id(obj.receiving_court)
