import json

# Step 1: Read the JSON file
with open('products.json', 'r') as file:
    products_data = json.load(file)

# Step 2: Parse JSON data into a dictionary
products_dict = {product['id']: product['name'] for product in products_data}

# Step 3: Infinite loop to keep the program running
while True:
    # Step 4: Get scanned ID from gm66 (barcode scanner)
    scanned_id = input("Scan the product ID from gm66 (or type 'exit' to quit): ")

    # Step 5: Check if the user wants to exit
    if scanned_id.lower() == 'exit':
        print("Exiting the program...")
        break  # Exit the loop and end the program

    # Step 6: Compare scanned ID with the dictionary
    if scanned_id in products_dict:
        product_name = products_dict[scanned_id]
        print(f"Scanned ID {scanned_id} , product name: {product_name}")
    else:
        print(f"No product found for ID {scanned_id}")
