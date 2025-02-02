from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk

def open_student_dashboard(student_details):
    # Create a new window for the student dashboard
    screen = Toplevel()
    screen.title("Student Management System - Student Dashboard")
    screen.geometry('925x500+300+200')  # Window size
    screen.config(bg="white")

    # Load the illustration (Ensure the correct path)
    img_path = "./asset/student.jpg"  # Path to the uploaded image
    image = Image.open(img_path)
    image = image.resize((350, 250), Image.LANCZOS)  # Resize to match UI
    img = ImageTk.PhotoImage(image)

    # Place the image on the left
    img_label = Label(screen, image=img, bg="white")
    img_label.image = img  # Keep reference
    img_label.place(x=50, y=120)

    # Welcome message
    Label(screen, text=f'Welcome {student_details["username"]}!', 
          bg='white', font=('Arial', 22, 'bold')).place(x=530, y=50)

    # Student information labels
    details = [
        ("Student ID", student_details["student_id"]),
        ("Student Name", student_details["username"]),
        ("Date of Birth", student_details["dob"]),
        ("User Role", student_details["role"]),
        ("Gender", student_details["gender"]),
        ("Department", student_details["department"])
    ]

    # Positioning the text neatly
    y_position = 130
    for label, value in details:
        Label(screen, text=f"{label} :", bg='white', font=('Arial', 14, 'bold')).place(x=500, y=y_position)
        Label(screen, text=value, bg='white', font=('Arial', 14)).place(x=650, y=y_position)
        y_position += 40

    # Logout button styling
    logout_button = Button(screen, text="Logout", command=screen.destroy,
                           bg='red', fg='white', font=('Arial', 12, 'bold'),
                           width=10, height=1, borderwidth=2)
    logout_button.place(x=630, y=370)

    screen.mainloop()
