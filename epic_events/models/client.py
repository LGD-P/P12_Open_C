from epic_events.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False, default="None")
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    last_contact_date = Column(DateTime,
                               nullable=False,
                               default=datetime.utcnow(),
                               onupdate=datetime.utcnow())

    commercial_contact_id = Column(Integer, ForeignKey('users.id'))
    commercial_contact = relationship('User', backref='clients')

    def __repr__(self):
        return f"<Client(id={self.id}, full_name='{self.full_name}', " \
               f"email='{self.email}')>"

    def __str__(self):
        return f"Client(id={self.id}, full_name='{self.full_name}', " \
               f"email='{self.email}')"
