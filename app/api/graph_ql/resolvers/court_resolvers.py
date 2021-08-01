from typing import List
from ariadne import ObjectType
from app.core.courts import courts
from app.entities import Court

court = ObjectType("Court")


@court.field("lowerCourts")
def resolve_lower_courts(obj: Court, *_) -> List[Court]:
    '''Given a court, find all the courts that list this as it's parent'''
    return [Court(**c, id=id) for id, c in courts.items() if c['parent'] == obj.id]
