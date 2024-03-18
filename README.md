# Projet de gestion de données avec Python, Docker et PostgreSQL

Ce projet consiste en une application Python hebergée sur Docker qui récupère des fichiers CSV, les importe dans une base de données PostgreSQL également dockerisée, exécute deux requêtes sur ces données, puis exporte les résultats en CSV. L'ensemble de l'application ainsi que les tests sont encapsulés dans des conteneurs Docker indépendants pour assurer la portabilité et la facilité de déploiement.


### Structure du Projet

- **app**
  - **database.py** : Contient les méthodes connect, execute_query, close.
  - **utils.py** : Permet d'importer le CSV avec Pandas et d'exporter en CSV.
  - **main.py** : Contient les 2 requêtes et fait appel à database et utils.
- **tests**
  - **test_customer_analysis.py**
  - **test_sales_report.py**
- **Docker**
  - **Dockerfile** : Lance main.py.
  - **Dockerfile.test** : Lance pytest.
  - **init_db.sql** : Crée les tables dans la base de données.
  - **wait-for-it.sh** : Issu du repo [wait-for-it](https://github.com/vishnubob/wait-for-it/tree/master), permet d'attendre que la base de données se lance pour lancer app et tests.
- **output** : Contient les fichiers CSV résultant des 2 requêtes.
- **resources** : Contient les 3 fichiers CSV qui permettent la manipulation des données.
- **docker-compose.yml** : Lance les services app, tests et db.
- **requirements.txt**
- **requirements-test.txt**

### Prérequis

- Docker
- docker-compose

### Instructions

Assurez-vous que les fichiers CSV nécessaires pour la manipulation des données sont présents dans le dossier resources avant de lancer l'application. Les résultats des requêtes seront exportés dans le dossier output.

1. **Cloner le projet :**
   ```
   git clone https://github.com/SZPNR/python-csv-postgres-docker.git
   ```
   
3. **Accéder au répertoire du projet :**
   ```
   cd python-csv-postgres-docker 
   ```
   
4. **Build avec docker-compose :**
   ```
   docker-compose build
   ```

5. **Lancement de toute l'application avec les tests :**
   ```
   docker-compose up
   ```
   
6. **Lancement de l'application sans les tests :**
   ```
   docker-compose up app
   ```
   
7. **Lancement des tests :**
   ```
   docker-compose up tests
   ```
   
8. **Accéder aux fichiers CSV résultants :**
   Les fichiers CSV résultants seront disponibles dans le répertoire `output`.



