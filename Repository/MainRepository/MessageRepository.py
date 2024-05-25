from Data.DataManager import *

from collections import deque

class MessageRepository:
    def __init__(self, person1, person2):
        self.sender = person1
        self.reciever = person2
        self.queue = deque()
        self.data = DataManager.getMessageData(person1, person2)

        # init messenge queue and import data
       
    def initData(self):
        if (self.data.isEmpty()):
            # create new file
            pass
        else: 
            for message in self.data:
                self.queue.append(self.data)

    def addMessage(self, message):
        self.queue.append(message) # insert into queue
        DataManager.saveMesssageData(message) # save massage to txt file (data)

    def showMessage(self):
        tempQueue = self.queue
        while tempQueue.count != 0:
            print(tempQueue.popleft())



