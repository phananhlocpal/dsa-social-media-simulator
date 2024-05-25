from Database.BaseUtil import *
from DataStructure.LinkedList.UserLinkedList import *
from DataStructure.Graph.NetworkGraph import *
import sqlite3

class FriendUtil(BaseUtil):
    def __init__(self):
        super().__init__() 
        self.db_name = self.dbFile

    def connect(self):
        return sqlite3.connect(self.db_name)

    def insert(self, friend1, friend2):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            INSERT INTO friends (friend1, friend2)
            VALUES (?, ?)
            ''', (friend1, friend2))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

    def delete(self, friend1, friend2):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            DELETE FROM friends WHERE (friend1 = ? and friend2 = ?) or (friend1 = ? and friend2 = ?)
            ''', (friend1, friend2, friend2, friend1))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            conn.close()

    def update(self):
        pass

    def getAll(self, typeGet):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT * FROM friends
            ''')
            friends = c.fetchall()
            
            if typeGet == 'matrix':
                adjacency_list = {}
                for friend1, friend2 in friends:
                    if friend1 not in adjacency_list:
                        adjacency_list[friend1] = []
                    if friend2 not in adjacency_list:
                        adjacency_list[friend2] = []
                    adjacency_list[friend1].append(friend2)
                    adjacency_list[friend2].append(friend1)
                return adjacency_list
            
            elif typeGet == 'graph':
                graph = NetworkGraph()
                for friend1, friend2 in friends:
                    graph.add_edge(friend1, friend2)
                return graph
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

    def isRelationExist(self, friend1, friend2):
        conn = self.connect()
        c = conn.cursor()
        try:
            # Kiểm tra mối quan hệ hai chiều giữa friend1 và friend2
            c.execute('''
            SELECT 1 FROM friends WHERE (friend1 = ? AND friend2 = ?) OR (friend1 = ? AND friend2 = ?)
            ''', (friend1, friend2, friend2, friend1))
            result = c.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Error checking relation: {e}")
            return False
        finally:
            conn.close()

    def getRelation(self, name):
        pass

    def getFriendList(self, name):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT DISTINCT u.name, u.fullname, u.gender, u.age
            FROM user u, friends f
            WHERE (u.name = f.friend1 AND f.friend2 = ?) OR (u.name = f.friend2 AND f.friend1 = ?)
            ''', (name, name))
            friend_list = c.fetchall()
            return friend_list
        except sqlite3.Error as e:
            print(f"Error fetching friend list: {e}")
            return None
        finally:
            conn.close()
    
    def getFriendLinkedList(self, name):
        conn = self.connect()
        c = conn.cursor()
        friend_list_ll = UserLinkedList()  # Create a new linked list for friends
        try:
            c.execute('''
            SELECT DISTINCT u.name, u.fullname, u.gender, u.age
            FROM user u, friends f
            WHERE (u.name = f.friend1 AND f.friend2 = ?) OR (u.name = f.friend2 AND f.friend1 = ?)
            ''', (name, name))
            friends = c.fetchall()
            # Add friends to the linked list
            for friend in friends:
                friend_node = UserNode(friend[0], friend[1], friend[2], friend[3])
                friend_list_ll.insertAtEnd(friend_node)
            return friend_list_ll
        except sqlite3.Error as e:
            print(f"Error fetching friend list: {e}")
            return None
        finally:
            conn.close()