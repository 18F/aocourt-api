from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.api import dependency
from app.data import case
from app.data.database import get_db

router = APIRouter()
clerk = dependency.AllowRoles(['clerk'])


@router.get("/{case_id}")
def read_items(
    case_id: int,
    db: Session = Depends(get_db)
) -> Any:
    '''
    Returns details about case associated with {case_id}
    '''
    the_case = case.get(db, case_id)
    if the_case is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return the_case
