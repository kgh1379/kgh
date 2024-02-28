import os

# Define the project structure
project_structure = {
    "RI_Inventory_Management": {
        "pages": ["dashboard.py", "inventory.py", "usage.py", "stock_input.py", "purchase_requests.py", "storage.py", "disposal.py"],
        "utils": ["database.py", "notifications.py"],
        "data": [],
        "tests": ["test_database.py", "test_notifications.py"],
    }
}

# Function to create directories and files
def create_structure(base_path, structure):
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for item in contents:
            if "." in item:  # It's a file
                open(os.path.join(folder_path, item), 'a').close()
            else:  # It's a directory
                create_structure(folder_path, {item: contents[item]})

# Create the project structure
create_structure(".", project_structure)