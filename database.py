import sqlite3

# Function to create the Users table
def create_table():
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()

    # Create the Users table with a CHECK constraint for the role column
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            dob TEXT NOT NULL,
            department TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('ADMIN', 'STUDENT')),
            gender TEXT)
    ''')

    conn.commit()
    conn.close()

# User all users
def fetch_users():
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    conn.close()
    return users

#  Data Insert
def insert_user(username, dob, department, password, role, gender):
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users(username, dob, department, password, role, gender) VALUES(?,?,?,?,?,?)', 
                       (username, dob, department, password, role, gender))
        conn.commit()
        print(f"User '{username}' inserted successfully.")

        # Fetch and display users immediately after insertion
        display_users()

    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
    finally:
        conn.close()

def delete_user(username):
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    display_users()  # Refresh UI after deletion

def update_user(username, dob, department, role, gender,id):
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET username = ?, dob = ?, department = ?, role = ?, gender = ? WHERE id = ?", 
                   (username, dob, department, role, gender, id))
    conn.commit()
    conn.close()
    display_users()  # Refresh UI after update

def id_exists(username):
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

# Function to create a new user (either ADMIN or STUDENT)
def create_user(username, password, role, dob, department, gender=None):
    if role not in ['ADMIN', 'STUDENT']:
        print("Invalid role. Role must be either 'ADMIN' or 'STUDENT'.")
        return

    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()

    try:
        # Insert the new user into the Users table
        cursor.execute(''' 
            INSERT INTO Users (username, dob, department, password, role, gender) 
            VALUES (?, ?, ?, ?, ?, ?) 
        ''', (username, dob, department, password, role, gender))
        conn.commit()
        print(f"{role} user '{username}' created successfully.")
        display_users()  # Refresh UI after insertion

    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
    finally:
        conn.close()

# Function to authenticate users (either ADMIN or STUDENT)
def authenticate_user(username, password):
    conn = sqlite3.connect('student-management.db')
    cursor = conn.cursor()

    # Try to find the user in the Users table
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[4]  # Password is in the 5th column
        if stored_password == password:
            return {
                "student_id": user[0],  
                "username": user[1], 
                "dob": user[2],     
                "department": user[3],
                "role": user[5],
                "gender": user[6]        
            }
        else:
            return "Invalid password."

    return "User not found."  # Return if user is not found

# Function to display all users after insert/update/delete
def display_users():
    users = fetch_users()
    print("\nCurrent Users in Database:")
    for user in users:
        print(user)
    print("\n")

# Example of creating users
def initialize_users():
    # Create a default admin user if not exists
    if not id_exists("admin"):
        create_user("admin", "admin", "ADMIN", "1980-01-01", "Administration", "Male")

    # Create a default student user if not exists
    if not id_exists("student"):
        create_user("student", "student", "STUDENT", "2000-01-01", "Computer Science", "Female")

# Main block to run the code
if __name__ == "__main__":
    # Initialize the database and create the table
    create_table()

    # Initialize default users
    initialize_users()

    # Test user authentication
    username = input("Enter username: ")
    password = input("Enter password: ")

    auth_result = authenticate_user(username, password)
    if isinstance(auth_result, dict):
        print(f"Authenticated {auth_result['role']} user: {auth_result['username']}")
    else:
        print(auth_result)

    # Show all users in the database
    display_users()
