from typing import List
from ariadne import ObjectType
from app.entities import Court

court = ObjectType("Court")


@court.field("lowerCourts")
def resolve_lower_courts(obj: Court, *_) -> List[Court]:
    '''Given a court, find all the courts that list this as it's parent'''
    return Court.from_id(obj.id).lower_courts()
