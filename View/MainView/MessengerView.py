import socket, threading, os, time, sys
from tabulate import tabulate
from Database.Utils.FriendUtil import *
from collections import deque
from Database.Utils.MessageUtil import *
class MessengerView:
    def __init__(self, username):
        self.username = username
        self.friendUtil = FriendUtil()
        self.myDeque = deque()
        self.messageUtil = MessageUtil()
        
        self.getFriendsList()

    def createConnection(self):
        '''
            Main process that start client connection to the server 
            and handle its input messages
        '''
        SERVER_ADDRESS = '127.0.0.1'
        SERVER_PORT = 12000

        try:
            self.socket_instance = socket.socket()
            self.socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        except Exception as e:
            print(f"Error Server: {e}")

    def showView(self):
        choice = '-1'
        while choice != '0':
            os.system('cls')
            
            self.createConnection()
            # Connected to server
            self.socket_instance.send(self.username.encode())
            response = self.socket_instance.recv(1024).decode()

            print(tabulate(self.friends, headers=['username', 'fullname', 'gender', 'age'], tablefmt="grid"))
            choice = input("Select friend you want to chat: ")
            if choice in self.usernameList:
                if self.messageUtil.get5LastedMessage(self.username, choice):
                    for item in self.messageUtil.get5LastedMessage(self.username, choice):
                        self.myDeque.append(item)
                self.client(choice)

    def getFriendsList(self):
        self.friends = self.friendUtil.getFriendList(self.username)
        self.getUsernameFromFriendsList()
    
    def getUsernameFromFriendsList(self):
        self.usernameList = []
        for i in self.friends:
            self.usernameList.append(i[0])

    

    def client(self, recipient) -> None:

        self.recipient = recipient
        # Check if self.recipient is online
        self.socket_instance.send(f'CHECK_RECIPIENT: {self.recipient}'.encode())
        response = self.socket_instance.recv(1024).decode()
        if response == 'READY':
            print(f'You and {self.recipient} are ready to chat!')
            # Start listening for messages
            self.startMessegeListener()
        else:
            if response == 'ONLINE':
                print(f'{self.recipient} is currently online, but not ready to chat.')
            elif response == 'OFFLINE':
                print(f'{self.recipient} is currently offline.')
            
            while True:
                self.socket_instance.send(f'CHECK_RECIPIENT: {self.recipient}'.encode())
                response = self.socket_instance.recv(1024).decode()

                if response != 'READY':
                    messgaeInput = input("Do you want to send message offline? Press 'yes' to accept or presss any key to reload request chat online: ")
                    if messgaeInput == 'yes':
                        self.startMessegeOffline()
                        break 
                elif response == 'READY':
                    print(f'You and {self.recipient} are ready to chat!')
                    self.startMessegeListener()
                    break 
        try:
            pass

        except Exception as e:
            print(f'Error connecting to server socket {e}')
            # You can handle this case as needed
            input("Press to close the connect to server")
            self.socket_instance.close()

    def startMessegeOffline(self):
        msg = ''
        while msg != 'quit':
            self.showDequeView()
            msg = input("")
            if msg != 'quit':
                self.messageUtil.insert(self.username, self.recipient, self.messageUtil, msg)

    def startMessegeListener(self):
        # Start listening for messages
        threading.Thread(target=self.handle_messages, args=[self.socket_instance]).start()

        while True:
            os.system('cls')
            self.showDequeView()
            msg = input('')
            if msg == 'u':
                self.updateDequeUp()
            elif msg == 'd':
                self.updateDequeDown()
            elif msg == 'quit':
                self.socket_instance.send(f'END_CHAT:{self.recipient}'.encode())
                break
            else:
                self.socket_instance.send(f'SEND_MESSAGE:{self.username},{self.recipient},{msg}'.encode())
        input("Press to close server ...")
        self.socket_instance.close()

    def handle_messages(self, connection: socket.socket):
        '''
            Receive messages sent by the server and display them to user
        '''
        while True:
            try:
                msg = connection.recv(1024).decode().strip()
                if msg:
                    print(f'From server: {msg}')
                    if ':' in msg:
                        command, content = msg.split(':', 1)
                        command = command.strip()
                        content = content.strip()
                    else:
                        command = msg
                        content = ""

                    if command == "SEND_MESSAGE":
                        # sender, receiver, message = content.split(',')
                        # sender = sender.strip()
                        # receiver = receiver.strip()
                        # message = message.strip()

                        # Insert message to database
                        self.updateDequeDown()
                        self.showDequeView()
                else:
                    print('Server does not return anything')
                    break
            except Exception as e:
                print(f'Error handling message from server: {e}')
                input('Press any key to close connection ...')
                connection.close()
                break

    def updateDequeDown(self):
        # Check it is lasted message, we cant get lasted message
        if len(self.myDeque) == 5:
            if self.myDeque[4] != self.messageUtil.getLastedMessage(self.username, self.recipient):
                self.myDeque.append(self.messageUtil.getLastedMessage(self.username, self.recipient))
        elif len(self.myDeque) < 5:
            self.myDeque.append(self.messageUtil.getLastedMessage(self.username, self.recipient))
        if len(self.myDeque) == 6:
            self.myDeque.popleft()

    def updateDequeUp(self):
        if len(self.myDeque) == 5:
            if self.myDeque[0] != self.messageUtil.getOlderMessage(self.recipient, self.username, self.myDeque.pop()[2]):
                self.myDeque.appendleft(self.messageUtil.getOlderMessage(self.username, self.recipient, self.myDeque.pop()[2]))
        if len(self.myDeque) == 6:
            self.myDeque.pop()

    def showDequeView(self):
        os.system('cls')
        if not self.myDeque:
            return
        
        for item in self.myDeque:
            print(f"[{item[2]}] {item[0]}: {item[1]}")
        print("Input your message: ")
            