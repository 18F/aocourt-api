from typing import Optional
from ariadne import ObjectType
from app.entities import User, Court

user = ObjectType("User")


@user.field("court")
def resolve_courts(obj: User, *_) -> Optional[Court]:
    '''Given a user, resolve the court'''
    if obj.court_id:
        return Court.from_id(obj.court_id)
