from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import parse_obj_as

from app.entities import User
from app.data.database import Base
from ..role.role import association_table
from ..mixins import TimeStamps


class User_DTO(TimeStamps, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role_DTO", secondary=association_table)

    def to_entity(self) -> User:
        print("Self", self.email, self.id, self.full_name)
        return parse_obj_as(User, self)
