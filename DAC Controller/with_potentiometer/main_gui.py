import serial
import time
import tkinter as tk
from tkinter import messagebox
import threading


def read_out(arduino: serial.Serial):
    while arduino.is_open:
        print(arduino.readline().decode().strip())

def potentiometer_mode_toggle():
    try:
        arduino.write('POT'.encode())
        messagebox.showinfo('Info', 'Potentiometer mode activated. Set a voltage value to exit this mode.')
    except Exception as e:
        messagebox.showerror('Error', e)

def set_voltage(event=None):
    try:
        voltage = voltage_entry.get()
        if voltage == "":
            arduino.write('POT'.encode())
            messagebox.showinfo('Info', 'Potentiometer mode activated. Enter a voltage value to exit this mode.')
        else:
            voltage = float(voltage)
            if 0 <= voltage <= 4.61:
                from constants import voltage_visual_offset

                voltage *= voltage_visual_offset
                voltage_str = f'{voltage:.2f}'
                arduino.write(voltage_str.encode())

                arduino_output = arduino.readline().decode().strip()
                try:
                    validation_voltage = float(arduino_output)
                    validation_voltage /= voltage_visual_offset
                    messagebox.showinfo('Info', f'Voltage updated to {validation_voltage:.2f} V.')
                except ValueError as e:
                    messagebox.showerror('Error', e)
            else:
                raise ValueError()
    except ValueError:
        messagebox.showerror(
            'Error',
            'Invalid input. Please enter a valid voltage between 0 and 4.61 volts, or click potentiometer mode to use potentiometer.',
        )

def exit_program():
    arduino.close()
    arduino_read_thread.join()
    root.destroy()

# First value is Arduino's serial port identifier
# (e.g., 'COM4' on Windows, '/dev/ttyACM0' or '/dev/ttyUSB0' on Linux)
from constants import arduino_com_val_1, arduino_com_val_2
arduino = None
try:
    arduino = serial.Serial(arduino_com_val_1, 9600)
except Exception:
    try:
        arduino = serial.Serial(arduino_com_val_2, 9600)
    except Exception:
        while arduino == None:
            try:
                arduino = serial.Serial(input(f"Could not locate arduino on {arduino_com_val_1} or {arduino_com_val_2}. Enter in COM[PORT] of arduino"), 9600)
            except Exception:
                pass
time.sleep(2)

root = tk.Tk()
root.title('MCP4725 Voltage Control')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

voltage_label = tk.Label(frame, text='Enter the desired voltage (0 to 4.61) or leave empty to use the potentiometer:')
voltage_label.grid(row=0, column=0, padx=5, pady=5)

voltage_entry = tk.Entry(frame)
voltage_entry.grid(row=0, column=1, padx=5, pady=5)
voltage_entry.bind('<Return>', set_voltage)
voltage_entry.focus_set()

set_voltage_button = tk.Button(frame, text='Click to set voltage (or press enter)', command=set_voltage)
set_voltage_button.grid(row=1, column=0, padx=5, pady=5)

set_potentiometer_mode_button = tk.Button(frame, text='Potentiometer Mode', command=potentiometer_mode_toggle)
set_potentiometer_mode_button.grid(row=2, column=0, padx=5, pady=5)

exit_button = tk.Button(frame, text='Exit', command=exit_program)
exit_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

arduino_read_thread = threading.Thread(None, read_out, 'arduino_out', arduino)
arduino_read_thread.start()
root.mainloop()
