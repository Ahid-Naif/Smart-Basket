import serial

# Open serial port
ser = serial.Serial('/dev/ttyS0', 9600)  # Change '/dev/ttyUSB0' to your serial port

# Send command to request data
ser.write(b'READ_DATA\n')

# Read response
response = ser.readline()

# Parse response (assuming response is in ASCII format)
data = response.decode().strip()

# Close serial port
ser.close()

# Process the data as needed
print("Data from GM66 sensor:", data)
