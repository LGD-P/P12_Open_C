from epic_events.models.base import Base
from sqlalchemy import (Column, Integer,
                        String, DateTime, ForeignKey
                        )

from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contract_id = Column(Integer, ForeignKey(
        'contracts.id', ondelete="CASCADE"))
    support_contact_id = Column(
        Integer, ForeignKey('users.id', ondelete="CASCADE"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(250), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(800))

    contract = relationship('Contract', backref='events')
    support_contact = relationship('User', backref='events')

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', "\
            f"start_date='{self.start_date}', end_date='{self.end_date}')>"

    def __str__(self):
        return f"Event(id={self.id}, name='{self.name}', "\
            f"start_date='{self.start_date}', end_date='{self.end_date}')"
