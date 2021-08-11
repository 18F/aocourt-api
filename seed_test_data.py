'''Seed the database with test data'''
import json

from app.entities import DistrictCase, DocketEntry
from app.data.database import SessionLocal

db = SessionLocal()

CASE_DATA_PATH = "./seed_data/case.json"

with open(CASE_DATA_PATH, 'r') as case_file:
    cases = json.load(case_file)
    for case in cases:
        case['docket_entries'] = [DocketEntry(**d, court=case['court']) for d in case['docket_entries']]
        db.add(DistrictCase(**case))
    db.commit()
