import os

WORKING_DIR = os.getcwd().replace('scripts', '')
TOKEN = os.environ['FIVE_STAR_TOKEN']

OFFICE_COORDINATES = [50.386533, 30.475933]     #latitude. longitude
PRICE_OF_KM = 3 # uah

INITIAL_LOG_TEXT = '\n*********************************************************************************************************************************************\n|№|***********************************message**************************************|***********user**********|************date**************|\n'
DEVELOPER_ID = '116516979'


PRO_RATE = 100
MID_RATE = 75
NEW_RATE = 50

HOURS_BETWEEN_SHIFTS = 6
CHECK_IN_ALLOWED_BEFORE_SHIFT_MIN = 15

STAT_ITEMS_ON_ONE_PAGE = 10

TIME_TRACKER_SECONDS_PERIOD = 600   # 10 min