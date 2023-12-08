# db_manager.py

import os
from pathlib import Path
import sqlite3
from elautil import config

class ELAAssessmentDatabase:

    def __init__(self):
        dbname = config.ELA_ASSESSMENT_LOCALDB_NAME
        dbdir = config.ELA_ASSESSMENT_LOCALDB_DIR
        if (os.path.exists(dbdir) == False):
            Path(dbdir).mkdir(parents=True)
        
        self.database_file = os.path.join(dbdir, dbname)
        self.connection = None
        self.connect()
        self.createTables()

    def connect(self):
        if (self.connection == None):
            try:
                self.connection = sqlite3.connect(self.database_file)
            except sqlite3.Error as e:
                self.connection = None
                print(f"Error connecting to the database: {e}")

        return

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def createTables(self):
        return

    def save_assessment(self,assessment_item):
        print(vars(assessment_item))
        return

    def create_table(self):
        """Create a sample table in the database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            self.connection.commit()
            print("Table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_user(self, username, email):
        """Insert a new user into the 'users' table."""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', (username, email))
            self.connection.commit()
            print("User inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")

    def query_users(self):
        """Query all users from the 'users' table."""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            return users
        except sqlite3.Error as e:
            print(f"Error querying users: {e}")
            return None
