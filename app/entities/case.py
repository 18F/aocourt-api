import datetime
from typing import List, Literal, Union, Optional, TypeVar
from dataclasses import dataclass, field

from .docket_entry import DocketEntry
from app.core.enums import CourtType, CaseStatus
from .court import Court
from .case_entity import CaseEntity
from .record_on_appeal import RecordOnAppeal, RecordOnAppealDocketEntry

T = TypeVar('T', bound='Case')


@dataclass
class Case(CaseEntity):
    title: str
    date_filed: datetime.date
    status: Optional[str]

    def seal(self: T, sealed: bool) -> T:
        self.sealed = sealed
        return self

    def create_record_on_appeal(self, receiving_court: Optional[Court] = None):
        pass


@dataclass
class DistrictCase(Case):
    docket_entries: List[DocketEntry] = field(default_factory=list)
    type: Literal[CourtType.district] = field(init=False, default=CourtType.district)
    sealed: bool = False

    def create_record_on_appeal(self, receiving_court: Optional[Court] = None) -> RecordOnAppeal:
        self.validate_appeal(receiving_court)
        self.status = CaseStatus.submitted_for_appeal
        return RecordOnAppeal(
            original_case_id=self.id,
            docket_entries=list(map(RecordOnAppealDocketEntry.from_docket_entry, self.docket_entries)),
            title=self.title,
            status=CaseStatus.submitted_for_appeal,
            receiving_court=receiving_court.id if receiving_court else None,
            court=self.court,
            sealed=self.sealed,
            date_filed=datetime.datetime.now(),
        )

    def validate_appeal(self, court: Optional[Court]) -> None:
        if self.status == CaseStatus.on_appeal or self.status == CaseStatus.submitted_for_appeal:
            raise ValueError(f"A record of appeal has already been created for Case {self.id}")
        if court and court.type != CourtType.appellate:
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
            receiving_court = Court.from_id(district_case.court).parent_court()
            if receiving_court is None:
                raise ValueError("Can not determine appelate court")
        else:
            receiving_court = Court.from_id(receiving_court_id)

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
