from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqla_models import User, Client, Contract, Event, Base

engine = create_engine(
    'postgresql://postgres:MyPassIs23Word@localhost:5432/postgres')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()


commercial = User(
    name="John Doe", email="JDoe-commercial@epevent.com", role="commercial")
management = User(name="Tom Henri",
                  email="Thenri-management@epevent.com", role='management')
support = User(name="Charlotte, Green",
               email="CGreen-support@epevent.com", role="support")


client = Client(full_name="CHOMSKY",
                email="Chomsky@client1.com", phone="+33731245675")


contract = Contract(client=client, total_amount=10000, remaining_amount=5000,
                    status=True)


event = Event(name="Chomsky-Birthday", contract=contract, support_contact=support.id,
              start_date=datetime(2023, 12, 12), end_date=datetime(2023, 12, 13),
              location="Paris", attendees=50, notes="All attendees consent to come")


session.add_all([commercial, management, support, client, contract, event])


session.commit()


session.close()
