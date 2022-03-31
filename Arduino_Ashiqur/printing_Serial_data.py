# Import the library
import serial

# Try to connect to the port
try:
    device = serial.Serial("COM5", 9600)
except:
    print("Failed to connect")
    exit()

# Read data and print it to terminal... until you stop the program
while True:
    line = device.readline()
    line = str(line)
    line.replace('\r\n', '')
    print(line)