from faker import Faker
import pytz
import re
import random
import string
import uuid
from datetime import timedelta, datetime

from epic_events.models.user import User
from epic_events.models.role import Role
from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.event import Event

f = Faker(['fr_FR'])
timezone = pytz.timezone('Europe/Paris')

password_regex = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


def generate_password(password_regex):
    password = None
    while password is None or not password_regex.fullmatch(password):
        password = ''.join(
            random.choice(string.ascii_letters + string.digits + "#?!@$%^&*-")
            for _ in range(10))
        return password


def generate_email(name, role):
    firstname = name.split(" ")[1]
    lastname = name.split(" ")[0]
    email = f"{firstname}.{lastname}-{role}@epicevent.com"
    return email.lower()


def generate_roles():
    role_1 = Role(id=1, name='support')
    role_2 = Role(id=2, name='management')
    role_3 = Role(id=3, name='commercial')
    roles_list = [role_1, role_2, role_3]
    return roles_list


def generate_user(role, id, password, ):
    name = f.name()
    user = User(id=id,
                name=name,
                email=generate_email(name, role.name),
                role_id=role.id,
                password=password,
                role=role)
    user.hash_pass(password)
    return user

# To generate fake roles  conftest
# role_list = generate_roles()

# To generate fake users dict for conftest
# user1, user2, user3 = generate_user(role_list[0],'4','S3CRET@26'), generate_user(role_list[1],'5','S3CRET@27'), generate_user(role_list[2],'6','S3CRET@28')
# print('')
# print(vars(user1))
# print('')
# print(vars(user2))
# print('')
# print(vars(user3))


def generate_client(id):
    full_name = f.name()
    email = generate_email(full_name, 'client')
    phone = f.phone_number()
    company_name = f.company().replace(' ', '-') + " & Co."
    creation_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    last_contact_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    client = Client(id=id,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    company_name=company_name,
                    creation_date=creation_date,
                    last_contact_date=last_contact_date)
    return client

# To generate fake clients dict for conftest
# note that date format must be  : datetime(2024, 12, 24, 19, 20)

# client1, client2, client3 = generate_client('1'), generate_client('2'), generate_client('3')
# print(vars(client1))
# print('')
# print(vars(client2))
# print('')
# print(vars(client3))


def generate_contract(id, client_id, management_contact_id):
    total_amount = f.random_int(min=0, max=15000)
    remaining_amount = f.random_int(min=0, max=5000)
    status = False
    contract = Contract(id=id,
                        client_id=client_id,
                        uuid=str(uuid.uuid4()),
                        management_contact_id=management_contact_id,
                        total_amount=total_amount,
                        remaining_amount=remaining_amount,
                        status=status)
    return contract

# To generate fake contracts dict for conftest
# contract1,contract2,contract3 = generate_contract("1","1","3"),generate_contract("2","2","3"),generate_contract("3","3","3")
# print(vars(contract1))
# print('')
# print(vars(contract2))
# print('')
# print(vars(contract3))


def generate_event(id, contract_id):
    support_contact_id = None
    name = f.first_name() + "-Event"
    start_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    end_date = (datetime.strptime(start_date, '%d-%m-%Y - %H:%M') +
                timedelta(hours=24)).strftime('%d-%m-%Y - %H:%M')
    location = f.address()
    attendees = f.random_int(min=0, max=500)
    notes = f.text(max_nb_chars=80)
    event = Event(id=id,
                  name=name,
                  contract_id=contract_id,
                  support_contact_id=support_contact_id,
                  start_date=start_date,
                  end_date=end_date,
                  location=location,
                  attendees=attendees,
                  notes=notes)
    return event

# To generate fake events dict for conftest
# note that date format must be  : datetime(2024, 12, 24, 19, 20)

# event1,event2,event3 = generate_event("1","3"),generate_event("2","3"),generate_event("3","3")
# print(vars(event1))
# print(vars(event2))
# print(vars(event3))




