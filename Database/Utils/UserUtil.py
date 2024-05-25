import sqlite3
from DataStructure.LinkedList.UserLinkedList import *
from Database.BaseUtil import *

class UserUtil(BaseUtil):
    def __init__(self):
        self.db_name = 'Database/database.db'

    def connect(self):
        return sqlite3.connect(self.db_name)

    def insert(self, name, fullname, password, gender, age):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            INSERT INTO user (name, fullname, password, gender, age)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, fullname, password, gender, age))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

    def delete(self, name):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            DELETE FROM user WHERE name = ?
            ''', (name,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            conn.close()

    def update(self, name, fullname=None, password=None, gender=None, age=None):
        conn = self.connect()
        c = conn.cursor()
        try:
            if fullname is not None:
                c.execute('''
                UPDATE user SET fullname = ? WHERE name = ?
                ''', (fullname, name))
            if password is not None:
                c.execute('''
                UPDATE user SET password = ? WHERE name = ?
                ''', (password, name))
            if gender is not None:
                c.execute('''
                UPDATE user SET gender = ? WHERE name = ?
                ''', (gender, name))
            if age is not None:
                c.execute('''
                UPDATE user SET age = ? WHERE name = ?
                ''', (age, name))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
        finally:
            conn.close()

    def getAll(self, typeGet):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT * FROM user
            ''')
            users = c.fetchall()
            if typeGet == 'list':
                return users
            else: 
                user_list = UserLinkedList()
                user_list.insertAtBegin(users[0])
                for user in users:
                    user_list.insertAtEnd(user)
                return user_list
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

    def search(self, name):
        conn = self.connect()
        c = conn.cursor()
        try:
            search_parts = name.lower().split()
            query = "SELECT * FROM user WHERE "
            conditions = []
            for part in search_parts:
                conditions.append("LOWER(fullname) LIKE ?")
            query += " AND ".join(conditions)
            params = ['%' + part + '%' for part in search_parts]
            c.execute(query, params)
            results = c.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error searching data: {e}")
        finally:
            conn.close()
    
    def authenticator(self, name, password):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT name FROM user WHERE name = ? AND password = ?
            ''', (name, password))
            result = c.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            conn.close()

    def checkExist(self, name):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT 1 FROM user WHERE name = ?
            ''', (name,))
            result = c.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Error checking existence of name: {e}")
            return False
        finally:
            conn.close()

    def getProfileById(self, user_id):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT 'Name', name FROM user WHERE name = ?
            UNION
            SELECT 'Full Name', fullname FROM user WHERE name = ?
            UNION
            SELECT 'Gender', gender FROM user WHERE name = ?
            UNION
            SELECT 'Age', age FROM user WHERE name = ?
            ''', (user_id, user_id, user_id, user_id))
            profile = c.fetchall()
            return profile
        except sqlite3.Error as e:
            print(f"Error fetching profile: {e}")
            return None
        finally:
            conn.close()

    def getUsernameByFullName(self, fullname):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT name FROM user WHERE fullname = ?
            ''', (fullname,))  # Thêm dấu phẩy để tạo tuple
            profile = c.fetchone()
            return profile
        except sqlite3.Error as e:
            print(f"Error fetching profile: {e}")
            return None
        finally:
            conn.close()
