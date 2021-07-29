from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from pydantic import parse_obj_as
from app.data.database import Base
from app.core.enums import CourtType
from ..mixins import TimeStamps
from app.schemas.case import Case as Case_Type


class Case_DTO(TimeStamps, Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date_filed = Column(DateTime)
    sealed = Column(Boolean, default=False)
    docket_entries = relationship("DocketEntry_DTO", cascade="all, delete")
    type = Column(String)
    court = Column(String)
    status = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'case'
    }

    def to_entity(self) -> Case_Type:
        return parse_obj_as(Case_Type, self)


class DistrictCase_DTO(Case_DTO):
    __mapper_args__ = {
        'polymorphic_identity': CourtType.district
    }


class AppellateCase_DTO(Case_DTO):
    original_case_id = Column(Integer)
    reviewed = Column(Boolean, default=False)
    remanded = Column(Boolean, default=False)
    __mapper_args__ = {
        'polymorphic_identity': CourtType.appellate
    }
