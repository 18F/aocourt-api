import datetime
from dataclasses import dataclass, replace, field


@dataclass
class DocketEntry:
    id: int = field(init=False)
    case_id: int
    sequence_no: int
    text: str
    date_filed: datetime.datetime
    entry_type: str
    created_at: datetime.datetime = field(init=False)
    updated_on: datetime.datetime = field(init=False)
    sealed: bool = False

    def copy(self):
        return replace(self)
