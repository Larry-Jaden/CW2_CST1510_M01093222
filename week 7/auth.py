# week 7

import bcrypt
import os

# Constants
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt with automatic salt generation.
    
    Args:
        plain_text_password (str): The plaintext password to hash
        
    Returns:
        str: The hashed password as a UTF-8 string
    """
    # Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    
    # Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a stored bcrypt hash.
    
    Args:
        plain_text_password (str): The password to verify
        hashed_password (str): The stored hash to check against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    # Encode both the plaintext password and the stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    # Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def user_exists(username):
    """
    Checks if a username already exists in the user database.
    
    Args:
        username (str): The username to check
        
    Returns:
        bool: True if the user exists, False otherwise
    """
    # Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    # Read the file and check each line for the username
    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f.readlines():
                # Split the line into username and hash
                stored_username = line.strip().split(',')[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False
    
    return False

def register_user(username, password):
    """
    Registers a new user by hashing their password and storing credentials.
    
    Args:
        username (str): The username for the new account
        password (str): The plaintext password to hash and store
        
    Returns:
        bool: True if registration successful, False if username already exists
    """
    # Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Append the new user to the file
    # Format: username,hashed_password
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    
    print(f"Success: User '{username}' registered successfully!")
    return True

def login_user(username, password):
    """
    Authenticates a user by verifying their username and password.
    
    Args:
        username (str): The username to authenticate
        password (str): The plaintext password to verify
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    
    # Search for the username in the file
    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f.readlines():
                # Split the line, handling potential commas in the hash
                parts = line.strip().split(',', 1)  # Split only on first comma
                if len(parts) == 2:
                    stored_username, stored_hash = parts
                    
                    # If username matches, verify the password
                    if stored_username == username:
                        if verify_password(password, stored_hash):
                            print(f"Success: Welcome, {username}!")
                            return True
                        else:
                            print("Error: Invalid password.")
                            return False
    except FileNotFoundError:
        print("Error: User database not found.")
        return False
    except Exception as e:
        print(f"Error reading user database: {e}")
        return False
    
    # If we reach here, the username was not found
    print("Error: Username not found.")
    return False

def validate_username(username):
    """
    Validates username format.
    
    Args:
        username (str): The username to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Basic validation as suggested in workshop concepts
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    if len(username) > 20:
        return False, "Username must be no more than 20 characters long."
    
    return True, "Username is valid."

def validate_password(password):
    """
    Validates password strength.
    
    Args:
        password (str): The password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Basic validation as suggested in workshop concepts
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    
    return True, "Password is valid."

def display_menu():
    """Displays the main menu options."""
    print("\n")
    print("Building a Secure Authentication System")
    print("")
    print("[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("")

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("Please select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\nUSER REGISTRATION")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
            
        elif choice == '2':
            # Login flow
            print("\nUSER LOGIN")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("(In a real application, you would now access the dashboard)")
                input("\nPress Enter to return to main menu...")
            
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()