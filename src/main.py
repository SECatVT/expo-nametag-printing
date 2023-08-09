import PySimpleGUI as sg
from win32com.client import Dispatch

import query
from config import GeneralConfig, NameTagConfig, QueryConfig

# verify event
EVENT_ID = QueryConfig.event_id
event = query.event_query(EVENT_ID).json()
print(event['data']['event']['title'])

# set up simple GUI
sg.theme("SystemDefaultForReal")
HEADER_FONT = ("Calibri", 22)
INPUT_FONT = ("Courier", 20)
TEXT_SIZE = (15, 1)
sg.set_options(font=HEADER_FONT)

def textCreater(text_content):
    return sg.Text(text=text_content, size=TEXT_SIZE, font=INPUT_FONT)

# design the GUI
input1 = [textCreater("Badge Register ID"), sg.InputText(do_not_clear=False, key="BRID")]
input2 = [textCreater("VT PID"), sg.InputText(do_not_clear=False, key="PID")]

backup_fn = [textCreater("First Name"), sg.InputText(do_not_clear=False, key="FN")]
backup_ln = [textCreater("Last Name"), sg.InputText(do_not_clear=False, key="LN")]
backup_major = [textCreater("Major"),
            sg.Combo(list(NameTagConfig.majors), default_value="Aerospace Engineering", key="MJ")]
backup_year = [textCreater("Year"),
            sg.Combo(list(NameTagConfig.years), default_value="Freshman", key="YR")]
backup_r_id = [textCreater("Registration ID"),
             sg.InputText(do_not_clear=False, default_text="123456", key="RID")]
backup = [backup_fn, backup_ln, backup_major, backup_year, backup_r_id]

layout = [
    [sg.Text("Option 1 - Scan QR code from SwapCard")], input1,
    [sg.Text("Option 2 - Input VT PID")], input2,
    [sg.Checkbox("Manual Input Backup (enable by checking the box)", key="MIConfirm")], *backup,
    [sg.Submit()]
]
window = sg.Window("Engineering Expo", layout, size=(800, 600))

while True:
    event, inputs = window.read()
    print(event, inputs)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    first_name, last_name, major, year, regis_id = '', '', '', '', ''

    if not inputs["MIConfirm"]:
        if not inputs['BRID'] == '':
            people_filter = {'qrCodes': inputs['BRID']}
            person = query.people_filter_query(EVENT_ID, people_filter)

            if person.json()['data']['eventPerson']['nodes'] == []:
                print("Warning - Invaild registration ID. EventPerson can not be resolved.")
                continue

        elif not inputs['PID'] == '':
            people_search = inputs['PID']
            if not '@' in people_search:
                people_search += '@vt.edu'
            person = query.people_search_query(EVENT_ID, people_search)

            if person.json()['data']['eventPerson']['nodes'] == []:
                print("Warning - Invaild PID/VT email. EventPerson can not be resolved.")
                continue

        else:
            print("Warning - No Input Detected")
            continue

        eventPerson = person.json()['data']['eventPerson']['nodes'][0]
        # assign from the query result
        first_name = eventPerson['firstName']
        last_name = eventPerson['lastName']

        fields = eventPerson['withEvent']['fields']
        first_major_flag = True
        for field in fields:
            if first_major_flag and 'definition' in field and field['definition']['translations'][0]['name'] == 'Major':
                # MultipleSelectField query structure
                major = field['translations'][0]['value']
                first_major_flag = False

            if 'definition' in field and field['definition']['translations'][0]['name'] == 'Graduation Year':
                # SelectField query structure
                graduation_time = field['translations'][0]['value']
                if not graduation_time == "None" or not graduation_time == "Other":
                    graduation_year = int(graduation_time[-4:])
                    year = NameTagConfig.years[4 + GeneralConfig.CURRENT_YEAR - graduation_year]

                else: year = graduation_time

        badges = eventPerson['withEvent']['badges']
        regis_id = badges[0]['barcode']

    else:
        first_name, last_name, major, year, regis_id = [inputs[k] for k in ('FN', 'LN', 'MJ', 'YR', 'RID')]

    print('#'*10 + ' NameTag Info ' + '#'*10 +
          f"\n{'First Name:':<20}{first_name}" + f"\n{'Last Name:':<20}{last_name}" +
          f"\n{'Major:':<20}{major}" + f"\n{'Year:':<20}{year}" + 
          f"\n{'Registration ID:':<20}{regis_id}\n")

window.close()
