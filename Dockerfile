FROM python:3.5.6-slim-jessie

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

COPY . /usr/src/app/election-boards

WORKDIR /usr/src/app/election-boards
ENV DJANGO_SETTINGS_MODULE election_boards.settings.production

RUN apt-get update \
    && apt-get install -y gcc gdal-bin \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && mkdir -p /tmp/log/uwsgi \
    && chown -R user:user /tmp/log/uwsgi

EXPOSE 8080
CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]