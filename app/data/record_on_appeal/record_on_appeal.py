import datetime

from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from ..database import mapper_registry
from app.entities import RecordOnAppeal, RecordOnAppealDocketEntry

roa_table = Table(
    'records_on_appeal',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('original_case_id', Integer, ForeignKey('cases.id'), nullable=False),
    Column('title', String, nullable=False),
    Column('date_filed', DateTime),
    Column('sealed', Boolean, default=False),
    Column('type', String),
    Column('court', String),
    Column('receiving_court', String),
    Column('status', String, nullable=True),
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

roa_docket_entry_table = Table(
    "roa_docket_entry",
    mapper_registry.metadata,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('case_id', Integer, ForeignKey('records_on_appeal.id'), nullable=False),
    Column('sequence_no', Integer, nullable=False),
    Column('court', String, nullable=False),
    Column('recieving_court', String, nullable=True),
    Column('text', String, nullable=False),
    Column('date_filed', DateTime),
    Column('entry_type', String, nullable=False),
    Column('sealed', Boolean, default=False),
    Column('include_with_appeal', Boolean, default=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow),
    Column(
        'updated_on',
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
)


def run_mappers():
    mapper_registry.map_imperatively(RecordOnAppealDocketEntry, roa_docket_entry_table)
    mapper_registry.map_imperatively(
        RecordOnAppeal,
        roa_table,
        properties={
            'docket_entries': relationship(
                RecordOnAppealDocketEntry,
                order_by="asc(RecordOnAppealDocketEntry.sequence_no)"
            )
        }
    )
