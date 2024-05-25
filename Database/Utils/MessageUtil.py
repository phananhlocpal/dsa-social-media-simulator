import sqlite3
from DataStructure.LinkedList.UserLinkedList import *
from Database.BaseUtil import *
from datetime import datetime

class MessageUtil(BaseUtil):
    def __init__(self):
        self.db_name = 'Database/database.db'

    def connect(self):
        return sqlite3.connect(self.db_name)

    def insert(self, user1, user2, user, message):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO message (user1, user2, time, user, message)
                                       VALUES (?, ?, ?, ?, ?)''', (user1, user2, datetime.now(), user, message))
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

    def get5LastedMessage(self, user1, user2):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
                SELECT user, message, time
                FROM message
                WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
                ORDER BY time DESC
                LIMIT 5
            ''', (user1, user2, user2, user1))
            messages = c.fetchall()
            return messages
        except sqlite3.Error as e:
            print(f"Error fetching profile: {e}")
            return None
        finally:
            conn.close()
    
    def getLastedMessage(self, user1, user2):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute("""
                SELECT user, message, time
                FROM message
                WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
                ORDER BY time DESC
                LIMIT 1
            """, (user1, user2, user2, user1))
            messages = c.fetchone()
            return messages
        except sqlite3.Error as e:
            print(f"Error fetching profile: {e}")
            return None
        finally:
            conn.close()

    def getOlderMessage(self, user1, user2, time):
        conn = self.connect()
        c = conn.cursor()
        try:
            # Find the time of the given message
            c.execute('''
                SELECT time FROM message
                WHERE ((user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)) AND time = ?
                ORDER BY time DESC
                LIMIT 1
            ''', (user1, user2, user2, user1, time))
            
            result = c.fetchone()
            if result is None:
                print("Given message not found.")
                return None
            
            message_time = result[0]
            
            # Get messages older than the given message
            c.execute('''
                SELECT user, message, time FROM message
                WHERE ((user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)) AND time < ?
                ORDER BY time DESC
                LIMIT 1
            ''', (user1, user2, user2, user1, message_time))
            
            older_messages = c.fetchone()
            return older_messages
            
        except sqlite3.Error as e:
            print(f"Error fetching messages: {e}")
            return None
        finally:
            conn.close()
