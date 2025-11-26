import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role="user"):
    """
    Register a new user in the database.
    """
    # Validate input
    if not username or not password:
        return False, "Username and password are required."
    
    conn = connect_database()
    cursor = conn.cursor()
    
    # Ensure users table exists
    create_users_table(conn)
    
    # Check if username already exists
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    password_hash_str = password_hash.decode("utf-8")
    
    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash_str, role)
    )
    conn.commit()
    conn.close()
    
    return True, f"User '{username}' registered successfully with role '{role}'."

def login_user(username, password):
    """
    Authenticate a user against the database.
    """
    user = get_user_by_username(username)
    
    # User not found
    if not user:
        return False, "User not found."
    
    stored_hash = user[2]  # password_hash column
    
    # Verify password
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        role = user[3]  # role column
        return True, f"Login successful! Welcome {username} (role: {role})."
    else:
        return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """
    Migrate users from users.txt to the database.
    """
    path = Path(filepath)
    
    # Check if file exists
    if not path.exists():
        print(f"⚠️ Warning: {filepath} not found. Skipping migration.")
        return 0
    
    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0
    
    # Read the file line by line
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            
            # Parse the line
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue
            
            username = parts[0]
            password_hash = parts[1]
            role = parts[2] if len(parts) >= 3 else "user"
            
            # Insert into database using parameterized query
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                migrated_count += 1
            except sqlite3.IntegrityError:
                # User already exists (username is UNIQUE)
                print(f"⚠️ User '{username}' already exists. Skipping.")
    
    conn.commit()
    conn.close()
    return migrated_count