from __future__ import absolute_import, unicode_literals, print_function
from celery.decorators import periodic_task
from celery.schedules import crontab

from google.oauth2 import service_account
import googleapiclient.discovery
from google.cloud import storage

from boards.models import Boards
from django.conf import settings

import subprocess
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'app/gcskeyfile.json'

SPREADSHEET_ID = settings.SPREADSHEET_ID

RANGE_NAME = '表單回應 1!A:L'

@periodic_task(
    run_every=(crontab(hour=3, minute=30)),
    name='app.tasks.backup_db',
    ignore_result=True,
)
def backup_db():

    if settings.BACKUP_DB:
        # Start to dump database
        filename = 'dumps/election_board_{}.dump'.format(int(time.time()))
        print('Start to back up database to file:{}'.format(filename))

        db = settings.DATABASES['default']
        command = 'pg_dump -Fc --dbname=postgresql://{}:{}@localhost/{} -f {}'.format(db['USER'], db['PASSWORD'], db['NAME'], filename)
        pop = subprocess.Popen(command, shell=True)
        pop.wait()
        print('backup finished')

        # Start upload procedure
        client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

        bucket_name = 'projects.readr.tw'
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob('election-board/{}'.format(filename))
        blob.upload_from_filename(filename)

        # Delete db dump
        rmdb = subprocess.Popen('rm {}'.format(filename), shell=True)
        rmdb.wait()
        print('file {} deleted!'.format(filename))
    else:
        print('Set not to backup db')

@periodic_task(
    run_every=(crontab(hour='*/6')),
    name='app.tasks.check_spreadsheet',
    ignore_result=True,
)
def check_spreadsheet():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials, cache_discovery=False)
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    values = result.get('values', [])
    if not values:
        print('No data found')
    else:
        for row in values[1:]:
            # Check if this row is verified
            if len(row) == 12 and row[11].upper() == 'Y':
                # Parse board id
                try:
                    board_id = int(row[2])
                except ValueError:
                    print('board id could not be parsed')
                    continue
                # Get board instance to update on board id
                try:
                    board = Boards.objects.get(id=board_id)
                except Boards.DoesNotExist:
                    print('Board {} does not exists.'.format(board_id))
                    continue
                # Parse price
                if row[6] is not None and row[6] != '':
                    try:
                        price = int(row[6])
                        board.price = price
                    except ValueError:
                        # Situation when content couldn't convert to integer
                        # NOT A PRICE
                        print('price not an integer')
                else:
                    print('cannot parse price')

                # Parse receipt
                if row[7] is not None and row[7] != '':
                    receipt = list(map(lambda x: x.strip(), row[7].split(',')))
                    board.receipt = receipt

                #Parse Note
                if row[10] is not None and row[10] != '':
                    board.note = row[10]

                # Update board
                board.save()
            else:
                print('not verified')
 
