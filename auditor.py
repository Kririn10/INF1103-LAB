inventory = 0
failed = 0

print("Smart Inventory Auditor")
print("Type 'quit' to exit\n")

while True:
    inputs = input ("Enter Stock Quantity: ")

    if input == "quit":
        break

    if not inputs.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed += 1
        continue

    stock_quantity = int(inputs)
    inventory += stock_quantity
    print(f"Total: {inventory} units\n")

    if inventory > 500:
        print("Inventory exceeds 500 units. Please review stock levels.\n")
        break

    print("\n" + "="*40)
    print(f"Total Units: {inventory}")
    print(f"Failed Entries: {failed}")
    print("="*40)