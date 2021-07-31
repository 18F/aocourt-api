from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.data import user, role
from app.core.config import settings
from app.entities import User
from .database import mapper_registry
from app.core.security import get_password_hash


def init_db(db: Session) -> None:
    '''This is a stub for inserting initial data that may be needed for the application,
    such as initial users. At the moment this is just a couple roles and
    an admin user with these roles assigned.

    Structural changes to the database should happen in migrations, not here.
    In fact, if if turns out data like roles is needed for the application, we
    may opt to put this in migrations as well.
    '''
    initial = user.get_by_email(db, email=settings.INITIAL_ADMIN_USER)
    if not initial:
        admin_role = role.get_by_name(db, rolename='admin')
        clerk_role = role.get_by_name(db, rolename='clerk')

        hashed_password = get_password_hash(settings.INITIAL_ADMIN_PASSWORD)
        roles = [r for r in (admin_role, clerk_role) if r]

        user_in = User(
            email=settings.INITIAL_ADMIN_USER,
            hashed_password=hashed_password,
            roles=roles,
            full_name="Initial Admin",
            username="admin"
        )
        user.add(db, user_in)
        db.commit()


def create_tables():
    '''Set up tables for the tests'''
    engine = create_engine(settings.DATABASE_URL)
    mapper_registry.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
