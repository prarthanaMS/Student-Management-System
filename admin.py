from tkinter import Toplevel, StringVar, messagebox, ttk, Canvas, Scrollbar
import tkinter as tk
from customtkinter import CTkLabel, CTkEntry, CTkComboBox, CTkButton
from PIL import Image, ImageTk
import subprocess
import database

def open_admin_dashboard():
    app = Toplevel()
    app.title("Student Management System - Admin Dashboard")
    app.geometry('925x600+300+200')
    app.configure(bg="white")

    font1 = ('Arial', 12, 'bold')
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold")) 

    # Load the illustration image
    img_path = "./asset/admin.jpg"
    image = Image.open(img_path)
    image = image.resize((400, 350), Image.LANCZOS)
    img = ImageTk.PhotoImage(image)

    # UI Title and Logout Button
    header_frame = tk.Frame(app, bg="#f2f2f2", height=50)
    header_frame.pack(fill="x")

    title = tk.Label(header_frame, text="Edu Management System", font=('Arial', 18, 'bold'), fg="#007bff", bg="#f2f2f2")
    title.pack(side="left", padx=20)

    # Redirect to main.py upon logout
    def logout():
        app.destroy()  # Close the current window
        subprocess.run(["python", "main.py"])  # Open main.py

    logout_button = tk.Button(header_frame, text="Logout", font=font1, fg="white", bg="red", command=logout)
    logout_button.pack(side="right", padx=20, pady=10)

    # Left-side Form Fields
    form_frame = tk.Frame(app, bg="white")
    form_frame.place(x=20, y=70)

    # Create global StringVars for Gender and Role
    gender_var = StringVar()
    role_var = StringVar()

    # User Name Label and Entry
    CTkLabel(form_frame, text="User Name :", font=font1, text_color="#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    username_entry = CTkEntry(form_frame, font=font1, text_color="#000", fg_color="white", border_color="#007bff", border_width=2, width=200)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    # Date Of Birth Label and Entry
    CTkLabel(form_frame, text="Date of Birth :", font=font1, text_color="#000000").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    dob_entry = CTkEntry(form_frame, font=font1, text_color="#000", fg_color="white", border_color="#007bff", border_width=2, width=200)
    dob_entry.grid(row=1, column=1, padx=10, pady=5)

    # Gender Label and ComboBox
    CTkLabel(form_frame, text="Gender :", font=font1, text_color="#000000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    gender_dropdown = CTkComboBox(form_frame, font=font1, text_color="#000", fg_color="white", variable=gender_var, values=['Male', 'Female'], state='readonly', border_width=2, width=200)
    gender_var.set("Male")
    gender_dropdown.grid(row=2, column=1, padx=10, pady=5)

    # Department Label and Entry
    CTkLabel(form_frame, text="Department :", font=font1, text_color="#000000").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    department_entry = CTkEntry(form_frame, font=font1, text_color="#000", fg_color="white", border_color="#007bff", border_width=2, width=200)
    department_entry.grid(row=3, column=1, padx=10, pady=5)

    # Password Label and Entry
    CTkLabel(form_frame, text="Password :", font=font1, text_color="#000000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    password_entry = CTkEntry(form_frame, font=font1, text_color="#000", fg_color="white", border_color="#007bff", border_width=2, width=200, show="*")
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    # Role Label and ComboBox
    CTkLabel(form_frame, text="Role :", font=font1, text_color="#000000").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    role_dropdown = CTkComboBox(form_frame, font=font1, text_color="#000", fg_color="white", variable=role_var, values=['Student', 'Admin'], state='readonly',  border_width=2, width=200)
    role_var.set("Student")
    role_dropdown.grid(row=5, column=1, padx=10, pady=5)

    # Buttons (Add, Clear, Update, Delete)
    button_frame = tk.Frame(app, bg="white")
    button_frame.place(x=20, y=300)

    CTkButton(button_frame, text="ADD", font=font1, fg_color="#17a2b8", text_color="white", width=100, command=lambda: insert()).grid(row=0, column=0, padx=5, pady=10)
    CTkButton(button_frame, text="Clear", font=font1, fg_color="#007bff", text_color="white", width=100, command=lambda: clear()).grid(row=0, column=1, padx=5, pady=10)
    CTkButton(button_frame, text="Update", font=font1, fg_color="orange", text_color="white", width=100, command=lambda: update()).grid(row=1, column=0, padx=5, pady=10)
    CTkButton(button_frame, text="Delete", font=font1, fg_color="red", text_color="white", width=100, command=lambda: delete()).grid(row=1, column=1, padx=5, pady=10)

    # Right-side Image Placement
    img_label = tk.Label(app, image=img, bg="white")
    img_label.image = img
    img_label.place(x=550, y=90)

    # Table for Student Records
    table_frame = tk.Frame(app, bg="white")
    table_frame.place(x=20, y=400)

    tree = ttk.Treeview(table_frame, height=8, columns=("ID", "Name", "DOB", "Department","Password", "Role", "Gender"))
    
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="User Name")
    tree.heading("DOB", text="Date Of Birth")
    tree.heading("Department", text="Department")
    tree.heading("Password", text="Password")
    tree.heading("Role", text="Role")
    tree.heading("Gender", text="Gender")

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("ID", width=100)
    tree.column("Name", width=120)
    tree.column("DOB", width=120)
    tree.column("Department", width=120)
    tree.column("Password", width=120)
    tree.column("Role", width=100)
    tree.column("Gender", width=100)

    tree.pack(fill="both", expand=True)

    # Functions for CRUD Operations
    def add_to_treeview():
        """Fetch data and update the Treeview."""
        users = database.fetch_users()
        tree.delete(*tree.get_children())  # Clear old data
        for user in users:
            tree.insert('', 'end', values=user)

    def display_data(event):
        """Display selected row data in the entry fields."""
        selected_item = tree.focus()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()  # Call clear() without any arguments
            username_entry.insert(0, row[1])
            dob_entry.insert(0, row[2])
            department_entry.insert(0, row[3])
            password_entry.insert(0, row[4])  # Assuming password is part of the data
            role_var.set(row[5])
            gender_var.set(row[6])

    def insert():
        """Insert new user into the database."""
        username = username_entry.get()
        dob = dob_entry.get()
        department = department_entry.get()
        password = password_entry.get()
        role = role_var.get()
        gender = gender_dropdown.get()

        if not username or not dob or not department or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        if database.id_exists(username):
            messagebox.showerror("Error", "User already exists!")
            return

        database.insert_user(username, dob, department, password, role, gender)
        clear()
        add_to_treeview()  # Refresh treeview
        messagebox.showinfo('Success', 'User added successfully!')

    def update():
        """Update user details in the database."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a user to update')
            return
        id = tree.item(selected_item)['values'][0]
        username = username_entry.get()
        dob = dob_entry.get()
        department = department_entry.get()
        role = role_var.get()
        gender = gender_dropdown.get()

        database.update_user(username, dob, department, role, gender, id)
        add_to_treeview()  # Refresh treeview
        clear()
        messagebox.showinfo('Success', 'User updated successfully')

    def delete():
        """Delete selected user from the database."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a user to delete')
            return
        
        username = username_entry.get()
        database.delete_user(username)
        add_to_treeview()  # Refresh treeview
        clear()
        messagebox.showinfo('Success', 'User deleted successfully')

    def clear():
        """Clear all entry fields."""
        username_entry.delete(0, tk.END)
        dob_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        role_dropdown.set('STUDENT')
        gender_dropdown.set('Male')

    def update_table():
        """Update the Treeview with data from the database."""
        tree.delete(*tree.get_children())
        users = database.fetch_users()
        for user in users:
            tree.insert('', 'end', values=user)

    # Bind event to Treeview
    tree.bind('<ButtonRelease>', display_data)

    update_table()
    app.mainloop()
