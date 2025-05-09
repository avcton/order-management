from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Privilege(Base):
    __tablename__ = "privileges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

    role_privileges = relationship(
        "RolePrivilege", back_populates="privilege", cascade="all, delete-orphan")
