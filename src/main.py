from datetime import datetime
import pathlib
import time
import warnings

import gspread
import PySimpleGUI as sg
from win32com.client import Dispatch

import query
from config import GeneralConfig, NameTagConfig, QueryConfig

# There is a messy warning from google sheet api for unknown reason
warnings.filterwarnings("ignore", message=".*Worksheet.update")

# Globals
DATA = GeneralConfig.DATA
EVENT_PERSON = GeneralConfig.EVENT_PERSON
NODE = GeneralConfig.NODE
FIRST_NAME = GeneralConfig.FIRST_NAME
LAST_NAME = GeneralConfig.LAST_NAME
EMAIL = GeneralConfig.EMAIL
PHONE_NUMBER = GeneralConfig.PHONE_NUMBER
DEFINITION = GeneralConfig.DEFINITION
TRANSLATION = GeneralConfig.TRANSLATION

EVENT_ID = QueryConfig.event_id
DEFAULT_FONT = ("Calibri", 22)
INPUT_FONT = ("Courier", 20)
TEXT_SIZE = (15, 1)

# verify event
event = query.event_query(EVENT_ID).json()
print(event['data']['event']['title'] + '\n')

# set up simple GUI
sg.theme("SystemDefaultForReal")
sg.set_options(font=DEFAULT_FONT)

# set up Google Sheet Log
service_account = gspread.service_account(filename=GeneralConfig.GOOGLE_LOG_KEYFILE_NAME)
log_sheet = service_account.open(GeneralConfig.GOOGLE_LOG_SHEET_NAME)
work_sheet = log_sheet.worksheet(GeneralConfig.WORKSHEET_NAME)
end_cell = work_sheet.find(GeneralConfig.GOOGLE_LOG_END_TOKEN)

# private utility functions
def _text_creater(text_content):
    return sg.Text(text=text_content, size=TEXT_SIZE, font=INPUT_FONT)

def _cell_range(row):
    return "A" + str(row) + ":I" + str(row)

def _check_row_insert(check_cell):
    backup_row = 1
    if check_cell is None:
        while not work_sheet.cell(backup_row,1).value is None:
            backup_row += 1
        return backup_row
    else:
        return check_cell.row

def _printer_set_up():
    try:
        dymo_printer = Dispatch("Dymo.DymoAddIn")
        print(dymo_printer.GetDymoPrinters())
        label_path = pathlib.Path("./src/label/student_badge_v3.label")
        dymo_printer.SelectPrinter(dymo_printer.GetDymoPrinters())
        dymo_printer.Open(label_path)
        dymo_label = Dispatch("Dymo.DymoLabels")

    except Exception as dymo_err:
        dymo_printer = None
        dymo_label = None
        print("No Printer Found ", dymo_err)

    return dymo_printer, dymo_label

# printer dispatch
printer, label = _printer_set_up()

# design the GUI
input1 = [_text_creater("Badge Register ID"), sg.InputText(do_not_clear=False, key="BRID")]
input2 = [_text_creater("VT PID"), sg.InputText(do_not_clear=False, key="PID")]

backup_fn = [_text_creater("First Name"), sg.InputText(do_not_clear=False, key="FN")]
backup_ln = [_text_creater("Last Name"), sg.InputText(do_not_clear=False, key="LN")]
backup_major = [_text_creater("Major"),
            sg.Combo(list(NameTagConfig.majors), default_value="Aerospace Engineering", key="MJ")]
backup_year = [_text_creater("Year"),
            sg.Combo(list(NameTagConfig.years), default_value="Freshman", key="YR")]
backup_r_id = [_text_creater("Registration ID"),
             sg.InputText(do_not_clear=False, default_text="123456", key="RID")]
backup_email = [_text_creater("VT Email"),
             sg.InputText(do_not_clear=False, default_text="hokie@vt.edu", key="VTEML")]
backup_phone = [_text_creater("Phone Number"),
             sg.InputText(do_not_clear=False, default_text="(123)-456-7890", key="PHONE")]
backup = [backup_fn, backup_ln, backup_major, backup_year, backup_r_id, backup_email, backup_phone]

layout = [
    [sg.Text("Option 1 - Scan QR code from SwapCard")], input1,
    [sg.Text("Option 2 - Input VT PID")], input2,
    [sg.Checkbox("Manual Input Backup (enable by checkbox)", key="MIConfirm")], *backup,
    [sg.Submit(), sg.Text("Please only exit this program by closing the window.",text_color="red")]
]
window = sg.Window(str(GeneralConfig.CURRENT_YEAR) + " Engineering Expo Student Nametag Printing",
                   layout, size=(2400, 1300))

# confirm inserting row number
row_insert = _check_row_insert(end_cell)
# record start time as timestamp for a previous event
timePrev = time.time()

while True:
    event, inputs = window.read()
    print(event, inputs)
    if time.time() - timePrev < 3:
        continue
    timePrev = time.time()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    first_name, last_name, major, year, regis_id = '', '', '', '', ''
    email, phone_number = '', ''

    # Parse information from SwapCard API queries
    if not inputs["MIConfirm"]:
        # Option 1 - Search by registration ID
        if not inputs['BRID'] == '':
            people_filter = {'qrCodes': inputs['BRID']}
            person = query.people_filter_query(EVENT_ID, people_filter)

            print(person.json())

            if person.json()[DATA][EVENT_PERSON][NODE] == []:
                print("Warning - Invaild registration ID. EventPerson can not be resolved.")
                continue

        # Option 2 - Search by PID or VT email
        elif not inputs['PID'] == '':
            # people_search = inputs['PID']
            pid = inputs['PID']
            if not '@' in pid:
                pid += '@vt.edu'
            people_filter = {'emails': pid}
            person = query.people_filter_query(EVENT_ID, people_filter)

            print(person.json())

            if person.json()[DATA][EVENT_PERSON][NODE] == []:
                print("Warning - Invaild PID/VT email. EventPerson can not be resolved.")
                continue

        else:
            print("Warning - No Input Detected")
            continue

        eventPerson = person.json()[DATA][EVENT_PERSON][NODE][0]
        # assign from the query result
        first_name = eventPerson[FIRST_NAME]
        last_name = eventPerson[LAST_NAME]
        email = eventPerson[EMAIL]
        if not eventPerson[PHONE_NUMBER] == []:
            phone_number = eventPerson[PHONE_NUMBER][0]["number"]

        # Fetch major & year from fields - only the first major is recorded
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

            # if not inputs["OWGLConfirm"] and DEFINITION in field and field[DEFINITION][TRANSLATION][0]['name'] == 'Graduation Year':
            #     # SelectField query structure
            #     graduation_time = field[TRANSLATION][0]['value']
            #     if not graduation_time == "None" or not graduation_time == "Other":
            #         graduation_year = int(graduation_time[-4:])
            #         if "Spring" in graduation_time:
            #             graduation_year -= 1
            #         year = NameTagConfig.years[3 + GeneralConfig.CURRENT_YEAR - graduation_year]

            #     else: year = graduation_time

        badges = eventPerson['withEvent']['badges']
        regis_id = badges[0]['barcode']

    # Parse, well barely, from manual inputs
    else:
        first_name, last_name, major, year, regis_id, email, phone_number = \
            [inputs[k] for k in ('FN', 'LN', 'MJ', 'YR', 'RID','VTEML','PHONE')]

    # Special cases assignments
    if "freshman" in year.lower():
        major = NameTagConfig.majors[NameTagConfig.major_index["GE"]]

    if "construction" in major.lower() and "management" in major.lower():
        major = NameTagConfig.majors[NameTagConfig.major_index["CEM"]]

    if "computer" in major.lower() and "science" in major.lower():
        major = NameTagConfig.majors[NameTagConfig.major_index["CS"]]

    if "building" in major.lower() and "construction" in major.lower():
        major = NameTagConfig.majors[NameTagConfig.major_index["BUC"]]

    # Terminal output for student info
    print('#'*10 + ' NameTag Info ' + '#'*10 +
          f"\n{'First Name:':<20}{first_name}" + f"\n{'Last Name:':<20}{last_name}" +
          f"\n{'Major:':<20}{major}" + f"\n{'Year:':<20}{year}" +
          f"\n{'Registration ID:':<20}{regis_id}\n")

    # Log the query or inputed student record to a pre-established Google Sheet
    now_datetime = datetime.now()
    now_date = now_datetime.strftime("%m/%d/%Y")
    now_time = now_datetime.strftime("%H:%M:%S")
    organized_data = [[now_date, now_time, first_name, last_name, major, year, regis_id, email, phone_number]]
    work_sheet.update(_cell_range(row_insert), organized_data)

    # Terminal output for Google Sheet log Confirmation
    print('#'*10 + ' Query Logged ' + '#'*10 + '\n')

    if printer is not None and label is not None:
        try:
            # Print job
            label.SetField("fn", first_name)
            label.SetField("ln", last_name)
            label.SetField("y", year)
            label.SetField("m", major)
            label.SetField("BARCODE", regis_id)

            printer.StartPrintJob()
            printer.Print(1, False)
            printer.EndPrintJob()

            print("\nPrint Success\n")

        except Exception as err:
            printer.EndPrintJob()
            print("\nPrinting Not Resolved - ", err, "\n")

    # Index increment
    row_insert += 1

work_sheet.update('A' + str(row_insert), GeneralConfig.GOOGLE_LOG_END_TOKEN)
if printer is not None:
    printer.EndPrintJob()
window.close()
