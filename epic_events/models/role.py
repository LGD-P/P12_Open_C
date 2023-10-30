from epic_events.models.base import Base
from epic_events.views.users_view import invalid_role

from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship
import click


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship('User', back_populates='role')

    def role_is_valid(self, value):
        if value in ["support", "commercial", "management"]:
            return value
        else:
            invalid_role()
            raise click.UsageError("Invalid role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', relationship='{self.users}'>"

    def __str__(self):
        return f"Role(id={self.id}, name='{self.name}', relationship='{self.users}')"
