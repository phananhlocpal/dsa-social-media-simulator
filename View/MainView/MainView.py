import os
from View.MainView.NewsFeedView.NewsFeedView import *
from View.MainView.SearchPeopleView import *
from View.MainView.FriendListView import *
from View.MainView.ProfileView import *
from View.MainView.MessengerView import *
from tabulate import tabulate

class MainView:
    def __init__(self, name):
        self.name = name
        self.textList = []
        self.textList.append([''])
        self.textList.append(['1. News feed'])
        self.textList.append(['2. Search people'])
        self.textList.append(['3. Friends list'])
        self.textList.append(['4. My profile'])
        self.textList.append(['5. Messenger'])
        self.textList.append(['0. Log out'])

    def showView(self):
        main_choice = '-1'
        while main_choice != '0':
            os.system('cls')
            print(tabulate(self.textList, headers=['DASHBOARD'], tablefmt='grid'))
            main_choice = input("\nInput your choice: ")
            if main_choice.isdigit():
                choice = int(main_choice)
                # Case proccess
                if choice == 1:
                    newsFeedView = NewsFeedView(self.name)
                    newsFeedView.showView()
                elif choice == 2:
                    searchPeopleView = SearchPeopleView(self.name)
                    searchPeopleView.showView()
                elif choice == 3:
                    friendListView = FriendListView(self.name)
                    friendListView.showView()
                elif choice == 4:
                    profileView = ProfileView(self.name)
                    profileView.showView()
                elif choice == 5:
                    messengerView = MessengerView(self.name)
                    messengerView.showView()    
            else:
                print("Invalid input. Please enter a number.")
                input("Press any key to continue ...")
                main_choice = '-1'


'''
login. Vì thêm nhiều hơn là truy cập vào danh sách, nên lựa chọn danh sách liên kết
newfeed (Post Linkedlist)
searchPople SQL


'''