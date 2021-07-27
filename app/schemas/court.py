from typing import Optional
from pydantic import BaseModel
from app.core.enums import CourtType


class Court(BaseModel):
    '''
    Info on Federal Courts
    '''
    id: str
    type: CourtType
    short_name: str
    full_name: str
    parent: Optional[str] = None
