from Database.Utils.UserUtil import *
from tabulate import tabulate
import os
class ProfileView:
    def __init__(self, username):
        self.username = username
        self.userUtil = UserUtil()
        self.getProfile()

    def showView(self):
        choice = '-1'
        while choice != '0':
            os.system('cls')
            print("My Profile")
            print(tabulate(self.profile, headers=['Section', 'Information'], tablefmt='grid'))
            print("1. Change Password")
            print("2. Change Fullname")
            print("0. Back")
            choice = input("Your selection: ")
            if choice.isdigit:
                if choice == '1':
                    new_password = input("Your new password: ")
                    self.changePassword(new_password)
                    print("Your password changed")
                    self.getProfile()
                elif choice == '2':
                    new_fullname = input("Your new full name: ")
                    self.changeFullName(new_fullname)
                    print("Your full name changed")
                    self.getProfile()
            else:
                print("Invalid command. Your must enter a number!")
            input("Press any key to continue ...")

    def getProfile(self):
        self.profile = self.userUtil.getProfileById(self.username)
    
    def changePassword(self, new_password):
        self.userUtil.update(name=self.username, password=new_password)
    
    def changeFullName(self, new_fullname):
        self.userUtil.update(name=self.username, fullname=new_fullname)
