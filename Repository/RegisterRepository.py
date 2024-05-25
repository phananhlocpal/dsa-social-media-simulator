from Database.Utils.UserUtil import *

class RegisterRepository:
    def __init__(self) -> None:
        pass

    def addUser(self, username, fullname, password, gender, age):
        userUtil = UserUtil()
        userUtil.insert(username, fullname, password, gender, age)