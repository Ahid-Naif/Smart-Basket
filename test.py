import sys
import serial

# Configure the serial port
serial_port = '/dev/ttyAMA0'  # Adjust this based on your barcode scanner's serial port
baud_rate = 9600  # Adjust this based on your barcode scanner's baud rate
timeout = 1  # Timeout in seconds

# Open the serial port
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
except serial.SerialException as e:
    print("Error opening serial port:", e)
    sys.exit(1)

print("Barcode scanner test (Press Ctrl+C to exit)")

try:
    while True:
        # Read a line from the serial port (barcode scanner)
        barcode = ser.readline().strip().decode('utf-8')
        if barcode:
            print("Scanned barcode:", barcode)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Close the serial port
    ser.close()
