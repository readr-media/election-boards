# election-boards
election-boards is the RESTful server for providing election boards information. It is written in **Django Rest Framework**, and a partial revision of REST server in g0v [councilor-vote-guide project](https://github.com/g0v/councilor-voter-guide.git).

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

## Start Celery

### In developing
```bash
celery -A election_boards worker -l info -B
```

## Output data for analysis

### SQL command
```SQL
SELECT bb.id "看板ID", bb.image "對照圖片代碼", bb.verified_amount "驗證次數", ST_AsText(bb.coordinates) "座標", CONCAT(county, district, road) "地址", cand.count "候選人姓名", slogans.count "看板標語", amount.count "看板數量" FROM boards_boards AS bb LEFT JOIN (SELECT candidates.board_id, STRING_AGG(candidates.count, ' ') AS count FROM (SELECT bc.board_id, CONCAT(ct.name, '=', COUNT(ct.name)) AS count FROM boards_checks AS bc LEFT JOIN boards_checks_candidates AS bcc ON bc.id = bcc.checks_id LEFT JOIN candidates_terms AS ct ON bcc.terms_id = ct.id WHERE bc.type != 2 GROUP BY bc.board_id, ct.name ORDER BY bc.board_id) AS candidates GROUP BY candidates.board_id) AS cand ON bb.id = cand.board_id LEFT JOIN (SELECT slg.board_id, STRING_AGG(slg.count, ' ') AS count FROM (SELECT bc.board_id, CONCAT(bc.slogan, '=', COUNT(bc.slogan)) AS count FROM boards_checks AS bc GROUP BY bc.board_id, bc.slogan ORDER BY bc.board_id) AS slg GROUP BY slg.board_id) AS slogans ON bb.id = slogans.board_id LEFT JOIN (SELECT amnt.board_id, STRING_AGG(amnt.count, ' ') AS count FROM (SELECT bc.board_id, CONCAT(bc.headcount, '次=', COUNT(bc.headcount)) AS count FROM boards_checks AS bc GROUP BY bc.board_id, bc.headcount ORDER BY bc.board_id) AS amnt GROUP BY amnt.board_id) AS amount ON bb.id = amount.board_id;
```

### SQL output csv
```SQL
\copy (SELECT commands) to 'absolute path + filename' with csv
```
