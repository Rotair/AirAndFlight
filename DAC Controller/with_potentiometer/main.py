import serial
import time
import threading

def read_out(arduino):
    while True:
        print(arduino.readline().decode().strip())

def main():
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
    threading.Thread(None, read_out, 'arduino_out', arduino)
    time.sleep(2)  # Give the connection some time to establish

    while True:
        try:
            user_input = input("Enter the desired voltage (0 to 4.61) or type 'POT' to use the potentiometer (type 'exit' to quit): ")
            if user_input == "":
                continue
            if user_input.lower() == "exit":
                break
            if user_input.lower() == "pot":
                arduino.write("POT".encode())
                print("Potentiometer mode activated. Send a voltage value to exit this mode.")
            else:
                voltage = float(user_input)
                if 0 <= voltage <= 4.61:
                    from constants import voltage_visual_offset
                    voltage *= voltage_visual_offset
                    voltage_str = f'{voltage:.2f}'
                    arduino.write(voltage_str.encode())
                    arduino_output = arduino.readline().decode().strip()
                    try:
                        validation_voltage = float(arduino_output)
                        validation_voltage /= voltage_visual_offset
                        print(f"Voltage updated to {validation_voltage:.2f} V.")
                    except ValueError:
                        print(f"{arduino_output}")
                else:
                    raise ValueError()
        except ValueError:
            print("Invalid input. Please enter a valid voltage between 0 and 4.61 volts, 'POT', or 'exit'.")
        except KeyboardInterrupt:
            print("\nExitting...")
            break

    arduino.close()

if __name__ == "__main__":
    main()
