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

ser.write(b'JOG60\r\n')

while 1:
  tdata = ser.read(5)           # Wait forever for anything
  print(tdata)
