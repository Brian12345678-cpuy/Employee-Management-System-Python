import sqlite3
import os
import shutil
from datetime import datetime
import threading

# Function to create the backups table
def create_backups_table():
    try:
        conn = sqlite3.connect('Backups.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS backups (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        time TEXT,
                        type TEXT,
                        location TEXT
                        )''')
        conn.commit()
        conn.close()
        print("Backups table created successfully.")
    except Exception as e:
        print(f"Error creating backups table: {str(e)}")

# Function to insert a new backup record into the backups table
def insert_backup_record(date, time, backup_type, location):
    try:
        conn = sqlite3.connect('Backups.db')
        c = conn.cursor()
        c.execute('''INSERT INTO backups (date, time, type, location)
                     VALUES (?, ?, ?, ?)''', (date, time, backup_type, location))
        conn.commit()
        conn.close()
        print("Backup record inserted successfully.")
    except Exception as e:
        print(f"Error inserting backup record: {str(e)}")

# Function to perform database backup
def backup_database(target_folder=None):
    try:
        source_db = "Employees.db"
        timestamp = datetime.now()
        formatted_date = timestamp.strftime("%Y-%m-%d")
        formatted_time = timestamp.strftime("%H-%M-%S")
        formatted_time_db = timestamp.strftime("%H:%M:%S")

        if target_folder:
            backup_file = os.path.join(target_folder, f"Backup_{formatted_date}_{formatted_time}.bak")
        else:
            target_folder = "Backups"
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            backup_file = os.path.join(target_folder, f"Backup_{formatted_date}_{formatted_time}.bak")
        
        # Insert backup record into the backups table
        insert_backup_record(formatted_date, formatted_time_db, "Manual Backup", backup_file)
        
        source_conn = sqlite3.connect(source_db)
        backup_conn = sqlite3.connect(backup_file)

        with source_conn:
            source_conn.backup(backup_conn)

        print("Backup completed successfully.")
        
        return backup_file
    except Exception as e:
        print(f"Error during backup: {str(e)}")
        return None

# Function to perform auto database backup
def auto_backup_database():
    try:
        source_db = "Employees.db"
        timestamp = datetime.now()
        formatted_date = timestamp.strftime("%Y-%m-%d")
        formatted_time = timestamp.strftime("%H-%M-%S")
        formatted_time_db = timestamp.strftime("%H:%M:%S")

        target_folder = "Backups"
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        backup_file = os.path.join(target_folder, f"Auto_Backup_{formatted_date}_{formatted_time}.bak")
        
        # Insert backup record into the backups table
        insert_backup_record(formatted_date, formatted_time_db, "Automatic Backup", backup_file)
        
        source_conn = sqlite3.connect(source_db)
        backup_conn = sqlite3.connect(backup_file)

        with source_conn:
            source_conn.backup(backup_conn)

        print("Auto Backup completed successfully.")
        
        return backup_file
    except Exception as e:
        print(f"Error during backup: {str(e)}")
        return None

# Function to replicate database
def replicate_database():
    try:
        source_db = "Employees.db"
        target_folder = "Replicates"
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        timestamp = datetime.now()
        formatted_date = timestamp.strftime("%Y-%m-%d")
        formatted_time = timestamp.strftime("%H-%M-%S")
        formatted_time_db = timestamp.strftime("%H:%M:%S")
        target_db = os.path.join(target_folder, f"Replicated_{formatted_date}_{formatted_time}.db")
        
        shutil.copy(source_db, target_db)
        insert_backup_record(formatted_date, formatted_time_db, "Replication", target_db)
        print("Replication completed successfully.")
        
        return target_db
    except Exception as e:
        print(f"Error during replication: {str(e)}")
        return None

# Function to perform auto database replication   
def auto_replicate_database():
    try:
        source_db = "Employees.db"
        target_folder = "Replicates"
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        timestamp = datetime.now()
        formatted_date = timestamp.strftime("%Y-%m-%d")
        formatted_time = timestamp.strftime("%H-%M-%S")
        formatted_time_db = timestamp.strftime("%H:%M:%S")
        target_db = os.path.join(target_folder, f"Auto_Replicated_{formatted_date}_{formatted_time}.db")
        
        shutil.copy(source_db, target_db)
        insert_backup_record(formatted_date, formatted_time_db, "Automatic Replication", target_db)
        print("Auto Replication completed successfully.")
        
        return target_db
    except Exception as e:
        print(f"Error during replication: {str(e)}")
        return None

# Automated backup function
def automated_backup():
    auto_backup_database()
    

# Automated replication function
def automated_replication():
    auto_replicate_database()
    
# Function to restore the database from a backup file
def restore_database(backup_file):
    try:
        # Ensure the backup file exists
        if not os.path.exists(backup_file):
            print("Backup file does not exist.")
            return
        
        # Get the current database file
        current_db = "Employees.db"
        
        # Close any existing connections to the database
        conn = sqlite3.connect(current_db)
        conn.close()
        
        # Remove the current database file
        os.remove(current_db)
        
        # Copy the backup file to replace the current database
        shutil.copy(backup_file, current_db)
        
        print("Database restored successfully.")
    except Exception as e:
        print(f"Error during database restoration: {str(e)}")

# Create backups table if it doesn't exist
create_backups_table()
