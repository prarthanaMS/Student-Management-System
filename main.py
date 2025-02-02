from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from admin import open_admin_dashboard  # Import the Admin Dashboard
from student import open_student_dashboard  # Import the Student Dashboard
from database import authenticate_user  # Assuming this is for login authentication

root = Tk()
root.title('Student Management System')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Define frames for the UI
login_frame = Frame(root, width=925, height=500, bg="white")
admin_frame = Frame(root, width=925, height=500, bg="white")
student_frame = Frame(root, width=925, height=500, bg="white")

# Create a function to show a frame
def show_frame(frame):
    frame.place(x=0, y=0)
    frame.tkraise()

# Function to handle the login action
def signin():
    username = user.get()
    password = code.get()

    # Check the login credentials
    result = authenticate_user(username, password)
    if isinstance(result, dict):  # Successful login
        role = result['role']
        if role == 'ADMIN':
            messagebox.showinfo("Login Successful", f"Welcome, Admin!")
            root.destroy()  # Close the current window
            open_admin_dashboard()  # Open Admin Dashboard in admin.py
        else:
            messagebox.showinfo("Login Successful", f"Welcome, Student {username}!")
            student_details = {
                'student_id': result['student_id'], 
                'username': result['username'],    
                'dob': result['dob'],
                'department': result['department'], 
                'role': result['role'],  
                'gender': result['gender']               
            }
            open_student_dashboard(student_details)  # Open Student Dashboard
    else:  # Invalid login
        messagebox.showerror("Invalid", result)

# Code for handling the image loading and login form in the login_frame
try:
    image = Image.open(r"./asset/login.jpg")
    img = ImageTk.PhotoImage(image)
    Label(login_frame, image=img, bg='white').place(x=50, y=50)
except Exception as e:
    messagebox.showerror("Error", f"Image not found or cannot be loaded: {e}")

# Login form on the login_frame
frame = Frame(login_frame, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def handle_enter(e, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')

def handle_leave(e, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)

user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', lambda e: handle_enter(e, user, 'Username'))
user.bind('<FocusOut>', lambda e: handle_leave(e, user, 'Username'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', lambda e: handle_enter(e, code, 'Password'))
code.bind('<FocusOut>', lambda e: handle_leave(e, code, 'Password'))
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign In', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)
Sign_Up = Button(frame, width=6, text='Sign Up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
Sign_Up.place(x=215, y=270)

# Show the login frame initially
show_frame(login_frame)

root.mainloop()

