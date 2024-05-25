import sqlite3
import os
from tabulate import tabulate

def query(queryString):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console for Windows and Unix-based systems
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute(queryString)
        conn.commit()
        
        # Determine the type of query
        queryType = queryString.strip().split()[0].upper()
        
        if queryType in ['INSERT', 'UPDATE', 'DELETE']:
            # For INSERT, UPDATE, DELETE queries, show affected row count
            print(f"Query executed successfully. Rows affected: {c.rowcount}")
        else:
            # For SELECT queries, fetch and display the results
            rows = c.fetchall()
            if rows:
                column_names = [description[0] for description in c.description]
                print(tabulate(rows, headers=column_names, tablefmt="grid"))
            else:
                # If no rows are returned, print column names from the `user` table as an example
                column_names = [description[0] for description in c.description]
                print(tabulate([], headers=column_names, tablefmt="grid"))
            
    except Exception as e:
        print(f"Error in query: {e}")
    finally:
        conn.close()

# Test DELETE query

queryString = '''
INSERT INTO friends (friend1, friend2)
VALUES ('locpa', 'anhhp');

'''
queryString = '''
SELECT user, message, time
                FROM message
                WHERE (user1 = 'locpa' AND user2 = 'thaoqhn') OR (user1 = 'thaoqhn' AND user2 = 'locpa')
                ORDER BY time DESC
                LIMIT 5
'''


queryString = '''
                    SELECT time FROM message
                WHERE user1 = locpa AND user2 = thaoqhn AND time = ?
                ORDER BY time DESC
                LIMIT 1
            
'''
# queryString = '''
# INSERT INTO user (name, fullname, password, gender, age)
# VALUES ('anhhp', 'Phạm Hoàng Anh', '123', 'Nam', 24)
# '''
query(queryString)
