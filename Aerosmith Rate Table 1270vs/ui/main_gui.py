from tkinter import *
from tkinter import ttk
import unittest.mock as mock

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment, SendFailed

import serial

root = Tk()
root.title("Aerosmith Rate Table 1270vs Control Panel")
root.geometry("500x90")

response_terminator = '/r/n/>/r/n'.encode()

class BoardControl:
    def __init__(self, COM:str, fake:bool = False):
        if fake:
            self.ser = serial.serial_for_url('loop://', timeout=0.05)
        else:
            self.ser = serial.Serial(
                port=COM,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
        self.fake = fake
        self.rate_table = RateTableCommandFactory(self.ser)
        self.current_rate = 0
        
    def setRate(self, rate:int) -> (bool, str):
        jog_acl = self.rate_table.command(ACLCommands.JOG)
        
        try:
            jog_acl.data = rate
        except InvalidArugment as e:
            return (False, f"Rate not set. {e}")
        except SendFailed as e:
            if not self.fake:
                return (False, f"Rate not set. {e}")
            
        self.current_rate = rate
        return (True, "Rate set to " + str(rate))

try:
    boardControl = BoardControl('COM3', fake=True)
except serial.SerialException as e:
    print(e)


def setRate(newRate:int):
    successful, message = boardControl.setRate(newRate)
    if successful:
        current_rate.set(newRate)
    message_to_user.set(message)


mainframe = ttk.Frame(root, padding="5 5 5 5")
mainframe.grid(column=0, row=0, columnspan=1, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

top_row = ttk.Frame(mainframe)
top_row.grid(column=0, row=0, columnspan=1, sticky=(N, E, W))

com_select_button = ttk.Button(top_row, text="COM Port")
com_select_button.grid(column=0, row=0)

manual_test_button = ttk.Button(top_row, text="Manual Test")
manual_test_button.grid(column=1, row=0)



bottom_row = ttk.Frame(mainframe)
bottom_row.grid(column=0, row=2, columnspan=2, sticky=(S, W, E))

message_to_user = StringVar(value="Ready")

message_to_user_label = ttk.Label(bottom_row, textvariable=message_to_user)
message_to_user_label.grid(column=0, row=0, sticky=(W))

exit_button = ttk.Button(bottom_row, text="Exit", command=root.destroy)
exit_button.grid(column=1, row=0, sticky=(E))



middle_row = ttk.Frame(mainframe)
middle_row.grid(column=0, row=1, rowspan=1, sticky=(N, S,))

current_rate = StringVar(value="0")

current_rate_label = ttk.Label(middle_row, text="Current Rate:", padding="40 0 0 0")
current_rate_label.grid(column=1, row=0, sticky=(W))

current_rate_value = ttk.Label(middle_row, textvariable=current_rate, padding="0 0 40 0")
current_rate_value.grid(column=2, row=0, sticky=(W))

change_rate_back_button = ttk.Button(middle_row, text="<", command=lambda: setRate(boardControl.current_rate - 10))
change_rate_back_button.grid(column=0, row=0, sticky=(W))

change_rate_forward_button = ttk.Button(middle_row, text=">", command=lambda: setRate(boardControl.current_rate + 10))
change_rate_forward_button.grid(column=3, row=0, sticky=(W))

root.mainloop()