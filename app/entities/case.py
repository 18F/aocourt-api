import datetime
from typing import List, Literal, Union, Optional, TypeVar
from dataclasses import dataclass, field

from .docket_entry import DocketEntry
from app.core.enums import CourtType, CaseStatus
from .court import Court
from app.core.courts import courts

T = TypeVar('T', bound='Case')


@dataclass
class Case():
    id: int = field(init=False)
    title: str
    court: str
    date_filed: datetime.date
    status: Optional[str]
    created_at: datetime.datetime = field(init=False)
    updated_on: datetime.datetime = field(init=False)

    def seal(self: T, sealed: bool) -> T:
        self.sealed = sealed
        return self


@dataclass
class DistrictCase(Case):
    docket_entries: List[DocketEntry] = field(default_factory=list)
    type: Literal[CourtType.district] = field(init=False, default=CourtType.district)
    sealed: bool = False

    def validate_appeal(self, court: Court) -> None:
        if self.status == CaseStatus.on_appeal:
            raise ValueError(f"Case {self.id} has already been sent to appellate")
        if court.type != CourtType.appellate:
            raise ValueError(f"Can not appeal to {court.full_name}")


@dataclass
class BankruptcyCase(Case):
    docket_entries: List[DocketEntry] = field(default_factory=list)
    type: Literal[CourtType.bankruptcy] = field(init=False, default=CourtType.bankruptcy)
    sealed: bool = False

    def validate_appeal(self, court: Court) -> None:
        pass


@dataclass
class AppellateCase(Case):
    original_case_id: int
    docket_entries: List[DocketEntry] = field(default_factory=list)
    type: Literal[CourtType.appellate] = field(init=False, default=CourtType.appellate)
    sealed: bool = False
    reviewed: bool = False
    remanded: bool = False

    def validate_appeal(self, court: Court) -> None:
        pass

    @classmethod
    def from_district_case(cls, district_case, receiving_court_id: Optional[str] = None):
        '''Create a new appellate case from a district case'''
        if receiving_court_id is None:
            court_id = courts[district_case.court]['parent']
            receiving_court = Court(id=court_id, **courts[court_id])
        else:
            receiving_court = Court(id=receiving_court_id, **courts[receiving_court_id])

        district_case.validate_appeal(receiving_court)

        appellate_case = cls(
            original_case_id=district_case.id,
            docket_entries=[d.copy() for d in district_case.docket_entries],
            title=district_case.title,
            status=CaseStatus.submitted_for_appeal,
            court=receiving_court.id,
            sealed=district_case.sealed,
            date_filed=datetime.datetime.now(),

        )
        return appellate_case


CaseType = Union[DistrictCase, AppellateCase, BankruptcyCase]
