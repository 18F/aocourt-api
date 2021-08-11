from typing import Optional, TypeVar, Type, List
from dataclasses import dataclass
from app.core.enums import CourtType
from app.core.courts import courts

T = TypeVar('T', bound='Court')


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

    @classmethod
    def from_id(cls: Type[T], court_id: str) -> T:
        court_data = courts[court_id]
        return cls(**court_data, id=court_id)

    def parent_court(self: T) -> Optional[T]:
        if self.parent:
            return courts.get(self.parent)

    def lower_courts(self: T) -> List[T]:
        print(courts)
        return [self.__class__.from_id(id) for id, c in courts.items() if c['parent'] == self.id]
