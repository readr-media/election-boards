# election-boards
election-boards is the RESTful server for providing election boards information. It is written in **Django Rest Framework**, and a revision of g0v [councilor-vote-guide project](https://github.com/g0v/councilor-voter-guide.git).

## Prerequisite

### Install dependencies
```bash
pip install -r requirements.txt
```
### Set `DJANGO_SETTINGS_MODULE`
In local develop mode, use config in `/election_boards/settings/dev.py`, set environment envariable like below:
```bash
export DJANGO_SETTINGS_MODULE=election_boards.setting.dev
```

If production environment `/election_boards/settings/production.py` preferred, use:
```bash
export DJANGO_SETTINGS_MODULE=election_boards.setting.production
```
