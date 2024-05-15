import customtkinter
from tkinter import *
from tkinter import messagebox
import database
import main  # Importing the main application window

# Dictionary of predefined username-password pairs
credentials = {
    'admin': 'password123'
}

def verify_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in credentials and credentials[username] == password:
        # If credentials are correct, open the main application window
        root.destroy()  # Close the login window
        main.run_main_app()  # Open the main application window
    else:
        # If credentials are incorrect, display an error message
        messagebox.showerror('Login Failed', 'Invalid username or password')

# Create the login window
root = customtkinter.CTk()
root.title('Login')
root.geometry('300x300')
root.config(bg='#161c25')

font1 = ('Roboto', 20, 'bold')
font2 = ('Roboto', 12, 'bold')

# Username label and entry field
username_label = customtkinter.CTkLabel(root, text='Username:', font=font2, text_color='#fff', bg_color='#161C25')
username_label.pack(pady=5)
username_entry = customtkinter.CTkEntry(root, font=font2, text_color='#000', fg_color='#fff', border_color='#0C9295', border_width=2)
username_entry.pack(pady=5)

# Password label and entry field
password_label = customtkinter.CTkLabel(root, text='Password:', font=font2, text_color='#fff', bg_color='#161C25')
password_label.pack(pady=5)
password_entry = customtkinter.CTkEntry(root, font=font2, text_color='#000', fg_color='#fff', border_color='#0C9295', border_width=2, show='*')
password_entry.pack(pady=5)

# Login button
login_button = customtkinter.CTkButton(root, text='Login', font=font2, command=verify_login, text_color='#fff', fg_color='#05A312', hover_color='#00850B', bg_color='#161c25', cursor='hand2', corner_radius=15)
login_button.pack(pady=20)

root.mainloop()
