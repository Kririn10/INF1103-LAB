total_inventory = 0
failed_entries = 0

print("SMART INVENTORY AUDITOR")
print("Type 'quit' to exit\n")

while True:
    user_input = input ("Enter Stock Quantity: ")

    if user_input == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    stock_quantity = int(user_input)
    total_inventory += stock_quantity
    print(f"✓ Total: {total_inventory} units\n")

    if total_inventory > 500:
        print(" Warning: Inventory exceeds 500 units. Please review stock levels.\n")
        break

    print("\n" + "="*40)
    print(f"Total Units: {total_inventory}")
    print(f"Failed Entries: {failed_entries}")
    print("="*40)