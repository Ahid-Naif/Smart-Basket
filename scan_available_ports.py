import glob

def find_serial_ports():
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

available_ports = find_serial_ports()
print("Available serial ports:", available_ports)
