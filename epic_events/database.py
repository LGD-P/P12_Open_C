from epic_events.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def create_database():
    engine = create_engine(
        os.environ.get("DATABASE_URL"))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session

