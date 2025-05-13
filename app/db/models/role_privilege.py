from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey


class RolePrivilege(Base):
    __tablename__ = "role_privileges"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    privilege_id = Column(Integer, ForeignKey(
        "privileges.id"), primary_key=True)

    role = relationship("Role", back_populates="role_privileges")
    privilege = relationship("Privilege", back_populates="role_privileges")
