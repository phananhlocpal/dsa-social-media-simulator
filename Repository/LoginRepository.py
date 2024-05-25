from Database.Utils.UserUtil import *

class LoginRepository:
    def __init__(self):
        self.userUtil = UserUtil()
        
    def authenticator(self, username, password):
        return self.userUtil.authenticator(username, password)