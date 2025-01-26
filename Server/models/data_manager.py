import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_file="data/members.json"):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Create data file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            initial_data = {
                "0123": {
                    "Full name": "John Doe",
                    "Age": "25",
                    "Phone number": "0123456789",
                    "Last attendance": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                }
            }
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=4)
            print(f"Created initial {self.data_file} with sample data")

    def get_member_info(self, member_id):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data.get(member_id, None)
        except Exception as e:
            print(f"Error reading member data: {e}")
            return None

    def add_member(self, member_id, member_data):
        try:
            # Validate input data
            required_fields = ["Full name", "Age", "Phone number"]
            if not all(field in member_data for field in required_fields):
                print("Error: Missing required fields")
                return False
            
            if not member_data["Phone number"].isdigit():
                print("Error: Phone number must contain only digits")
                return False
            
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Check if member already exists
            if member_id in data:
                print(f"Error: Member with ID {member_id} already exists")
                return False
                
            # Add timestamp if not present
            if "Last attendance" not in member_data:
                member_data["Last attendance"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            data[member_id] = member_data
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Successfully added member with ID {member_id}")
            return True
            
        except Exception as e:
            print(f"Error adding member: {e}")
            return False

    def update_attendance(self, member_id):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            if member_id in data:
                data[member_id]["Last attendance"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                
                with open(self.data_file, 'w') as f:
                    json.dump(data, f, indent=4)
                return True
            return False
        except Exception as e:
            print(f"Error updating attendance: {e}")
            return False
