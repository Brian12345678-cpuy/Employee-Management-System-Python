from tkinter import filedialog
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database
import time 
import database_backup
import shutil
import os 
import sys

def scheduled_backup():
    database_backup.automated_backup()
    messagebox.showinfo("Auto Backup", "The database has been backed up.")
    database_backup.automated_replication()
    messagebox.showinfo("Auto Replicate", "The database has been replicated.")
    app.after(60000, scheduled_backup)

def backup_to_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        backup_file = database_backup.backup_database(folder_selected)
        messagebox.showinfo("Success", f"The database has been backed up to {backup_file}")

def replicate_database():
    database_backup.replicate_database()
    messagebox.showinfo("Success", "The database has been replicated.")

def restore_backup():
    pass

def back_up_database():
    database_backup.backup_database()
    messagebox.showinfo("Success", "The database has been backed up.")


def download_strategy():
    def resource_path(relative_path):
        """ Get the absolute path to the resource, works for both development and PyInstaller bundle. """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Path to the strategy PDF file
    strategy_file = resource_path('Strategy/Disaster_Recovery_Plan_for_Enterprise_Database.pdf')
    
    print(f"Looking for strategy file at: {strategy_file}")
    
    # Check if the strategy file exists
    if not os.path.isfile(strategy_file):
        print("The strategy file does not exist.")
        messagebox.showerror("Error", "The strategy file does not exist.")
        return

    # Ask user where to save the file
    save_location = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    
    if save_location:
        try:
            with open(strategy_file, 'rb') as src_file:
                with open(save_location, 'wb') as dest_file:
                    dest_file.write(src_file.read())
            print(f"Strategy PDF has been saved to {save_location}")
            messagebox.showinfo("Success", f"Strategy PDF has been saved to {save_location}")
        except FileNotFoundError:
            print("The strategy file was not found.")
            messagebox.showerror("Error", "The strategy file was not found.")
        except PermissionError:
            print("Permission denied. Please check your file permissions.")
            messagebox.showerror("Error", "Permission denied. Please check your file permissions.")
        except Exception as e:
            print(f"Failed to save the strategy PDF: {e}")
            messagebox.showerror("Error", f"Failed to save the strategy PDF: {e}")


def run_main_app():
    global app
    app = customtkinter.CTk()
    app.title('Employee Management System')
    app.geometry('950x520')
    app.config(bg='#161c25')
    app.resizable(False, False)

    font1 = ('Roboto', 20, 'bold')
    font2 = ('Roboto', 12, 'bold')

    def add_to_treeview():
        employees = database.fetch_employees()
        tree.delete(*tree.get_children())
        for employee in employees:
            tree.insert('', END, values=employee)

    def clear(*clicked):
        if clicked:
            tree.selection_remove(tree.focus())
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        role_entry.delete(0, END)
        variable1.set('Male')
        variable2.set('Active')

    def display_data(event):
        selected_item = tree.focus()
        if selected_item:
            item_values = tree.item(selected_item)
            if 'values' in item_values:
                clear()
                values = item_values['values']
                id_entry.insert(0, values[0])
                name_entry.insert(0, values[1])
                role_entry.insert(0, values[2])
                variable1.set(values[3])
                variable2.set(values[4])
        else:
            pass

    def restore_database():
        backup_file = filedialog.askopenfilename(filetypes=[("Database Files", "*.db *.bak")])
        if backup_file:
            database_backup.restore_database(backup_file)
            messagebox.showinfo("Success", "Database has been successfully restored.")
            add_to_treeview()

    def delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to delete.')
        else:
            id = id_entry.get()
            name = name_entry.get()
            database.delete_employee(id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', name + ' has been deleted from the database.')

    def update():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update.')
        else:
            id = id_entry.get()
            name = name_entry.get()
            role = role_entry.get()
            gender = variable1.get()
            status = variable2.get()
            database.update_employee(name, role, gender, status, id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', name + ' of ID: ' + id + ' has been updated.')

    def insert():
        id = id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        gender = variable1.get()
        status = variable2.get()
        if not (id and name and role and gender and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exists(id):
            messagebox.showerror('Error', 'ID already exists.')
        else:
            database.insert_employee(id, name, role, gender, status)
            add_to_treeview()
            messagebox.showinfo('Success', name + ' has been added to the database.')

    id_label = customtkinter.CTkLabel(app, font=font1, text='ID:', text_color='#fff', bg_color='#161C25')
    id_label.place(x=20, y=20)

    id_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    id_entry.place(x=100, y=20)

    name_label = customtkinter.CTkLabel(app, font=font1, text='Name:', text_color='#fff', bg_color='#161C25')
    name_label.place(x=20, y=80)

    name_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    name_entry.place(x=100, y=80)

    role_label = customtkinter.CTkLabel(app, font=font1, text='Role:', text_color='#fff', bg_color='#161C25')
    role_label.place(x=20, y=140)

    role_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295', border_width=2, width=180)
    role_entry.place(x=100, y=140)

    gender_label = customtkinter.CTkLabel(app, font=font1, text='Gender:', text_color='#fff', bg_color='#161C25')
    gender_label.place(x=20, y=200)

    options = ['Male', 'Female']
    variable1 = StringVar()

    gender_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295', border_color='#0C9295', width=180, variable=variable1, values=options, state='readonly')
    gender_options.set('Male')
    gender_options.place(x=100, y=200)

    status_label = customtkinter.CTkLabel(app, font=font1, text='Status:', text_color='#fff', bg_color='#161C25')
    status_label.place(x=20, y=260)

    options_2 = ['Active', 'Inactive']
    variable2 = StringVar()

    status_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295', border_color='#0C9295', width=180, variable=variable2, values=options_2, state='readonly')
    status_options.set('Active')
    status_options.place(x=100, y=260)

    add_button = customtkinter.CTkButton(app, command=insert, font=font1, text_color='#fff', text='Add Employee', fg_color='#05A312', hover_color='#00850B', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260)
    add_button.place(x=20, y=310)

    clear_button = customtkinter.CTkButton(app, command=lambda:clear(True), font=font1, text_color='#fff', text='New Employee', fg_color='#161c25', hover_color='#ff5002', bg_color='#161c25', border_color='#f15704',  border_width=2, cursor='hand2', corner_radius=15, width=260)
    clear_button.place(x=20, y=360)

    update_button = customtkinter.CTkButton(app, command=update,  font=font1, text_color='#fff', text='Update Employee', fg_color='#161c25', hover_color='#ff5002', bg_color='#161c25', border_color='#f15704',  border_width=2, cursor='hand2', corner_radius=15, width=260)
    update_button.place(x=300, y=360)

    delete_button = customtkinter.CTkButton(app, command=delete, font=font1, text_color='#fff', text='Delete Employee', fg_color='#e40404', hover_color='#ae0000', bg_color='#161c25', border_color='#e40404',  border_width=2, cursor='hand2', corner_radius=15, width=260)
    delete_button.place(x=580, y=360)

    backup_button = customtkinter.CTkButton(app, font=font1, text_color='#fff', text='Backup Database', fg_color='#0C9295', hover_color='#0C9350', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260, command=back_up_database)
    backup_button.place(x=20, y=410)

    backup_to_button = customtkinter.CTkButton(app, font=font1, text_color='#fff', text='Backup To Folder', fg_color='#0C9295', hover_color='#0C9350', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260, command=backup_to_folder)
    backup_to_button.place(x=300, y=410)

    replicate_button = customtkinter.CTkButton(app, font=font1, text_color='#fff', text='Replicate Database', fg_color='#0C9295', hover_color='#0C9350', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260, command=replicate_database)
    replicate_button.place(x=580, y=410)

    restore_button = customtkinter.CTkButton(app, font=font1, text_color='#fff', text='Restore Database', fg_color='#0C9295', hover_color='#0C9350', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260, command=restore_database)
    restore_button.place(x=20, y=460)

    # New button for downloading strategy
    download_strategy_button = customtkinter.CTkButton(app, font=font1, text_color='#fff', text='Download Strategy', fg_color='#0C9295', hover_color='#0C9350', bg_color='#161c25', cursor='hand2', corner_radius=15, width=260, command=download_strategy)
    download_strategy_button.place(x=300, y=460)

    style = ttk.Style(app)
    style.theme_use('clam')
    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
    style.map('Treeview', background=[('selected', '#1a8f2d')])

    tree = ttk.Treeview(app, height=15)
    tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Status')
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', anchor=tk.CENTER, width=120)
    tree.column('Name', anchor=tk.CENTER, width=120)
    tree.column('Role', anchor=tk.CENTER, width=120)
    tree.column('Gender', anchor=tk.CENTER, width=120)
    tree.column('Status', anchor=tk.CENTER, width=120)

    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Role', text='Role')
    tree.heading('Gender', text='Gender')
    tree.heading('Status', text='Status')

    tree.place(x=300, y=20)
    tree.bind('<ButtonRelease>', display_data)

    add_to_treeview()
    app.after(60000, scheduled_backup)
    app.mainloop()

if __name__ == "__main__":
    run_main_app()
