from sqlalchemy import Column, Integer, String, Table

from ..database import mapper_registry
from app.entities import Role

role_table = Table(
    "roles",
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('rolename', String, unique=True, index=True)
)


def run_mappers():
    mapper_registry.map_imperatively(Role, role_table)
