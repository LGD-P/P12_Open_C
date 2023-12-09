

<p align = center>
<img  src="img/logo.png" />
</p>

# Epic Events

<p align = center>Ce project est un C.R.M, Client. Relationship. Management. réalisé avec une C.L.I, Command. Line. 
Interface réalisée s'appayant sur Python3.11 et :</p>

<p align = center>
    <a href="https://www.docker.com/">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original-wordmark.svg" width="65"/>
    </a>
    <a href="https://www.postgresql.org/">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original-wordmark.svg" width="65"/>
    </a>
    <a href="https://www.sqlalchemy.org/">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" width="65"/>
    </a>
    <a href="https://click.palletsprojects.com/en/8.1.x/">
        <img src="https://click.palletsprojects.com/en/8.1.x/_images/click-logo.png" width="80" />
    </a>
</p>

## But du project : 
- Au sein d'une équipe évènementielle ayant pour Role : Management Commercial Support
- Les Users doivent pouvoir gérer des relations Clients Contracts Events (C.R.U.D en fonction de leurs
attributions respectives)
- SQLAlchemy est l'O.R.M qui sécurisera nos requêtes en base de données.
- Un système de permission et l'utilisation de py-jwt viendra compléter la sécurité de l'app.
- Le projet sera monitoré sur [Sentry](https://sentry.io/welcome/)

<p align = center>
<img  src="img/diagram.png" />
</p>


# Installation du project:

## Cloner le projet:
```bash
    git clone https://github.com/LGD-P/P12_Open_C.git
```
## Installer le gestionnaire de dépendances poetry:<img src="https://python-poetry.org/images/logo-origami.svg" width=30>
    
    pip3 install poetry 

## Activer l'environnement virtuel depuis P12_Open_C/:

    poetry shell 

## Installer les dépendances:

    poetry install 
    poetry update

## Les variables d'environnement : .env
*Ce projet utilise dotenv il vous faut adapter un certain nombre de paramètres.*
*Dans epic_events/.env*
```bash
touch .env
sudo nano .env

DATABASE_URL= postgresql://YOURDBNAME:YOURPASSWORD@localhost:5432/postgres
SECRET_KEY= YOU SECRET_KEY_TO_MANAGE_JWT
TEMP_TOKEN_PATH = PATH/TO_STORE_YOUR_TEMP/TOKEN.txt
SENTRY_KEY = YOUR SENTRY DNS KEY
MANAGER_PASS = $argon2id$v=19$m=65536,t=12,p=4$6V0LgfB+T+kdw/hfCwFgjA$r/+/OEuLdDEdTHvKDn4+mX3Bo3+wLNPcEqvpVxBS3nw
```
```bash
ctrl + X

oui or yes

enter
```

    
## Lancer Docker : 
    
    sudo docker run --name YOURDBNAME -e POSTGRES_PASSWORD=YOURPASSWORD -d -p 5432:5432 postgres

    # avec sudo lsof -i :5432 vous devriez voir la base de données sur votre port 5432. 

## Première alimentation de la base de données :

    python3 first_migration.py

## Il n'y a plus qu'à :

```bash
python3 main.py authenticate login -e 'mallet.gabrielle-management@epicevent.com'
```

*Le mdp du manager est commenté dans first_migration.py*


##   Need Help ?

<p align = center> Comme tout CLI qui se respecte avec --help, vous accéderez au détail des commandes</p>

    python3 main.py --help 
    python3 main.py authenticate --help 
    python3 main.py role --help
    python3 main.py user --help
    python3 main.py client --help
    python3 main.py contract --help
    python3 main.py event --help
    ....
<p align = center>
<img  src="img/help-gif.gif" />
</p>



## Preview de la list- commande : 
    python3 main.py user list-user
    ..
<p align = center>
<img  src="img/list-gif.gif" />
</p>



## Vérifer la couverture du projet par les tests et la conformité flake8 
```bash
    pytest tests/ --cov=. --cov-report html
```
<p align = center>
<img  src="img/coverage.png" />
</p>


```bash
    flake8 --format=html --htmldir=flake-report
```
<p align = center>
<img  src="img/flake8.png" />
</p>

