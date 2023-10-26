import time
import serial

# ser = serial.Serial(
#     port='/dev/ttyUSB1',
#     baudrate=9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS
# )


# Windows 
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# ser.write(b'HOM\r\n')

ser.write(b'JOG60\r')

response_terminator = b'\r\n>\r\n'

response = ser.read_until(expected=response_terminator)
print(response)

def receive():
  ser.send
  response = ser.read_until(expected=response_terminator)
  print( )

