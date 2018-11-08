FROM python:3.5.6-slim-jessie

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

COPY . /usr/src/app/election-boards

WORKDIR /usr/src/app/election-boards
ENV DJANGO_SETTINGS_MODULE election_boards.settings.production

RUN apt-get update \
    && apt-get install -y gcc gdal-bin supervisor sudo \
    && sudo apt-get install -y curl ca-certificates \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - \
    && sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && sudo apt-get update \
    && mkdir -p /usr/share/man/man1 /usr/share/man/man7 dumps /tmp/log/uwsgi /var/log/celery /var/run/celery \
    && chown -R user:user /usr/src/app/election-boards /tmp/log/uwsgi /var/run/celery\
    && sudo apt-get install -y postgresql-client-9.6 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && mv supervisor.conf/*.conf /etc/supervisor/conf.d \
    && touch /var/log/celery/worker.log \
    && touch /var/log/celery/beat.log

EXPOSE 8080
CMD ["/bin/bash", "run.sh"]
