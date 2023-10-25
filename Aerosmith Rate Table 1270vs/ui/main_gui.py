from tkinter import *
from tkinter import ttk
import unittest.mock as mock

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment, SendFailed

import serial
import serial.tools.list_ports

[comport.device for comport in serial.tools.list_ports.comports()]


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
        self.com_port = COM
        self.fake = fake
        self.rate_table = RateTableCommandFactory(self.ser)
        self.current_rate = 0
        
    def setSerialPort(self, COM:str) -> (bool, str):
        if not self.fake:
            try:
                self.ser.close()
                self.ser = serial.Serial(
                    port=COM,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                )
            except Exception as e:
                return (False, f"Serial port not set. {e}")
        self.com_port = COM
        return (True, "Serial port set to " + COM)
        
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


def setBoardRate(newRate:int):
    successful, message = boardControl.setRate(newRate)
    if successful:
        current_rate.set(newRate)
    message_to_user.set(message)
    
def setBoardSerialPort(newPort:str):
    successful, message = boardControl.setSerialPort(newPort)
    if successful:
        com_port.set(newPort)
    message_to_user.set(message)

# tkinter setup

# styles = Style()
# styles.configure("highlighted_button", background="white")
# styles.configure("regular_button", background="SystemButtonFace")

root = Tk()
root.title("Aerosmith Rate Table 1270vs Control Panel")
root.geometry("600x130")

mainframe = ttk.Frame(root, padding="5 5 5 5")
mainframe.grid(column=0, row=0, rowspan=3, columnspan=1, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=2)
mainframe.rowconfigure(1, weight=2)
mainframe.rowconfigure(2, weight=0)

# top row, use to select between modes
top_row = ttk.Frame(mainframe)
top_row.grid(column=0, row=0, columnspan=1, sticky='new')

com_select_button = Button(top_row, text="COM Port", command=lambda: selectWindow('com_select'))
com_select_button.grid(column=0, row=0)

manual_test_button = Button(top_row, text="Manual Test", command=lambda: selectWindow('manual_edit'))
manual_test_button.grid(column=1, row=0)


# bottom row, displays messages to user and has an exit button
bottom_row = ttk.Frame(mainframe)
bottom_row.grid(column=0, row=2, columnspan=1, sticky='sew')
bottom_row.columnconfigure(0, weight=1)
bottom_row.columnconfigure(1, weight=1)

message_to_user = StringVar(value="Ready")

message_to_user_label = ttk.Label(bottom_row, textvariable=message_to_user)
message_to_user_label.grid(column=0, row=0, sticky='w')

exit_button = ttk.Button(bottom_row, text="Exit", command=root.destroy)
exit_button.grid(column=1, row=0, sticky='e')

# now create middle windows, these will be the main functions of the application

# change com port window

middle_row_com_select = Frame(mainframe)
middle_row_com_select.grid(column=0, row=1, sticky='ew')
middle_row_com_select.columnconfigure(0, weight=2)
middle_row_com_select.columnconfigure(1, weight=0)

com_port = StringVar(value=boardControl.com_port)

com_port_label = ttk.Label(middle_row_com_select, text="Current COM Port:", padding="200 0 0 0")
com_port_label.grid(column=0, row=0, sticky='w')

com_port_value = ttk.Label(middle_row_com_select, textvariable=com_port)
com_port_value.grid(column=1, row=0, sticky='e')

no_com_ports_label = None
com_port_buttons = None

def createComOptionButtons(no_com_ports_label, com_port_buttons):
    com_port_buttons = ttk.Frame(middle_row_com_select)
    com_port_buttons.grid(column=0, row=0, sticky=(W))
    
    com_port_buttons_label = ttk.Label(com_port_buttons, text="Select from available ports:")
    com_port_buttons_label.grid(column=0, row=0, sticky=(W))
    
    comports = serial.tools.list_ports.comports()
    
    if len(comports) == 0:
        if com_port_buttons is not None:
            com_port_buttons.grid_forget()
        no_com_ports_label = ttk.Label(com_port_buttons, text="No COM Ports Found")
        no_com_ports_label.grid(column=0, row=0, sticky=(W))
    else:
        if no_com_ports_label is not None:
            no_com_ports_label.grid_forget()
        for comport in serial.tools.list_ports.comports():
            comport_button = ttk.Button(com_port_buttons, text=comport.device, command=lambda: setBoardSerialPort(comport.device))
            comport_button.grid(column=0, row=serial.tools.list_ports.comports().index(comport) + 1, sticky=(W))
    
    return com_port_buttons


# manual rate change window

middle_row_manual_edit = Frame(mainframe)
middle_row_manual_edit.grid(column=0, row=1, columnspan=1, sticky='ns')

current_rate = StringVar(value="0")

current_rate_label = ttk.Label(middle_row_manual_edit, text="Current Rate:", padding="40 0 0 0")
current_rate_label.grid(column=1, row=0, sticky=(W))

current_rate_value = ttk.Label(middle_row_manual_edit, textvariable=current_rate, padding="0 0 40 0")
current_rate_value.grid(column=2, row=0, sticky=(W))

change_rate_back_button = ttk.Button(middle_row_manual_edit, text="<", command=lambda: setBoardRate(boardControl.current_rate - 10))
change_rate_back_button.grid(column=0, row=0, sticky=(W))

change_rate_forward_button = ttk.Button(middle_row_manual_edit, text=">", command=lambda: setBoardRate(boardControl.current_rate + 10))
change_rate_forward_button.grid(column=3, row=0, sticky=(W))

middle_windows = {
    "com_select" : {
        "window" : middle_row_com_select,
        'button' : com_select_button,
        'startup_func' : lambda: createComOptionButtons(no_com_ports_label, com_port_buttons)
    },
    "manual_edit" : {
        "window" : middle_row_manual_edit,
        'button' : manual_test_button,
        'startup_func' : None
    }
}

def selectWindow(window:str):
    for key in middle_windows:
        if key != window:
            middle_windows[key]['button'].configure(bg="SystemButtonFace")
            middle_windows[key]['window'].grid_forget()
        else:
            middle_windows[key]['button'].configure(bg="white")
            middle_windows[key]['window'].grid(column=0, row=1, columnspan=1, sticky='ns')
            if middle_windows[key]['startup_func'] is not None:
                middle_windows[key]['startup_func']()

selectWindow('com_select')


root.mainloop()