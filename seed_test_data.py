'''Seed the database with test data'''
import json

from app.schemas import CaseInput as Case_Validator
from app.models import DistrictCase, DocketEntry
from app.db.database import SessionLocal

db = SessionLocal()

CASE_DATA_PATH = "./seed_data/case.json"

with open(CASE_DATA_PATH, 'r') as case_file:
    cases = json.load(case_file)
    for case in cases:
        c = Case_Validator(**case)
        c.docket_entries = [DocketEntry(**d.dict()) for d in c.docket_entries]
        db_case = DistrictCase(**c.dict())
        db.add(db_case)
    db.commit()
