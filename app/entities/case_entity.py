from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class CaseEntity():
    '''
    This is a base class for almost records and cases including Cases, ROAs,
    and DocketEntries. All will need an id, an owning court, and date tracking.
    '''
    id: int = field(init=False)
    court: str
    created_at: datetime = field(init=False)
    updated_on: datetime = field(init=False)
