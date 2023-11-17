from faker import Faker
import pytz
import re
import random
import string
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
    # mettre le même pass à tous pour éviter les pb après le hash...
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


def generate_user(role, id):
    name = f.name()
    password = "S3cret@23"
    user = User(id=id, name=name, email=generate_email(name, role.name),
                role_id=role.id, password=password, role=role)
    user.hash_pass(password)
    return user


def generate_roles():
    role_1 = Role(id=1, name='management')
    role_2 = Role(id=2, name='commercial')
    role_3 = Role(id=3, name='support')
    roles_list = [role_1, role_2, role_3]
    return roles_list


def generate_client():
    full_name = f.name()
    email = generate_email(full_name, 'client')
    phone = f.phone_number()
    company_name = f.company_name()
    creation_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    last_contact_date = f.date_time(
        tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    return Client(full_name=full_name, email=email, phone=phone,
                  company_name=company_name, creation_date=creation_date,
                  last_contact_date=last_contact_date)


def generate_contract(client_id, management_contact_id):
    total_amount = f.random_int(min=0, max=15000)
    remaining_amount = f.random_int(min=0, max=5000)
    status = False
    return Contract(client_id=client_id,
                    management_contact_id=management_contact_id,
                    total_amount=total_amount,
                    remaining_amount=remaining_amount,
                    status=status)


def generate_event(name, contract_id):
    support_contact_id = None
    start_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
    end_date = (datetime.strptime(start_date, '%d-%m-%Y - %H:%M') +
                timedelta(hours=24)).strftime('%d-%m-%Y - %H:%M')
    location = f.address()
    attendees = f.random_int(min=0, max=500)
    notes = f.text(max_nb_chars=80)
    return Event(name=name, contract_id=contract_id,
                 support_contact_id=support_contact_id, start_date=start_date,
                 end_date=end_date, location=location,
                 attendees=attendees, notes=notes)
