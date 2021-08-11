from datetime import date
from typing import List, Optional
from dataclasses import dataclass, field

from .case_entity import CaseEntity
from .docket_entry import DocketEntry
from .court import Court


@dataclass
class RecordOnAppealDocketEntry(DocketEntry):
    recieving_court: Optional[str] = None
    include_with_appeal: bool = True

    @classmethod
    def from_docket_entry(cls, docket_entry):
        fields = ['case_id', 'court', 'sequence_no', 'text', 'date_filed', 'entry_type', 'sealed']
        return cls(**dict([(field, getattr(docket_entry, field)) for field in fields]))


@dataclass
class RecordOnAppeal(CaseEntity):
    title: str
    original_case_id: int
    receiving_court: Optional[str]
    date_filed: date
    status: Optional[str]
    docket_entries: List[RecordOnAppealDocketEntry] = field(default_factory=list)
    sealed: bool = False

    def send_to_court(self, court: Court):
        self.receiving_court = court.id
