import gspread
import query
from time import sleep
from config import GeneralConfig, NameTagConfig, QueryConfig

# Globals
DATA = GeneralConfig.DATA
EVENT_PERSON = GeneralConfig.EVENT_PERSON
NODE = GeneralConfig.NODE
FIRST_NAME = GeneralConfig.FIRST_NAME
LAST_NAME = GeneralConfig.LAST_NAME
EMAIL = GeneralConfig.EMAIL
PHONE_NUMBER = GeneralConfig.PHONE_NUMBER
EVENT_ID = QueryConfig.event_id

DEFINITION = GeneralConfig.DEFINITION
TRANSLATION = GeneralConfig.TRANSLATION

def _cell_range(row):
    return "A" + str(row) + ":I" + str(row)

# set up Google Sheet Log
service_account = gspread.service_account(filename=GeneralConfig.GOOGLE_LOG_KEYFILE_NAME)
log_sheet = service_account.open(GeneralConfig.GOOGLE_BACKUP_DB_SHEET_NAME)
work_sheet = log_sheet.worksheet(GeneralConfig.WORKSHEET_BACKUP_DB_NAME)
row_insert = 2

backup_variable = {'first': 3000}
backup_database = query.backup_database_query(EVENT_ID, backup_variable)
nodes = backup_database.json()[DATA][EVENT_PERSON][NODE]

print(f"Record Size {len(nodes)}")
for eventPerson in nodes:

    print(eventPerson)

    first_name, last_name, major, year, regis_id = '', '', '', '', ''
    email, phone_number, studentID, groupname = '', '', '', ''

    first_name = eventPerson[FIRST_NAME]
    last_name = eventPerson[LAST_NAME]
    email = eventPerson[EMAIL]
    if not eventPerson[PHONE_NUMBER] == []:
        phone_number = eventPerson[PHONE_NUMBER][0]["number"]

    if not eventPerson['groups'] == []:
        for group in eventPerson['groups']:
            groupname += group['name'] + ' '

    fields = eventPerson['withEvent']['fields']
    first_major_flag = True
    for field in fields:
        if first_major_flag and DEFINITION in field and field[DEFINITION][TRANSLATION][0]['name'] == 'Major':
            # MultipleSelectField query structure
            major = field[TRANSLATION][0]['value']
            first_major_flag = False

        if DEFINITION in field and field[DEFINITION][TRANSLATION][0]['name'] == 'School Year':
            # SelectField query structure
            year = field[TRANSLATION][0]['value']

        if DEFINITION in field and field[DEFINITION][TRANSLATION][0]['name'] == 'Student ID':
            # NumberField query structure - name aliasing
            studentID = field['studentID']

    badges = eventPerson['withEvent']['badges']
    if not badges == []:
        regis_id = badges[0]['barcode']

    organized_data = [[studentID, groupname, first_name, last_name, major, year,
                       regis_id, email, phone_number]]
    work_sheet.update(_cell_range(row_insert), organized_data)

    sleep(1)
    row_insert += 1
