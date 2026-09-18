

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
    
