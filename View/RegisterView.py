from Repository.RegisterRepository import *
import os
class RegisterView:
    def __init__(self) -> None:
        self.registerRepository = RegisterRepository()

    def showView(self):
        os.system('cls')
        print("Welcome to our social network")
        name = input("Enter 0 to back. Input your name to register: ")
        if name != "0":
            password = input("Enter 0 to back. Input your password to register: ")
            if password != '0':
                age = input("Enter 0 to back. Input your age to register: ")
                if age != '0':
                    fullname = input("Enter 0 to back. Input your fullname to register: ")
                    if fullname != '0':
                        gender = input("Enter 0 to back. Input your gender to register: ")
                        if gender != '0':
                            # Add user to data
                            self.registerRepository.addUser(name, fullname, password, gender, age)
