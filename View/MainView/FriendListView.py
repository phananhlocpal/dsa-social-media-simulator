from Database.Utils.FriendUtil import *
from Database.Utils.UserUtil import *
from tabulate import tabulate
import os

class FriendListView:
    def __init__(self, username):
        self.username = username
        self.friendUtil = FriendUtil()
        self.userUtil = UserUtil()
        self.friends = UserLinkedList()
        self.getFriendsList()

    def showView(self):
        choice = '-1'
        while choice != '0':
            os.system('cls')
            self.printFriendList()
            print("\n1. Sort by username")
            print("2. Sort by age")
            print("3. Print my relationship schema")
            print("0. Back")
            choice = input("Your selection: ")
            if choice.isdigit:
                if choice == '1':
                    self.sortByUsername()
                if choice == '2':
                    self.sortByAge()
                if choice == '3':
                    graph = self.friendUtil.getAll('graph') 
                    graph.draw()


    def getFriendsList(self):
        self.friends = self.friendUtil.getFriendLinkedList(self.username)
    
    def sortByUsername(self):
        self.friends.sort("username")

    def sortByAge(self):
        self.friends.sort("age")

    def printFriendList(self):
        friend_data = []
        current_node = self.friends.head
        while current_node:
            friend_data.append([current_node.name, current_node.fullname, current_node.gender, current_node.age])
            current_node = current_node.next

        print(tabulate(friend_data, headers=['username', 'fullname', 'gender', 'age'], tablefmt="grid"))