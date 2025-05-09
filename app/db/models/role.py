from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="role")
    role_privileges = relationship(
        "RolePrivilege", back_populates="role", cascade="all, delete-orphan")
