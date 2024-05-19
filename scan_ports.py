import serial.tools.list_ports

# Get a list of available serial ports
ports = serial.tools.list_ports.comports()

# Print information about each port
for port in ports:
    print(port)
