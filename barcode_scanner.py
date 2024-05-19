import json
import sys
import serial

# Step 1: Read the JSON file
with open('products.json', 'r') as file:
    products_data = json.load(file)

# Step 2: Parse JSON data into a dictionary
products_dict = {product['id']: {'name': product['name'], 'price': product['price']} for product in products_data}

# Configure the serial port
serial_port = '/dev/ttyACM0'  # Adjust this based on your barcode scanner's serial port
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
        scanned_id = ser.readline().strip().decode('utf-8')
        if scanned_id:
            # Check if the user wants to exit
            if scanned_id.lower() == 'exit':
                print("Exiting the program...")
                break  # Exit the loop and end the program
            
            # Compare scanned ID with the dictionary
            if scanned_id in products_dict:
                product_info = products_dict[scanned_id]
                product_name = product_info['name']
                product_price = product_info['price']
                print(f"Scanned ID {scanned_id}, product name: {product_name}, price: {product_price}")
            else:
                print(f"No product found for ID {scanned_id}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Close the serial port
    ser.close()
