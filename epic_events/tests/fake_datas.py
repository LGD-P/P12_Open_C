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
  # Modifier pour attribuer le meme pass pour tous
  # password_regex = re.compile(
  #  "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
  name = f.name()
  # password = generate_password(password_regex)
  password = "S3cret@23"
  user = User(id=id,
              name=name,
              email=generate_email(name, role.name),
              role_id=role.id,
              password=password,
              role=role)
  user.hash_pass(password)
  return user


def generate_roles():
  role_1 = Role(id=1, name='management')
  role_2 = Role(id=2, name='commercial')
  role_3 = Role(id=3, name='support')
  roles_list = [role_1, role_2, role_3]
  return roles_list


def generate_client(id):
  full_name = f.name()
  email = generate_email(full_name, 'client')
  phone = f.phone_number()
  company_name = f.company().replace(' ', '-') + " & Co."
  creation_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
  last_contact_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
  client = Client(id=id,full_name=full_name,
                  email=email,
                  phone=phone,
                  company_name=company_name,
                  creation_date=creation_date,
                  last_contact_date=last_contact_date)
  return client

# client1, client2, client3 = generate_client('1'), generate_client('2'), generate_client('3')
#print(vars(client1))
#print(vars(client2))
#print(vars(client3))


def generate_contract(id,client_id, management_contact_id):
  total_amount = f.random_int(min=0, max=15000)
  remaining_amount = f.random_int(min=0, max=5000)
  status = False
  contract =  Contract(id=id,client_id=client_id,uuid=str(uuid.uuid4()),
                  management_contact_id=management_contact_id,
                  total_amount=total_amount,
                  remaining_amount=remaining_amount,
                  status=status)
  return contract


#contract1,contract2,contract3 = generate_contract("1","1","3"),generate_contract("2","2","3"),generate_contract("3","3","3")
#print(vars(contract1))
#print(vars(contract2))
#print(vars(contract3))



def generate_event(name, contract_id):
  support_contact_id = None
  start_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
  end_date = (datetime.strptime(start_date, '%d-%m-%Y - %H:%M') +
              timedelta(hours=24)).strftime('%d-%m-%Y - %H:%M')
  location = f.address()
  attendees = f.random_int(min=0, max=500)
  notes = f.text(max_nb_chars=80)
  event =  Event(name=name,
               contract_id=contract_id,
               support_contact_id=support_contact_id,
               start_date=start_date,
               end_date=end_date,
               location=location,
               attendees=attendees,
               notes=notes)
  return event






"""
user_1 = generate_user(f.name(), role_1.name)
user_2 = generate_user(f.name(), role_2.name)
user_3 = generate_user(f.name(), role_3.name)


client_1 = generate_client()

contract_1 = generate_contract(client_1.id, user_2.id)

event_1 = generate_event(client_1.company_name, contract_1.id)


email = generate_email(f.name(), 'support')
password = generate_password(password_regex)
print('\n')
print("email = ", email)
print('\n')
print("password =", password)
print('\n')
print(f.name())
print('\n')
print(f.company())
print('\n')
print(f.phone_number())
print('\n')
print(f.address())
print('\n')
print(f.email())
print('\n')
print(f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M'))
start_date = f.date_time(tzinfo=timezone).strftime('%d-%m-%Y - %H:%M')
end_date = (datetime.strptime(start_date, '%d-%m-%Y - %H:%M') + timedelta(hours=24)).strftime('%d-%m-%Y - %H:%M')
print("début : ", start_date)
print("fin :", end_date)
print('\n')
print(f.city())
print('\n')
print(f.random_int(min=0, max=500))
print('\n')
print(f.text(max_nb_chars=200))
print('\n')

"""
