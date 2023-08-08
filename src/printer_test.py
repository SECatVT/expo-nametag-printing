import pathlib
import PySimpleGUI as sg
from win32com.client import Dispatch


printer = Dispatch("Dymo.DymoAddIn")
print(printer.GetDymoPrinters())

label_path = pathlib.Path("./student_badge.label")
printer.SelectPrinter(printer.GetDymoPrinters())
printer.Open(label_path)
label = Dispatch("Dymo.DymoLabels")

printer.StartPrintJob()
printer.Print(1, False)
printer.EndPrintJob()

# sg.theme("Reds")

# font = ("Courier", 24)
# sg.set_options(font=font)

# layout = [
#     [sg.Text("Please either scan your Hokie ID")],
#     [sg.Text("Hokie ID", size=(15, 1)), sg.InputText(do_not_clear=False)],
#     [sg.Text("or enter your First Name, Last Name, Year, and Major")],
#     [sg.Text("First Name", size=(15, 1)), sg.InputText(do_not_clear=False)],
#     [sg.Text("Last Name", size=(15, 1)), sg.InputText(do_not_clear=False)],
#     [sg.Text("PID", size=(15, 1)), sg.InputText(do_not_clear=False)],
#     [sg.Submit()]
# ]

# window = sg.Window("Engineering Expo", layout, size=(1200, 600))

# while True:

#     event, values = window.read()
#     print("event: {}".format(event))
#     print("values: {}".format(values))


