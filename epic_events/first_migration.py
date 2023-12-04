from epic_events.models.base import Base
from epic_events.models.user import User
from epic_events.models.role import Role

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

# The only role you need and a super_user attached to it
role_1 = Role(id=1, name='management')
management = User(id=1, name='Gabrielle Mallet', email='mallet.gabrielle-management@epicevent.com', role=role_1,
                  password=os.getenv('MANAGER_PASS'))  # as  S3cret@23

role_2 = Role(id=2, name='commercial')
role_3 = Role(id=3, name='support')


session.add_all([role_1, role_2, role_3, management])
session.commit()

session.close()
