

def get_valid_input():
    inputs = input("Enter Stock Quantity: ").strip()
    if inputs == "quit":
        return "quit"
    elif not inputs.isdigit():
         print("Invalid input. Please enter a valid number.")
         return None
    else:
        return inputs

def process_delivery(current_total, new_value):
    return int(current_total) + int(new_value)

def calculate_tax(amount):
    return int(amount) * 0.10

def generate_report(total_units, failed_attempts):
    print("\n" + "=" * 40)
    print(f"Total Units: {total_units}")
    print(f"Failed Entries: {failed_attempts}")
    print("=" * 40)
    
def main():
    
    inventory = 0
    failed = 0
    
    print("Smart Inventory Auditor")
    print("Type 'quit' to exit\n")


    
        inventory = process_delivery(int(inventory), int(delivery))
        tax = calculate_tax(delivery)
    
        print(f"Tax for this delivery: {tax:.2f}")
        print(f"Total: {inventory} units\n")

        if inventory > 500:
            print("Inventory exceeds 500 units. Please review stock levels.\n")
            break
        
    generate_report(inventory, failed)

if __name__ == "__main__":
    main()