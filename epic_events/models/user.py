from epic_events.models.base import Base
from sqlalchemy import (Column, Integer, String)


import passlib.hash


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def hash_pass(self, password):
        hashed_password = passlib.hash.argon2.using(rounds=12).hash(password)
        self.password = hashed_password

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"
