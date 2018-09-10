FROM python:3.5-alpine

RUN addgroup user && adduser -h /home/user -D user -G user -s /bin/sh

COPY . /usr/src/app/election-boards

WORKDIR /usr/src/app/election-boards
ENV DJANGO_SETTINGS_MODULE election_boards.settings.production

RUN apk update \
    && apk add --no-cache gcc libc-dev linux-headers postgresql-dev \
    && apk add --no-cache --virtual .build-deps-testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        gdal-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && mkdir -p /tmp/log/uwsgi \
    && chown -R user:user /tmp/log/uwsgi

EXPOSE 8080
CMD ["/usr/local/bin/uwsgi", "--ini", "uwsgi.ini"]
