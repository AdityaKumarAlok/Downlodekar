import os

def delete_items_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Directory '{folder_path}' does not exist.")
        return
    
    # Check if it's a directory
    if not os.path.isdir(folder_path):
        print(f"'{folder_path}' is not a directory.")
        return
    
    # Get a list of all items in the directory
    items = os.listdir(folder_path)
    
    # Iterate over each item and delete if it's a file
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted: {item_path}")

# Example usage:
directory_path = "/path/to/your/directory"
delete_items_in_folder(directory_path)
