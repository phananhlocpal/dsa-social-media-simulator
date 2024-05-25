import os
from Repository.LoginRepository import *
from View.MainView.MainView import *

class LoginView:
    def __init__(self):
        pass

    def showView(self):
        os.system('cls')
        print("Welcome to the login page")
        name = input("Enter 0 to back. Please input your username: ")
        password = input("Enter 0 to back. Please input your password: ")
        if name != '0' and password != '0':
            loginRepo = LoginRepository()
            if loginRepo.authenticator(name, password):
                mainView = MainView(name)
                mainView.showView()
            else: print("Login fail!")
       