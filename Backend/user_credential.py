import json
import os

# Define the file where credentials will be stored
credentials_file = "user_credentials.json"

# Function to load users from the JSON file
def load_users():
    # Check if the file exists
    if not os.path.exists(credentials_file):
        # If the file does not exist, create an empty JSON file
        with open(credentials_file, 'w') as file:
            json.dump({}, file)  # Create an empty dictionary
        
    # Load users from the file
    try:
        with open(credentials_file, 'r') as file:
            users_db = json.load(file)
    except json.JSONDecodeError:
        # If the file is corrupted or has bad data, return an empty dictionary
        users_db = {}
    
    return users_db

# Function to save users to the JSON file
def save_users(users_db):
    # Save the data to the JSON file
    with open(credentials_file, 'w') as file:
        json.dump(users_db, file, indent=4)
