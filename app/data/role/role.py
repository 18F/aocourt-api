from sqlalchemy import Column, Integer, String, Table, ForeignKey

from app.data.database import Base

association_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"))
)


class Role_DTO(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    rolename = Column(String, unique=True, index=True)
