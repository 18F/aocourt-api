import datetime
from .docket_entry import DocketEntry, DocketEntryInput
from typing import List, Literal, Union, Optional

from pydantic import BaseModel
from app.core.enums import CourtType, CaseStatus
from app.schemas.court import Court


class CaseBase(BaseModel):
    '''
    Shared properties. All cases need these
    even when first creating them.
    '''
    title: str
    date_filed: datetime.date
    sealed: bool = False
    court: str
    status: Optional[str] = None

    class Config:
        orm_mode = True


class CaseInput(CaseBase):
    '''
    Docket entries won't have things like IDs until
    they are in the DB.
    '''
    docket_entries: List[DocketEntryInput] = []
    type: CourtType


class AppellateCaseInput(CaseInput):
    '''
    Appleate cases need a few extra things at creating time
    '''
    type: CourtType = CourtType.appellate
    original_case_id: int
    reviewed: bool = False
    remanded: bool = False


# After cases are in the Database they will have properties
# like ID and the datetime created. These should be returned
# to the API caller.

class _Case(CaseBase):
    id: int
    created_at: datetime.datetime
    updated_on: datetime.datetime
    docket_entries: List[DocketEntry] = []
    type: CourtType


class DistrictCase(_Case):
    type: Literal[CourtType.district]

    def validate_appeal(self, court: Court) -> None:
        if self.status == CaseStatus.on_appeal:
            raise ValueError(f"Case {self.id} has already been sent to appellate")
        if court.type != CourtType.appellate:
            raise ValueError(f"Can not appeal to {court.full_name}")


class BankruptcyCase(_Case):
    type: Literal[CourtType.bankruptcy]

    def validate_appeal(self, court: Court) -> None:
        pass


class AppellateCase(_Case):
    type: Literal[CourtType.appellate]
    original_case_id: int
    reviewed: bool = False
    remanded: bool = False

    def validate_appeal(self, court: Court) -> None:
        pass


Case = Union[DistrictCase, AppellateCase, BankruptcyCase]
