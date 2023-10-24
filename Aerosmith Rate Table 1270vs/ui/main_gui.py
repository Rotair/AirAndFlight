from tkinter import *
from tkinter import ttk

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment

import serial

root = Tk()
root.title("Aerosmith Rate Table 1270vs Control Panel")

response_terminator = '/r/n/>/r/n'.encode()

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
        self.current_rate = 0
        
    def setRate(self, rate:int):
        jog_acl = self.rate_table.command(ACLCommands.JOG)

        jog_acl.data = rate
        
        expected_response = f'JOG{rate}'.encode()

        response = self.ser.read_until(expected=response_terminator)

        return expected_response == response

try:
    boardControl = BoardControl('COM3')
except serial.SerialException as e:
    print(e)




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



bottom_row = ttk.Frame(mainframe)
bottom_row.grid(column=0, row=2, columnspan=2, sticky=(S, E))

exit_button = ttk.Button(bottom_row, text="Exit", command=root.destroy)
exit_button.grid(column=1, row=0, sticky=(E))



middle_row = ttk.Frame(mainframe)
middle_row.grid(column=0, row=1, rowspan=1)

current_rate = StringVar(value="0")

current_rate_label = ttk.Label(middle_row, text="Current Rate:")
current_rate_label.grid(column=0, row=0, sticky=(W))

current_rate_value = ttk.Label(middle_row, textvariable=current_rate)
current_rate_value.grid(column=1, row=0, sticky=(W))

root.mainloop()