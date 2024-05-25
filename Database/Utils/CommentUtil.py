import sqlite3
from DataStructure.Tree.CommentKAryTree import *
from Database.BaseUtil import *

class CommentUtil(BaseUtil):
    def __init__(self):
        super().__init__() 
        self.db_name = self.dbFile

    def connect(self):
        return sqlite3.connect(self.db_name)

    def insert(self,  postId:int, commentContent:str, commentSibling, commentChild, isRoot):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            INSERT INTO comment (post_id, comment_content, comment_sibling, comment_child, isRoot)
            VALUES (?, ?, ?, ?, ?)
            ''', (postId, commentContent, commentSibling, commentChild, isRoot))
            conn.commit()

            comment_id = c.lastrowid
            return comment_id
        except Exception as e:
            print(f"Error inserting data: {e}")
            input()
        finally:
            conn.close()

    def delete(self, commentId):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            DELETE FROM post WHERE comment_id = ?
            ''', (commentId))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            conn.close()

    def update(self, commentId, commentContent, comment_child, comment_sibling):
        conn = self.connect()
        c = conn.cursor()
        try:
            # Constructing the query dynamically with parameter substitution
            query_parts = []
            query_params = []

            if commentContent is not None:
                query_parts.append("comment_content = ?")
                query_params.append(commentContent)
            
            if comment_child is not None:
                query_parts.append("comment_child = ?")
                query_params.append(comment_child)
            
            if comment_sibling is not None:
                query_parts.append("comment_sibling = ?")
                query_params.append(comment_sibling)
            
            query_params.append(commentId)

            if query_parts:
                queryString = f"UPDATE comment SET {', '.join(query_parts)} WHERE comment_id = ?"
                c.execute(queryString, query_params)
                conn.commit()
            else:
                print("No fields to update.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
        finally:
            conn.close()
    
    def getAllByPostId(self, postId, typeGet):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT * FROM comment WHERE post_id = ?
            ''', (int(postId),))
            comment_list = c.fetchall()
            if typeGet == 'list':
                return comment_list
            elif typeGet == 'tree':
                if comment_list:
                    commentTree = CommentKaryTree()
                    commentTree.build_tree(comment_list)
                    return commentTree
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

    def find_last_sibling_root_id(self, postId):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT comment_id FROM comment WHERE post_id = ? and isRoot = True
            ''', (int(postId),))
            comment_list = c.fetchall()
            
            # Check if the list is not empty and get the comment_id of the last comment
            if comment_list:
                last_sibling_root_id = comment_list[-1][0]  # Assuming comment_id is the first column
            else:
                last_sibling_root_id = None
                
            return last_sibling_root_id
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            conn.close()

    def checkExistCommentId(self, commentId: int):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
            SELECT comment_id FROM comment WHERE comment_id = ?
            ''', (int(commentId),))
            comment_list = c.fetchall()
            
            if comment_list:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            conn.close()