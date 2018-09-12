# election-boards
election-boards is the RESTful server for providing election boards information. It is written in **Django Rest Framework**, and a revision of rest part in g0v [councilor-vote-guide project](https://github.com/g0v/councilor-voter-guide.git).

## Prerequisite

### Install dependencies
```bash
pip install -r requirements.txt
```

### Prepare Postgresql server
#### Create Postgresql server
On Mac(using `brew`)
```bash
brew install postgresql
```
If the service not start automatically:
```bash
brew services start postgresql
```

#### Install PostGIS extension
On Mac you need to install extra library `postgis` on your machine before create extension in postgresql:
```bash
brew install postgis;
```
Then in postgres CLI type to create extension:
```postgres
CREATE EXTENSION postgis;
```

### Create database for Django
Default is using `election_boards`. It could be changed in `settings`
```postgres
CREATE DATABASE election_boards;
```

### Import g0v data for candidates
Firstly, download the postgres [dump](https://github.com/g0v/councilor-voter-guide/blob/master/voter_guide/local_db.dump). Then it could be restore in our new database using:
```bash
pg_restore -v -U [POSTGRESQL_USER] -d election_boards -h localhost [DUMP_FILE_NAME]
```
The dump data are import into database `election_boards`.

### Set `DJANGO_SETTINGS_MODULE`
In local develop mode, default is using config in `/election_boards/settings/dev.py`. Set environment envariable like below:
```bash
export DJANGO_SETTINGS_MODULE=election_boards.settings.dev
```

If production environment `/election_boards/settings/production.py` preferred, use:
```bash
export DJANGO_SETTINGS_MODULE=election_boards.settings.production
```

### Migration
#### Clean unnecessary migration files
The cleaning is necessary to reset migration history if your server are starting from the data from g0v project, but there are migration files generated during your development.
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```
(May not necessary)
#### Migrate
Only board is modified for database schema. So here only migrate boards model
```bash
python manage.py makemigrations boards
python manage.py migrate
```

## Run the server

### In development mode
```bash
python manage.py runserver
```

### In production mode
```bash
uwsgi --ini uwsgi.ini
```