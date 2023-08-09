import pathlib
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
