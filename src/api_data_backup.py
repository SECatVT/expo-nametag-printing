from time import sleep
import gspread
import query
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
END_CURSOR = GeneralConfig.GOOGLE_DB_END_CURSOR

# set up Google Sheet Log
service_account = gspread.service_account(filename=GeneralConfig.GOOGLE_LOG_KEYFILE_NAME)
log_sheet = service_account.open(GeneralConfig.GOOGLE_BACKUP_DB_SHEET_NAME)
work_sheet = log_sheet.worksheet(GeneralConfig.WORKSHEET_BACKUP_DB_NAME)

def _cell_range(row):
    return "A" + str(row) + ":I" + str(row)

def _check_row_insert():
    cursor = ''
    all_values = work_sheet.get_all_values()
    if work_sheet.cell(len(all_values),1).value == END_CURSOR:
        cursor = work_sheet.cell(len(all_values),2).value
    # backup_row = 1
    # # first round of iteration - setting bound
    # while work_sheet.cell(backup_row,2).value is not None:
    #     if work_sheet.cell(backup_row,1).value != END_CURSOR:
    #         backup_row += 300

    # # second round of iteration - binary search
    # low_bound_row = backup_row - 301
    # mid_bound_row = (backup_row + low_bound_row)//2
    # while mid_bound_row != low_bound_row:
    #     if work_sheet.cell(mid_bound_row,2).value is None:
    #         backup_row = mid_bound_row
    #     else:
    #         low_bound_row = mid_bound_row
    #     mid_bound_row = (backup_row + low_bound_row)//2
    # if work_sheet.cell(mid_bound_row,1).value == END_CURSOR:
    #     backup_row = mid_bound_row
    #     cursor = work_sheet.cell(mid_bound_row,2).value
    return len(all_values), cursor

row_insert, end_cursor = _check_row_insert()
if end_cursor == '':
    backup_variable = {'first': 3000}
else:
    backup_variable = {'first': 1000, "after": end_cursor}
backup_database = query.backup_database_query(EVENT_ID, backup_variable)
nodes = backup_database.json()[DATA][EVENT_PERSON][NODE]
end_cursor = backup_database.json()[DATA][EVENT_PERSON]["pageInfo"][END_CURSOR]

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

work_sheet.update('A' + str(row_insert), END_CURSOR)
work_sheet.update('B' + str(row_insert), end_cursor)
