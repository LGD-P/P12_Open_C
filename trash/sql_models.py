from sqlalchemy import (
    create_engine, Column, Integer,
    String, DateTime, ForeignKey, Boolean, func, Enum
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

ROLES = ["commercial", "management", "support"]


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # à rajouter password = Column(String, nullable=False)
    role = Column(Enum(*ROLES, name='user_roles'), nullable=False)
    # à rajouter une méthode pour gérer le hash et le check du password

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False, default="None")
    creation_date = Column(DateTime, nullable=False, default=func.now())
    last_contact_date = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now())

    commercial_contact_id = Column(Integer, ForeignKey('users.id'))
    commercial_contact = relationship('User', backref='clients')

    def __repr__(self):
        return f"<Client(id={self.id}, full_name='{self.full_name}', email='{self.email}')>"

    def __str__(self):
        return f"Client(id={self.id}, full_name='{self.full_name}', email='{self.email}')"


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


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(250), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(800))

    contract = relationship('Contract', backref='events')
    support_contact = relationship('User', backref='events')

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}')>"

    def __str__(self):
        return f"Event(id={self.id}, name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}')"
