from Repository.MainRepository.NewsFeedRepository import *
from collections import deque
from View.MainView.NewsFeedView.DetailPostView import *
import keyboard
from datetime import datetime
import os, time,sys
from tabulate import tabulate
from Database.Utils.PostUtil import *
import threading

class NewsFeedView:
    def __init__(self, name):
        self.name = name
        self.postUtil = PostUtil()
        # Define pending stack
        self.sizeStack = 5
        self.pendingStack = deque()

        # Define display list
        self.sizeList = 10
        self.displayList = []

        # Define start and end
        self.start = 0
        self.end = 5

        # Initialize gettedList
        self.gettedList = []

        self.initPendingStack()
        # Start the updatePendingStack in a separate thread
        self.update_thread = threading.Thread(target=self.updatePendingStackWhenSleep)
        self.update_thread.daemon = True
        self.update_thread.start()

        # Wait for the stack to be initially populated
        time.sleep(0.5)  # Wait a bit for the first update to happen

        # Print the display list
        self.printDisplayList()

    def showView(self):
        choice = ''
        while choice != '0':
            os.system('cls')

            # Show Post
            self.printDisplayList()
           
            print('\nInstruction: \n- Press \'0\' to back previous menu. \n- Press \'u\' to go up.\n- Press \'d\' to go down.\n- Press number of post to show detail.\n- Press C to create a post.\n- Press R to reload news feed.')
            choice = input("Select your choice: ")
            
            # Using `keyboard` to detect key presses
            if choice.lower() == 'u':
                if self.start != 0:
                    self.start -= 1
                    self.end -= 1
            elif choice.lower() == 'd':
                # Case allowing down:
                    # End does not equal to len of list
                    # End = len(list) and stack is not empty => updateDisplayList
                if self.end < len(self.displayList):
                    self.start += 1
                    self.end += 1
                    self.printDisplayList()
                elif self.end == len(self.displayList) and len(self.pendingStack) != 0:
                    self.start += 1
                    self.end += 1
                    self.updateDisplayList()
                    self.printDisplayList()
                # Case denying down:
                    # End = len(list) and stack is empty
                elif self.end == len(self.displayList) and not self.pendingStack:
                    t = 3
                    while t > 0:
                        # Print the message and flush the output
                        sys.stdout.write(f"\rPlease wait for loading latest news in {t} second(s)!")
                        sys.stdout.flush()
                        time.sleep(1)
                        t -= 1
                    # Clear the final message after the countdown
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    sys.stdout.flush()
            elif choice.lower() == 'c':
                print('You chose to create a post.')
                caption = input("Input your caption: ")
                self.create_post(caption)
            elif choice.isdigit():
                if int(choice) > 0:
                    detailPostView = DetailPostView(int(choice))
                    detailPostView.showView()                    

    def create_post(self, caption):
        # Insert caption to database
        newsfeedRepo = NewsFeedRepository()
        newsfeedRepo.insertPost(username=self.name, caption=caption, time=datetime.now())

    def initPendingStack(self):
        # Get 10 lastest post (at least if have) and append to pending stack
        lastedPost = self.postUtil.get10LastedPost(self.gettedList)
        if lastedPost:
            for post in lastedPost:
                self.pendingStack.append(post)
                self.gettedList.append(post[0])
            
            if len(self.pendingStack) < 10:
                for i in range(len(self.pendingStack)):
                    self.displayList.append(self.pendingStack.pop())
            else:
                for i in range(10):
                    self.displayList.append(self.pendingStack.pop())    

    def updatePendingStackWhenSleep(self):
        while True:
            # Updating each 5 seconds if len < 20
            # Get 1 lastest post (if have) and append to pending stack
            if len(self.pendingStack) < 20:
                lastedPost = self.postUtil.getLastedPost(self.gettedList)
                if lastedPost:
                    self.pendingStack.append(lastedPost)
                    self.gettedList.append(lastedPost[0])
            time.sleep(5)


    def updateDisplayList(self):
        if not self.pendingStack:
            return False
        else:
            # Check down? Get the 5 latest posts (at least) from pending stack
            if len(self.pendingStack) < 5:
                while self.pendingStack:
                    self.displayList.append(self.pendingStack.pop())
            else:

                for i in range(5):
                    self.displayList.append(self.pendingStack.pop())
            return True
            
    def printDisplayList(self):
        # Check if end index is within the valid range of displayList
        if self.end > len(self.displayList):
            self.end = len(self.displayList)

        # Check if there are any items to display
        if self.start >= len(self.displayList):
            print("No more posts to display.")
            return False

        # Create a temporary list for the range to display
        temp_list = []
        for i in range(self.start, self.end):
            if i <= len(self.displayList):
                temp_list.append([f"{self.displayList[i][0]}\n{self.displayList[i][1]}\n{self.displayList[i][3]}\n{self.displayList[i][2]}"])

        # Print the posts in a tabulated format if there are any to display
        if temp_list:
            print(tabulate(temp_list, headers=["Your News Feed"], tablefmt="grid"))
            return True
        else:
            print("No posts to display.")
            return False
