from typing import List, Optional, Union

from ariadne import ObjectType, InterfaceType
from app.entities import DocketEntry, Case, DistrictCase, AppellateCase, Court
from app.core.courts import courts

case = InterfaceType("Case")
docketentry = ObjectType("DocketEntry")
docketentry.set_alias("sequenceNumber", "sequence_no")


@case.type_resolver
def case_result_type(obj, *_):
    if isinstance(obj, DistrictCase):
        return "DistrictCase"
    if isinstance(obj, AppellateCase):
        return "AppellateCase"


@case.field("docketEntries")
def resolve_docket_entries(obj: Union[DistrictCase, AppellateCase], *_) -> List[DocketEntry]:
    # at the moment the data query grabs the whole docket, so this is convenient
    # this will probably change
    return obj.docket_entries


@case.field("court")
def resolve_court(obj: Case, *_) -> Optional[Court]:
    if obj.court:
        court = courts[obj.court]
        return Court(**court, id=obj.court)
