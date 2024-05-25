from Database.Utils.UserUtil import *
from Database.Utils.FriendUtil import *
class SearchPeopleRepository:
    def __init__(self):
        self.userUtil = UserUtil()
        self.friendUtil = FriendUtil()

    def search(self, name):
        return self.userUtil.search(name)
    
    def checkExistRelation(self, friend1, friend2):
        return self.friendUtil.isRelationExist(friend1, friend2)