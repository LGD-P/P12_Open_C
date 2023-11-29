from epic_events.models.base import Base
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.models.role import Role
from epic_events.models.client import Client
from epic_events.models.contract import Contract

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

# The only role you need and a user attached to it
role_1 = Role(id=1, name='management')
management = User(id=1, name='Gabrielle Mallet', email='mallet.gabrielle-management@epicevent.com', role=role_1,
                  password="$argon2id$v=19$m=65536,t=12,p=4$U8q5916rdY4xRgihdA4hZA$DG/"
                           "JgT0jwh4ArcbMPQ7Xv3ZdOjUitPDn9KFq2jnbYH0")  # as  S3CRET@23

role_2 = Role(id=2, name='commercial')
commercial = User(id=2, name='Jules Evrard', email='evrard.jules-commercial@epicevent.com', role=role_2,
                  password="$argon2id$v=19$m=65536,t=12,p=4$ujdmTAmhVIoRglDKGWPMGQ$EuA/"
                           "DgPVl95jk/OmNbYRfXRtLhao0d35ZjPSwHHhIeU")  # as  S3CRET@24

role_3 = Role(id=3, name='support')
support = User(id=3, name='Alex-Élise Charpentier', email='charpentier.alex-élise-supportt@epicevent.com', role=role_3,
               password="$argon2id$v=19$m=65536,t=12,p=4$eC+F8B5j7L2Xcu49B8D4Xw$WJQ7xO"
                        "edcIUVk+U1W1xrWgzAUcLi33wbqKoC8m8cgzg")  # as  S3CRET@25


session.add_all([role_1, role_2, role_3,
                 management, commercial, support])
session.commit()

# Two clients for this example
client_1 = Client(id=1, full_name='Adrien Lelièvre de Coste', email='lelièvre.adrien-client@epicevent.com',
                  phone='+33 6 98 31 70 48', company_name='Laroche & Co.',
                  commercial_contact_id=commercial.id)

client_2 = Client(id=2, full_name='Noël Masson', email='masson.noël-client@epicevent.com',
                  phone='+33 (0)4 88 80 55 52', company_name='Bouvet-S.A.R.L & Co.',
                  commercial_contact_id=commercial.id)

session.add_all([client_1, client_2])
session.commit()

# On signed contract and one not.
contract_signed = Contract(id=1, client_id=client_1.id, management_contact_id=commercial.id,
                           uuid=str(uuid.uuid4()),
                           total_amount=13757, remaining_amount=227,
                           status=True)

contract_not_signed = Contract(id=2, client_id=client_2.id, management_contact_id=commercial.id,
                               uuid=str(uuid.uuid4()),
                               total_amount=1051, remaining_amount=3671,
                               status=False)

session.add_all([contract_signed, contract_not_signed])
session.commit()


# One event linked to the signed contract.
event = Event(id=1, name='Alex-Elise', contract_id=contract_signed.id, support_contact_id=commercial.id,
              start_date='2024-06-12 - 12:00', end_date='2024-06-13 - 12:00',
              location='60, avenue Philippine Colin\n09105 Martel-sur-Roger',
              attendees=476, notes='All attendees are coming')

session.add_all([event])
session.commit()


session.close()
