from epic_events.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def database(func):
    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)
        engine = create_engine(
            os.environ.get("DATABASE_URL"))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            ctx.obj['session'] = session
            return func(ctx, *args, **kwargs)
    return wrapper
