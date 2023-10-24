from tkinter import *
from tkinter import ttk

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment

import serial

root = Tk()
root.title("Aerosmith Rate Table 1270vs Control Panel")

class BoardControl:
    def __init__(self, COM:str):
        self.ser = serial.Serial(
            port=COM,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.rate_table = RateTableCommandFactory(self.ser)

    def test_valid_response(self) -> bool:
            jog_acl = self.rate_table.command(ACLCommands.JOG)

            jog_acl.data = 60

            response = self.ser.read(5)
          
            expected_response = b'JOG60'
    
            return expected_response == response

boardControl = BoardControl('COM3')





mainframe = ttk.Frame(root, padding="5 5 5 5")
mainframe.grid(column=0, row=0, columnspan=1, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

top_row = ttk.Frame(mainframe)
top_row.grid(column=0, row=0, columnspan=1, sticky=(N, W))

com_select_button = ttk.Button(top_row, text="COM Port")
com_select_button.grid(column=0, row=0)

manual_test_button = ttk.Button(top_row, text="Manual Test")
manual_test_button.grid(column=1, row=0)

middle_row = ttk.Frame(mainframe)
middle_row.grid(column=0, row=1, rowspan=1)

bottom_row = ttk.Frame(mainframe)
bottom_row.grid(column=0, row=2, columnspan=2, sticky=(S, E))

exit_button = ttk.Button(bottom_row, text="Exit", command=root.destroy)
exit_button.grid(column=1, row=0, sticky=(E))

root.mainloop()