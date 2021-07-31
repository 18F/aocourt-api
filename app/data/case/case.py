import datetime
from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from ..database import mapper_registry
from app.entities.case import Case, DocketEntry, DistrictCase, AppellateCase


cases_table = Table(
    'cases',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, nullable=False),
    Column('date_filed', DateTime),
    Column('sealed', Boolean, default=False),
    Column('type', String),
    Column('court', String),
    Column('status', String, nullable=True),
    Column('original_case_id', Integer),
    Column('reviewed', Boolean, default=False),
    Column('remanded', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.datetime.utcnow),
    Column(
        'updated_on',
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
)

docket_entry_table = Table(
    "docket_entries",
    mapper_registry.metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('case_id', Integer, ForeignKey('cases.id'), nullable=False),
    Column('sequence_no', Integer, nullable=False),
    Column('text', String, nullable=False),
    Column('date_filed', DateTime),
    Column('entry_type', String, nullable=False),
    Column('sealed', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.datetime.utcnow),
    Column(
        'updated_on',
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
)


def run_mappers():
    mapper_registry.map_imperatively(DocketEntry, docket_entry_table)

    mapper_registry.map_imperatively(
        Case,
        cases_table,
        polymorphic_on=cases_table.c.type,
        polymorphic_identity="case",
        properties={
            'docket_entries': relationship(DocketEntry)
        }
    )

    mapper_registry.map_imperatively(
        DistrictCase,
        inherits=Case,
        polymorphic_identity="district"
    )

    mapper_registry.map_imperatively(
        AppellateCase,
        inherits=Case,
        polymorphic_identity="appellate"
    )
