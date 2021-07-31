from typing import Optional
from dataclasses import dataclass
from app.core.enums import CourtType


@dataclass(frozen=True)
class Court():
    '''
    Info on Federal Courts
    '''
    id: str
    type: CourtType
    short_name: str
    full_name: str
    parent: Optional[str] = None
