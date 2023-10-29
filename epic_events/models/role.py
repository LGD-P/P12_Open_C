from epic_events.models.base import Base
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship('User', back_populates='role')
