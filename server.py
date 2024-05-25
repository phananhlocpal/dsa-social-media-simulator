import socket, threading
from typing import Optional
from Database.Utils.MessageUtil import *

# Global dictionaries to maintain client's connections and their usernames
connections = {}
users = {}
pending_requests = {}  # Dictionary to track pending chat requests

ready_users = {}

def handle_user_connection(connection: socket.socket, address: str) -> None:
    # Receive the username first
    user = connection.recv(1024).decode().strip()
    users[connection] = user  # Store the connection object as the key
    ready_users[user] = None
    connection.send(f'{user} has connected from {address[0]}:{address[1]}'.encode())
    print(f'{user} has connected from {address[0]}:{address[1]}')
    while True:
        msg = connection.recv(1024).decode().strip()
        
        if msg:
            print(f"Messege from client << {msg} >>")
            # Split the message into command and content
            if ':' in msg:
                command, content = msg.split(':', 1)
                command = command.strip()
                content = content.strip()
            else:
                command = msg
                content = ""

            if command == "CHECK_RECIPIENT":
                recipient = content
                # Handle the case when recipient is not found
                key_list = []
                for key, value in ready_users.items():
                    key_list.append(key)
                if recipient not in key_list:
                    print(ready_users)
                    connection.send('OFFLINE'.encode())
                else:
                    recipient_conn = get_connection_by_username(recipient)
                    if recipient_conn:
                        ready_users[user] = recipient
                        print(ready_users)
                        # recipient is found
                        if ready_users[recipient] == user:
                            connection.send(f'READY'.encode())
                        else:
                            connection.send('ONLINE'.encode())
                    else:
                        # recipient is not found (unlikely but handle it)
                        connection.send('OFFLINE'.encode())
            elif command == "SEND_MESSAGE":
                sender, receiver, message = content.split(',',2)
                sender = sender.strip()
                receiver = receiver.strip()
                message = message.strip()
                messageUtil = MessageUtil()
                messageUtil.insert(sender, receiver, sender, message)
                connection.send(f'SEND_MESSAGE: {sender}, {receiver}, {message}'.encode())
                recipient_conn.send(f'SEND_MESSAGE: {sender}, {receiver}, {message}'.encode())
            elif command == "END_CHAT":
                recipient = content
                end_chat(user, recipient)
        else:
            print("Lỗi 1")
            remove_connection(connection)
            break
    try:
        pass
    except Exception as e:
        print(f'Error handling user connection: {e}')
        remove_connection(connection)

def get_connection_by_username(username: str) -> Optional[socket.socket]:
    '''
        Retrieve connection object by username
    '''
    for conn, user in users.items():
        if user == username:
            return conn
    return None

def start_chat(user1: str, user2: str, user2_conn: socket.socket) -> None:
    '''
        Start chat between two users
    '''
    for conn, user in users.items():
        if user == user1:
            user1_conn = conn
            break

    user1_conn.send(f'Chat with {user2} has started.'.encode())
    user2_conn.send(f'Chat with {user1} has started.'.encode())
    pending_requests.pop(user1, None)
    pending_requests.pop(user2, None)

def end_chat(user: str, recipient: str) -> None:
    '''
        End chat between two users
    '''
    for conn, u in users.items():
        if u == user or u == recipient:
            try:
                conn.send(f'Chat ended between {user} and {recipient}.'.encode())
            except Exception as e:
                print(f'Error sending end chat message: {e}')
                remove_connection(conn)

def remove_connection(conn: socket.socket) -> None:
    '''
        Remove specified connection from connections list
    '''
    if conn in connections:
        user = users[conn]
        print(f'{user} has disconnected.')
        conn.close()
        del connections[conn]
        del users[conn]
        pending_requests.pop(user, None)

def server() -> None:
    '''
        Main process that receives client's connections and starts a new thread
        to handle their messages
    '''

    LISTENING_PORT = 12000

    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')

        while True:
            socket_connection, address = socket_instance.accept()
            connections[socket_connection] = address
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        for conn in connections.keys():
            print("Lỗi 3")
            remove_connection(conn)
        socket_instance.close()

if __name__ == "__main__":
    server()
