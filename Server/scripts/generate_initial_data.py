import json
import os
from datetime import datetime

def generate_initial_json():
    # Sample data structure
    initial_data = {
        "0123": {
            "Full name": "Nguyen Tran Gia Ky",
            "Age": "22",
            "Phone number": "0936045769",
            "Last attendance": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
    }

    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Write the JSON file
    json_path = os.path.join(data_dir, 'members.json')
    with open(json_path, 'w') as f:
        json.dump(initial_data, f, indent=4)

    print(f"Created initial members.json at {json_path}")

if __name__ == "__main__":
    generate_initial_json()
