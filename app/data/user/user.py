import datetime
from sqlalchemy import Boolean, Column, Integer, String, Table, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database import mapper_registry
from app.entities import User, Role


association_table = Table(
    'user_roles',
    mapper_registry.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"))
)


user_table = Table(
    'users',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('username', String),
    Column('email', String, unique=True, index=True),
    Column('full_name', String),
    Column('hashed_password', String),
    Column('is_active', Boolean, default=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow),
    Column(
        'updated_on',
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
)


def run_mappers():
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            'roles': relationship(Role, secondary=association_table)
        }
    )
