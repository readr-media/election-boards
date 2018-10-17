from __future__ import absolute_import, unicode_literals, print_function
from celery.decorators import periodic_task
from celery.schedules import crontab

from google.oauth2 import service_account
import googleapiclient.discovery

from boards.models import Boards

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'app/gcskeyfile.json'

SPREADSHEET_ID = '19UjwwLiQ_jfpzsjG_VKlNn1b3dGoFCs3ZOR4s7yGb0I'
RANGE_NAME = '表單回應 1!A:K'

@periodic_task(
    run_every=(crontab(hour='*/6')),
    name='app.tasks.check_spreadsheet',
    ignore_result=True,
)
def check_spreadsheet():
    print('hello spreadsheet')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    values = result.get('values', [])
    if not values:
        print('No data found')
    else:
        for row in values[1:]:
            # Check if this row is verified
            if len(row) == 11 and row[10].upper() == 'Y':
                try:
                    board_id = int(row[2])
                except ValueError:
                    print('board id could not be parsed')
                    continue
 
                board = Boards.objects.get(id=board_id)
                print('id:{} image:{}'.format(board.id, board.image))
 
                # Parse price
                if row[6] is not None and row[6] != '':
                    try:
                        price = int(row[6])
                        print('price is:{}'.format(price))
                        board.has_price_info = True
                        board.price = price
                    except ValueError:
                        # Situation when content couldn't convert to integer
                        # NOT A PRICE
                        print('price not an integer')
                else:
                    print('cannot parse price')

                # Parse receipt
                if row[7] is not None and row[7] != '':
                    print('receipt list is:{}'.format(row[7]))
                    receipt = list(map(lambda x: x.strip(), row[7].split(',')))
                    print(receipt)
                    board.has_receipt_info = True
                    board.receipt = receipt

                # Update board
                board.save()
            else:
                print('not verified')
 
