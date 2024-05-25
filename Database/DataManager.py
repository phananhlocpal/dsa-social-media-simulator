import sqlite3, os

os.system('cls')
# Function to drop a table if it exists
def drop_table_if_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    if cursor.fetchone():
        cursor.execute(f"DROP TABLE {table_name};")
        print(f"Table {table_name} dropped.")
    else:
        print(f"Table {table_name} does not exist.")

# Kết nối tới cơ sở dữ liệu (sẽ tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop tables if they exist
tables = ['post', 'message', 'user', 'comment', 'friends']
for table in tables:
    drop_table_if_exists(c, table)

# Tạo bảng user
c.execute('''
CREATE TABLE user (
    name TEXT PRIMARY KEY,
    fullname TEXT,
    password TEXT NOT NULL,
    gender TEXT,
    age INTEGER
)
''')

# Tạo bảng post
c.execute('''
CREATE TABLE IF NOT EXISTS post (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT,
    caption TEXT,
    time DATETIME,
    FOREIGN KEY (username) REFERENCES user(name)
)
''')

# Tạo bảng message
c.execute('''
CREATE TABLE IF NOT EXISTS message (
    user1 TEXT,
    user2 TEXT,
    time DATETIME,
    user TEXT,
    message TEXT,
    PRIMARY KEY (user1, user2, time),
    FOREIGN KEY (user1) REFERENCES user(name),
    FOREIGN KEY (user2) REFERENCES user(name),
    FOREIGN KEY (user) REFERENCES user(name)
)
''')

# Create comment table
c.execute('''
CREATE TABLE IF NOT EXISTS comment (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    comment_content TEXT,
    comment_sibling INTEGER,
    comment_child INTEGER, 
    isRoot BOOLEAN,
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (comment_child) REFERENCES comment(comment_id)
    FOREIGN KEY (comment_sibling) REFERENCES comment(comment_id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS friends (
    friend1 TEXT,
    friend2 TEXT,
    FOREIGN KEY (friend1) REFERENCES user(name),
    FOREIGN KEY (friend2) REFERENCES user(name)
)          

''')

try:
    # Lưu các thay đổi
    conn.commit()
    print("Commit successfuly!")
except Exception as e:
    print("Commit failed: ", e)
finally:
    # Đóng kết nối tới cơ sở dữ liệu
    conn.close()
