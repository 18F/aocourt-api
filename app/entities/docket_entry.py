import datetime
from dataclasses import dataclass, replace

from .case_entity import CaseEntity


@dataclass
class DocketEntry(CaseEntity):
    case_id: int
    sequence_no: int
    text: str
    date_filed: datetime.datetime
    entry_type: str
    sealed: bool = False

    def copy(self):
        return replace(self)
