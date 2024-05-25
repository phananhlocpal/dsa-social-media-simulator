from collections import deque
from Database.Utils.PostUtil import *
class NewsFeedRepository:
    def __init__(self):
        pass
        # init post stack and import data 
    
    def insertPost(self, username, caption, time):
        postUtil = PostUtil()
        postUtil.insert(username= username, caption = caption, time = time)

    def removePost():
        pass

    def displayPost(self):
        pass

    def getAllPost(self, typeGet):
        postUtil = PostUtil()
        return postUtil.getAll(typeGet)