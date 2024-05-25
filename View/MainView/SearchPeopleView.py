import os
from Repository.MainRepository.SearchPeopleRepository import *
from Database.Utils.UserUtil import *
from Database.Utils.FriendUtil import *
from DataStructure.Tree.BKTree import *

class SearchPeopleView:
    def __init__(self, username):
        self.username = username
        self.userUtil = UserUtil()
        self.bktree = BKTree()
        self.buildTree()

    def buildTree(self):
        userList = self.userUtil.getAll("list")
        for user in userList:
            self.bktree.add(user[1]) # Add fullname node to BK Tree

    def showView(self):
        choice = '-1'
        while choice != '0':
            os.system('cls')
            print("Search people in our social media")
            print("Enter 0 to back main menu")
            choice = input("Input name of person who you want to find: ")
            if choice != '0':
                os.system('cls')
                self.search(choice)
                choice = input("Enter 0 to back main menu. Enter any key to continue: ")
    
    def search(self, name):
        new_choice = '-1'
        # Start searching name
        while new_choice != '0':
            os.system('cls')
            if self.bktree.search(name, 2):
                print("We found these people in our social media:")
                for i in self.bktree.search(name, 2):
                    username = self.userUtil.getUsernameByFullName(i)
                    print(f"{username[0]}: {i}")
                
                print("\nChoose people to add friend or press 0 to back!")
                new_choice = input("Input your choice: ")
                if new_choice != '0':
                    if self.checkExistRelation(new_choice, self.username):
                        print("You have been friends!")
                    else:
                        userUtil = UserUtil()
                        if userUtil.checkExist(new_choice):
                            self.addFriend(self.username, new_choice)
                            print("Add friends sucessfully! You are friends.")
                        else: print("This choice does not exist in database!")
                    input("Press any key to continue ...")
            else:
                print("We cant find any person naming this")
                input("Press any key to continue ...")
                break
    
    def addFriend(self, friend1, friend2):
        # Add friends and update data
        friendUtil = FriendUtil()
        friendUtil.insert(friend1, friend2)

    def checkExistRelation(self, friend1, friend2):
        return self.searchRepo.checkExistRelation(friend1, friend2)
