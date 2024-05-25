import os, time
from View.LoginView import *
from View.RegisterView import *
from tabulate import tabulate
from style import *

def startScreen():
    # Starting program
    for i in range(70):
        os.system('cls')
        print("{test:^70}".format(test = "WELCOME TO MY PROGRAM"))
        print()
        print("[{test:<70}]".format(test = "."*i))
        print("{test:>70}".format(test = "LOADING " + str(round((i/70)*100)) + "%"))
        time.sleep(0.02)

def endScreen():
    isExit = False
    os.system("cls")
    print("\t\tSTUDENTS AND TEACHERS MANAGEMENT PROGRAM")
    print("\t\t===== THANKS FOR USING THE PROGRAM =====")
    print()
    confirm = input("Enter \"Y\" to comfirm exit or \"N\" to return the main menu: ")
    while confirm != "Y" and confirm != "N":
        confirm = input("\t-> You must choose \"Y\" or \"N\". Please re-enter \"Y\" or \"N\": ")
    if confirm == "Y":
        os.system("cls")
        for i in range(3,0, -1):
            os.system("cls")
            print("\tGOOD BYE!")
            print("\tThe program will exit in ", i, " second.")
            time.sleep(1)
        os.system("cls")
        isExit = True
    else: 
        for i in range(3,0, -1):
            os.system("cls")
            print("\tWELCOME BACK")
            print("\tYou will return the main menu in ", i, " second.")
            time.sleep(1)
    return isExit

def main():
    # Declare required variables
    main_choice = int(0)
    isExit = False
    textList = []
    textList.append(['Made by Pal, Tai, Han anh Nhung'])
    textList.append([''])
    textList.append(['1. Login'])
    textList.append(['2. Register new account'])
    textList.append(['3. Exit'])

    # Declare repository
    loginView = LoginView()
    registerView = RegisterView()

    # Main program        
    while isExit != True:
        os.system('cls')
        print(tabulate(textList, headers=["SOCIAL MEDIA SIMULATOR"], tablefmt='grid'))
        main_choice = int(input("\nSelect your choice: "))

        #========================================================================================
        if main_choice == 1:
            loginView.showView()
        if main_choice == 2:
            registerView.showView()
        if main_choice == 3:
            if endScreen == True:
                isExit = True            

main()
