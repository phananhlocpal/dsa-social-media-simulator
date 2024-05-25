import sqlite3
from DataStructure.LinkedList.PostLinkedList import *
from Database.BaseUtil import *

class PostUtil(BaseUtil):
    def __init__(self):
        super().__init__() 
        self.db_name = self.dbFile

    def connect(self):
        return sqlite3.connect(self.db_name)

    def insert(self, username, caption, time):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            INSERT INTO post (username, caption, time)
            VALUES (?, ?, ?)
            ''', (username, caption, time))
            conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

    def delete(self, name, time):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            DELETE FROM post WHERE username = ? and time = ?
            ''', (name, time))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            conn.close()

    def update(self,postId:int, caption):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            UPDATE post SET caption = ? WHERE post_id = ?
            ''', (caption, postId))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
        finally:
            conn.close()

    def getAll(self, typeGet):
        conn = self.connect()
        c = conn.cursor()
        try:
            posts = list()
            c.execute('''
            SELECT * FROM post
            ''')
            posts = c.fetchall()
            if typeGet == 'list':
                return posts
            if typeGet == 'linkedlist':
                post_list = PostLinkedList()
                for post in posts:
                    post_list.append(post)
                return post_list
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

    def getPostById(self, postId:int):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT * FROM post WHERE post_id = ?
            ''', (postId, ))
            post = c.fetchone()          
            return post
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

    def get10LastedPost(self, gettedList: list):
    # Initialize gettedList as an empty list if it is None
        if gettedList is None:
            gettedList = []

        conn = self.connect()
        c = conn.cursor()
        try:
            if gettedList:
                # Write the SQL query to select the 10 latest posts not in gettedList
                query = '''
                    SELECT * FROM (
                        SELECT post_id, username, caption, time
                        FROM post
                        WHERE post_id NOT IN ({})
                        ORDER BY time DESC
                        LIMIT 10
                    )
                    ORDER BY time ASC
                '''.format(','.join('?' * len(gettedList)))
                
                c.execute(query, gettedList)
            else:
                # If gettedList is empty, just get the latest 10 posts
                query = '''
                    SELECT * FROM (
                        SELECT post_id, username, caption, time
                        FROM post
                        ORDER BY time DESC
                        LIMIT 10
                    )
                    ORDER BY time ASC
                '''
                c.execute(query)
            
            posts = c.fetchall()
            return posts
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()


    def getLastedPost(self, gettedList: list):
    # Initialize gettedList as an empty list if it is None
        if gettedList is None:
            gettedList = []

        conn = self.connect()
        c = conn.cursor()
        try:
            if gettedList:
                # Write the SQL query to select the 10 latest posts not in gettedList
                query = '''
                    SELECT * FROM (
                        SELECT post_id, username, caption, time
                        FROM post
                        WHERE post_id NOT IN ({})
                        ORDER BY time DESC
                        LIMIT 1
                    )
                    ORDER BY time ASC
                '''.format(','.join('?' * len(gettedList)))
                
                c.execute(query, gettedList)
            else:
                # If gettedList is empty, just get the latest 10 posts
                query = '''
                    SELECT * FROM (
                        SELECT post_id, username, caption, time
                        FROM post
                        ORDER BY time DESC
                        LIMIT 1
                    )
                    ORDER BY time ASC
                '''
                c.execute(query)
            
            post = c.fetchone()
            return post
        except sqlite3.Error as e:
            print(f"Error fetching data here: {e}")
        finally:
            conn.close()
