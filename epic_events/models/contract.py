from epic_events.models.base import Base
from sqlalchemy import (Column, Integer, DateTime, ForeignKey, Boolean, func,
                        )
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    management_contact_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Integer, nullable=False)
    remaining_amount = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=func.now())
    status = Column(Boolean, nullable=False)

    client = relationship('Client', backref='contracts')
    management_contact = relationship('User', backref='contracts')

    def __repr__(self):
        return f"<Contract(id={self.id}, uuid='{self.uuid}', total_amount={self.total_amount}, status={self.status})>"

    def __str__(self):
        return f"Contract(id={self.id}, uuid='{self.uuid}', total_amount={self.total_amount}, status={self.status})"
