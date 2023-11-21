import pytest
from click.testing import CliRunner

from epic_events.models.base import Base
from epic_events.tests.fake_datas import (generate_user, generate_roles)

from datetime import datetime


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    return [
        ("roles", [
            {
                "id": 1,
                "name": "support",
            },
            {
                "id": 2,
                "name": "management",
            },
            {
                "id": 3,
                "name": "commercial",
            },
        ]),
        (
            "users",
            [
                {
                    "id":
                        1,
                    "name":
                        "Kevin",
                    'email':
                        "keven@epicevent.com",
                    'role_id':
                        1,
                    'password':
                        "$argon2id$v=19$m=65536,t=12,"
                        "p=4$U8q5916rdY4xRgihdA4hZA$DG/JgT0jwh4ArcbMPQ7Xv3ZdOjUitPDn9KFq2jnbYH0"
                    # S3CRET@23
                },
                {
                    "id":
                        2,
                    "name":
                        "Denis Chamart",
                    'email':
                        "Denis Chamartt@epicevent.com",
                    'role_id':
                        2,
                    'password':
                        "$argon2id$v=19$m=65536,t=12,"
                        "p=4$ujdmTAmhVIoRglDKGWPMGQ$EuA/DgPVl95jk/OmNbYRfXRtLhao0d35ZjPSwHHhIeU"
                    # S3CRET@24
                },
                {
                    "id":
                        3,
                    "name":
                        "Pierre",
                    'email':
                        "Pierre@epicevent.com",
                    'role_id':
                        3,
                    'password':
                        "$argon2id$v=19$m=65536,t=12,"
                        "p=4$eC+F8B5j7L2Xcu49B8D4Xw$WJQ7xOedcIUVk+U1W1xrWgzAUcLi33wbqKoC8m8cgzg"
                    # S3CRET@25
                },
                {
                    'id':
                        4,
                    'name':
                        'Alex-Élise Charpentier',
                    'email':
                        'charpentier.alex-élise-supportt@epicevent.com',
                    'role_id':
                        1,
                    'password':
                        '$argon2id$v=19$m=65536,t=12,p=4$dE5JaY1xDqEUYkxJ6V3LmQ$gt/S2lmFj6Gv14qf9Fzp+3bITy1VanYCA6kRnO/xVrM'
                    # S3CRET@26
                },
                {
                    'id':
                        5,
                    'name':
                        'Gabrielle Mallet',
                    'email':
                        'mallet.gabrielle-management@epicevent.com',
                    'role_id':
                        2,
                    'password':
                        '$argon2id$v=19$m=65536,t=12,p=4$yDnnvNcagxDifE+pFcKYcw$2RX41/P7ZljWvAr5cgP0s5KfeNBce9akulDam8mahLY'
                    # S3CRET@27
                },
                {
                    'id':
                        6,
                    'name':
                        'Jules Evrard',
                    'email':
                        'evrard.jules-commercial@epicevent.com',
                    'role_id':
                        3,
                    'password':
                        '$argon2id$v=19$m=65536,t=12,p=4$htCaU4qRcu4dA8CYc+59zw$8gLiL/pGyNE9NukICpHQHf5yHSxgcSoeNQ0CD0yhqo0'
                    # S3CRET@28
                }
            ]),
        ("clients", [{
            'id': "1",
            'full_name': 'Adrien Lelièvre de Coste',
            'email': 'lelièvre.adrien-client@epicevent.com',
            'phone': '+33 6 98 31 70 48',
            'company_name': 'Laroche & Co.',
            'creation_date': datetime(2023, 6, 24, 14, 0),
            'last_contact_date': datetime(2023, 7, 24, 15, 0),
            'commercial_contact_id':None

        }, {
            'id': '2',
            'full_name': 'Noël Masson',
            'email': 'masson.noël-client@epicevent.com',
            'phone': '+33 (0)4 88 80 55 52',
            'company_name': 'Bouvet-S.A.R.L & Co.',
            'creation_date': datetime(2023, 10, 24, 10, 0),
            'last_contact_date': datetime(2023, 11, 10, 14, 0),
            'commercial_contact_id':None
        }, {
            'id': '3',
            'full_name': 'Alix Peron',
            'email': 'peron.alix-client@epicevent.com',
            'phone': '0298994244',
            'company_name': 'Mathilde-Roger-Costa & Co.',
            'creation_date': datetime(2023, 3, 10, 11, 32),
            'last_contact_date': datetime(2023, 11, 14, 18, 0),
            'commercial_contact_id':None
        }]),
        ("contracts", [{
            'id': '1',
            'uuid': 'd707c9f1-3d3b-48a5-b5a7-2529a5d2fa79',
            'client_id': '1',
            'management_contact_id': '3',
            'total_amount': 13757,
            'remaining_amount': 227,
            'creation_date': datetime(2023, 7, 25, 11, 32),
            'status': False
        }, {
            'id': '2',
            'uuid': '374e5575-35c1-4810-afbe-bf3c2836dfdd',
            'client_id': '2',
            'management_contact_id': '3',
            'total_amount': 1051,
            'remaining_amount': 3671,
            'creation_date': datetime(2023, 11, 12, 11, 32),
            'status': False
        }, {
            'id': '3',
            'uuid': '374e5575-35c1-4810-afbe-bf3c28365fdz',
            'client_id': '2',
            'management_contact_id': '3',
            'total_amount': 8664,
            'remaining_amount': 3464,
            'creation_date': datetime(2023, 11, 18, 11, 32),
            'status': False
        }]),
        ("events", [{
            'id':
                '1',
            'name':
                'Michèle-Event',
            'contract_id':
                '3',
            'support_contact_id':
                1,
            'start_date':
                datetime(2024, 10, 10, 19, 0),
            'end_date':
                datetime(2024, 10, 11, 20, 0),
            'location':
                '60, avenue Philippine Colin\n09105 Martel-sur-Roger',
            'attendees':
                476,
            'notes':
                'Côte votre abri jeune. Lumière croire chanter social gouvernement rejoindre.'
        }, {
            'id':
                '2',
            'name':
                'René-Event',
            'contract_id':
                '3',
            'support_contact_id':
                None,
            'start_date':
                datetime(2024, 1, 12, 19, 20),
            'end_date':
                datetime(2024, 1, 13, 14, 20),
            'location':
                'avenue Françoise Gaillard\n52202 Perrier',
            'attendees':
                204,
            'notes':
                'Claire gouvernement relever même animer premier monsieur.'
        }, {
            'id':
                '3',
            'name':
                'René-Event',
            'contract_id':
                '3',
            'support_contact_id':
                None,
            'start_date':
                datetime(2024, 12, 24, 19, 20),
            'end_date':
                datetime(2024, 12, 2, 14, 0),
            'location':
                '62, avenue de Da Costa\n48273 Sainte Olivie',
            'attendees':
                117,
            'notes':
                'Main juste qui prêt sourire escalier. Mon servir or.'
        }]),
    ]


@pytest.fixture
def role_list_mock():
    roles_list = generate_roles()
    return roles_list


@pytest.fixture
def mock_specific_user(role_list_mock):
    user_manager = generate_user(role_list_mock[0], 1,"S3cret@23")
    user_commercial = generate_user(role_list_mock[1], 2,"S3cret@23")
    user_support = generate_user(role_list_mock[2], 3,"S3cret@23")
    users_list = [user_manager, user_commercial, user_support]
    return users_list

