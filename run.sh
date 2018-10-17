supervisord -c /etc/supervisor/supervisord.conf && python manage.py migrate && /usr/local/bin/uwsgi --ini uwsgi.ini
