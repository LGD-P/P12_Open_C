
- [-]    Réussir à lancer le conteneur Postgres
    - [-]   Voir mon message sur Discord :
     https://hub.docker.com/_/postgres
     docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
    - [-] Faire un PoC du projet
        - [-]Recommendations
            - [-] Utiliser SQL Alchemy comme ORM
            - [-] Utiliser Click pour router les commandes vers des fonctions
        - [-] Réussir à faire des intéractions avec la base de donnée
        - [-] Réussir à insérer un model en base de donnée
        - [-] Réussir à insérer et afficher de la donnée via une commande
            - [-] Click
            - [-] Puis utilisation des models de l'ORM pour insérer/récupérer
