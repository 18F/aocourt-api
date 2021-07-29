'''Seed the database with test data'''
import json

from app.schemas import CaseInput as Case_Validator
from app.data.case.case import DistrictCase_DTO
from app.data.case.docket_entry import DocketEntry_DTO
from app.data.database import SessionLocal

db = SessionLocal()

CASE_DATA_PATH = "./seed_data/case.json"

with open(CASE_DATA_PATH, 'r') as case_file:
    cases = json.load(case_file)
    for case in cases:
        c = Case_Validator(**case)
        c.docket_entries = [DocketEntry_DTO(**d.dict()) for d in c.docket_entries]
        db_case = DistrictCase_DTO(**c.dict())
        db.add(db_case)
    db.commit()
