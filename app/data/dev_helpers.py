'''
These DB functions are only here to help reset data quickly during development.
There is [probably] no reason to have them after initial dev work
'''
import json
from app.schemas import CaseInput as Case_Validator
from sqlalchemy.orm import Session

from .case.case import DistrictCase_DTO, Case_DTO
from .case.docket_entry import DocketEntry_DTO

CASE_DATA_PATH = "./seed_data/case.json"


class CaseDevUtil:
    def delete_all(self, db: Session) -> bool:
        '''Deletes all cases from Database -- only for development'''
        db.query(DocketEntry_DTO).delete()
        db.query(Case_DTO).delete()
        db.commit()
        return True

    def add_seed_cases(self, db: Session) -> bool:
        db.execute("ALTER SEQUENCE cases_id_seq RESTART WITH 1")
        db.execute("ALTER SEQUENCE docket_entries_id_seq RESTART WITH 1")

        with open(CASE_DATA_PATH, 'r') as case_file:
            cases = json.load(case_file)
            for case in cases:
                c = Case_Validator(**case)
                c.docket_entries = [DocketEntry_DTO(**d.dict()) for d in c.docket_entries]
                db_case = DistrictCase_DTO(**c.dict())
                db.add(db_case)
            db.commit()
        return True


case_dev_util = CaseDevUtil()
