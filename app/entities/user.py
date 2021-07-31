from typing import List, Optional
from dataclasses import dataclass, field

from .role import Role


@dataclass
class User():
    email: str
    full_name: str
    username: str
    hashed_password: str
    id: Optional[int] = None
    is_active: bool = True
    roles: List[Role] = field(default_factory=list)
