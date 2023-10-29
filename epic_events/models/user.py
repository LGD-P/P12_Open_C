from epic_events.models.base import Base
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from epic_events.views.users_view import input_old_pass
import passlib.hash


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    password = Column(String, nullable=False)

    role = relationship('Role', back_populates='users')

    def hash_pass(self, password):
        hashed_password = passlib.hash.argon2.using(rounds=12).hash(password)
        self.password = hashed_password
        return self.password

    def confirm_pass(self, password):
        initial_password = input_old_pass()
        checking = passlib.hash.argon2.verify(initial_password, password)
        return checking

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"
