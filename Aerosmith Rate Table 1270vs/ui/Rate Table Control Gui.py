from tkinter import *
from tkinter import ttk
import unittest.mock as mock

from aerosmith.communication import Communication
from aerosmith.commands import RateTableCommandFactory, ACLCommands, Command, InvalidArugment, SendFailed

import serial
from serial.tools import list_ports
from enum import Enum
import threading
import time

response_terminator = '/r/n/>/r/n'.encode()

inital_serial_port = 'COM3'

faked_control = False

class BoardControl:
    enabled = False
    timeout = 0.5
    current_rate_key = 0
    bottom_rate_key = 0
    top_rate_key = 12
    connection_checker_thread: threading.Thread = None
    rates = {
        0: -60,
        1: -50,
        2: -40,
        3: -30,
        4: -20,
        5: -10,
        6: 0,
        7: 10,
        8: 20,
        9: 30,
        10: 40,
        11: 50,
        12: 60
    }
    
    def __init__(self, fake=False):
        self.fake=fake
        pass
        
    def setupSerialConnection(self, COM:str, fake:bool=None) -> (bool, str):
        if fake is not None:
            self.fake=fake
        if not self.fake:
            try:
                self.ser = serial.Serial(
                    port=COM,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=self.timeout
                )
                self.rate_table = RateTableCommandFactory(self.ser)
            except serial.SerialException as e:
                self.enabled = False
                return (False, f"Error setting serial port, board control not available.")
        self.enabled = True
        self.com_port = COM
        self.current_rate_key = 0
        if self.fake:
            return (True, f"Fake serial port set to {COM}, real board control will not work")
        else:
            self.connection_checker_thread = threading.Thread(target=self.connectionChecker)
            self.connection_checker_thread.start()
        return (True, f"Serial port set to {COM}")
    
    def connectionChecker(self):
        while self.enabled:
            comports = list_ports.comports()
            serial_port_exists = False
            for comport in comports:
                if comport.device == self.com_port:
                    serial_port_exists = True
                    break
            if serial_port_exists:
                time.sleep(0.5)
            else:
                self.enabled = False
                self.connection_checker_thread = None
                self.ser.close()
                setMessageToUser('Connection to board lost, please reconnect.')
                return
    
    def getCurrentRate(self) -> (int):
        return self.rates[self.current_rate_key]
        
    def setRate(self, rate_key:int) -> (bool, str):
        if not self.fake:
            jog_acl = self.rate_table.command(ACLCommands.JOG)
            
            try:
                jog_acl.data = self.rates[rate_key]
            except Exception as e:
                return (False, f"Error: {e}")
            
        self.current_rate_key = rate_key
        return (True, "Rate set to " + str(self.getCurrentRate()))
    
    def nextRate(self) -> (bool, str):
        if self.current_rate_key == self.top_rate_key:
            return self.setRate(self.bottom_rate_key)
        else:
            return self.setRate(self.current_rate_key + 1)
            
    def prevRate(self) -> (bool, str):
        if self.current_rate_key == self.bottom_rate_key:
            return self.setRate(self.top_rate_key)
        else:
            return self.setRate(self.current_rate_key - 1)

if __name__ == '__main__':

    # tkinter setup

    root = Tk()
    root.title("Aerosmith Rate Table 1270vs Control Panel")
    root.geometry("700x130")
    root.grid_propagate(True)

    mainframe = ttk.Frame(root, padding="5 5 5 5")
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    mainframe.grid_propagate(True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=2)
    mainframe.rowconfigure(1, weight=2)
    mainframe.rowconfigure(2, weight=0)

    # top row, use to select between modes
    top_row = ttk.Frame(mainframe)
    top_row.grid(column=0, row=0, sticky='new')
    top_row.columnconfigure(0, weight=0)
    top_row.columnconfigure(1, weight=0)
    top_row.columnconfigure(2, weight=1)
    top_row.grid_propagate(True)

    com_select_button = Button(top_row, text="Serial Port Select", command=lambda: selectWindow(Mode.COM_SELECT))
    com_select_button.grid(column=0, row=0, sticky='w')

    manual_test_button = Button(top_row, text="Manual Test", command=lambda: selectWindow(Mode.MANUAL_EDIT))
    manual_test_button.grid(column=1, row=0, sticky='w')
    
    connected_com_port = StringVar(value="None")
    connected_label = ttk.Label(top_row, text="Connected to:")
    connected_label.grid(column=2, row=0, sticky='e')
    connected_label_value = ttk.Label(top_row, textvariable=connected_com_port)
    connected_label_value.grid(column=3, row=0, sticky='e')


    # bottom row, displays messages to user and has an exit button
    bottom_row = ttk.Frame(mainframe)
    bottom_row.grid(column=0, row=2, sticky='sew')
    bottom_row.grid_propagate(True)
    bottom_row.columnconfigure(0, weight=1)
    bottom_row.columnconfigure(1, weight=1)

    message_to_user = StringVar(value="Ready")

    message_to_user_label = ttk.Label(bottom_row, textvariable=message_to_user)
    message_to_user_label.grid(column=0, row=0, sticky='w')
    message_to_user_label.grid_propagate(True)

    exit_button = ttk.Button(bottom_row, text="Exit", command=root.destroy)
    exit_button.grid(column=1, row=0, sticky='e')

    # now create middle windows, these will be the main functions of the application

    # change com port window

    middle_row_com_select = ttk.Frame(mainframe)
    middle_row_com_select.grid(column=0, row=1, sticky='ew')
    middle_row_com_select.grid_propagate(True)
    middle_row_com_select.columnconfigure(0, weight=1)
    middle_row_com_select.columnconfigure(1, weight=1)
    middle_row_com_select.columnconfigure(2, weight=1)
    middle_row_com_select.columnconfigure(3, weight=1)
    
    com_port_refresh_button = ttk.Button(middle_row_com_select, text="Refresh", command=lambda: createComOptionButtons(no_com_ports_found_frame, com_ports_found_frame))
    com_port_refresh_button.grid(column=1, row=0)

    no_com_ports_found_frame = ttk.Frame(middle_row_com_select, padding="0 0 40 0")
    com_ports_found_frame = ttk.Frame(middle_row_com_select, padding="0 0 40 0")

    def createComOptionButtons(no_com_ports_found_frame:ttk.Frame, com_ports_found_frame:ttk.Frame):
        comports = list_ports.comports()
        
        if len(comports) == 0:
            no_com_ports_found_frame.grid(column=0, row=0, sticky='w')
            if com_ports_found_frame is not None:
                com_ports_found_frame.grid_forget()
                
            no_com_ports_label = ttk.Label(no_com_ports_found_frame, text="No Serial Devices Found!")
            no_com_ports_label.grid(column=0, row=0)
            if faked_control:
                comport_button = ttk.Button(no_com_ports_found_frame, text=f'Fake COM Port ({inital_serial_port})', command=lambda: setupBoardControl(inital_serial_port))
                comport_button.grid(column=0, row=1, sticky=(W))
        else:
            com_ports_found_frame.grid(column=0, row=0, sticky='w')
            if no_com_ports_found_frame is not None:
                no_com_ports_found_frame.grid_forget()
                
            com_ports_found_frame.grid_propagate(True)
                
            com_port_buttons_label = ttk.Label(com_ports_found_frame, text="Select from available serial devices:")
            com_port_buttons_label.grid(column=0, row=0, sticky=(W))
            for (index, comport) in enumerate(comports):
                comport_button = ttk.Button(com_ports_found_frame, text=comport.description, command=lambda: setupBoardControl(comport.device))
                comport_button.grid(column=0, row=index + 1, sticky=(W))


    # manual rate change window

    middle_row_manual_edit = ttk.Frame(mainframe)
    middle_row_manual_edit.grid(column=0, row=1, sticky='nsew')
    middle_row_manual_edit.grid_propagate(True)

    current_rate = StringVar(value="0")

    current_rate_label = ttk.Label(middle_row_manual_edit, text="Current Rate:", padding="40 0 0 0")
    current_rate_label.grid(column=1, row=0, sticky=(W))

    current_rate_value = ttk.Label(middle_row_manual_edit, textvariable=current_rate, padding="0 0 40 0")
    current_rate_value.grid(column=2, row=0, sticky=(W))

    change_rate_back_button = ttk.Button(middle_row_manual_edit, text="-10", command=lambda: prevBoardRate())
    change_rate_back_button.grid(column=0, row=0, sticky=(W))

    change_rate_forward_button = ttk.Button(middle_row_manual_edit, text="+10", command=lambda: nextBoardRate())
    change_rate_forward_button.grid(column=3, row=0, sticky=(W))


    class Mode(Enum):
        COM_SELECT = 'com_select'
        MANUAL_EDIT = 'manual_edit'

    objects_for_mode:dict[Mode, dict[str, any]] = {
        Mode.COM_SELECT : {
            "window" : middle_row_com_select,
            'button' : com_select_button,
            'startup_func' : lambda: createComOptionButtons(no_com_ports_found_frame, com_ports_found_frame)
        },
        Mode.MANUAL_EDIT : {
            "window" : middle_row_manual_edit,
            'button' : manual_test_button,
            'startup_func' : None
        }
    }

    def selectWindow(window:Mode):
        for key in objects_for_mode:
            if key != window:
                objects_for_mode[key]['button'].configure(bg="SystemButtonFace")
                objects_for_mode[key]['window'].grid_forget()
            else:
                objects_for_mode[key]['button'].configure(bg="white")
                objects_for_mode[key]['window'].grid(column=0, row=1, sticky='ns')
                if objects_for_mode[key]['startup_func'] is not None:
                    objects_for_mode[key]['startup_func']()

    selectWindow(Mode.COM_SELECT)
    
    # create board control object
    
    boardControl = BoardControl(fake=faked_control)
        
    # create functions to set board values and integrate with tkinter window
    
    def getBoardControlObject():
        return boardControl
    
    def setMessageToUser(msg: str):
        message_to_user.set(msg)

    def nextBoardRate():
        successful, message = boardControl.nextRate()
        if successful:
            current_rate.set(boardControl.getCurrentRate())
        message_to_user.set(message)
        
    def prevBoardRate():
        successful, message = boardControl.prevRate()
        if successful:
            current_rate.set(boardControl.getCurrentRate())
        message_to_user.set(message)
        
    def setupBoardControl(newPort:str):
        successful, message = boardControl.setupSerialConnection(newPort)
        if successful:
            manual_test_button['state'] = 'normal'
            connected_com_port.set(newPort)
        else:
            manual_test_button['state'] = 'disabled'
            connected_com_port.set('None')
        message_to_user.set(message)
        
    setupBoardControl(inital_serial_port)


    root.mainloop()