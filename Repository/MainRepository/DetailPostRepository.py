from collections import deque
from Database.Utils.CommentUtil import *
from Database.Utils.PostUtil import *

class DetailPostRepository:
    def __init__(self):
        self.commentUtil = CommentUtil()
        self.postUtil = PostUtil()
        # init post stack and import data 
    
    def insertComment(self, postId, commentContent, commentSibling, commentChild, isRoot):
        return self.commentUtil.insert(int(postId), str(commentContent), commentSibling, commentChild, isRoot)

    def removePost():
        pass

    def displayPost(self):
        pass

    def getAllComment(self, typeGet):
        return self.commentUtil.getAll(typeGet)
    
    def getAllCommentByPostId(self, postId, typeGet):
        return self.commentUtil.getAllByPostId(int(postId), typeGet)
    
    def updateComment(self, commentId, commentContent, commentSibling, commentChild):
        self.commentUtil.update(int(commentId), commentContent, commentChild, commentSibling)
    
    def findCommentRootSiblingId(self,postId):
        return self.commentUtil.find_last_sibling_root_id(postId)
    
    def checkExistCommentId(self, commentId: int):
        return self.commentUtil.checkExistCommentId(commentId)

    def updatePost(self, postId:int, caption):
        self.postUtil.update(postId, caption)

    def getPostCaption(self, postId):
        post = self.postUtil.getPostById(postId)
        return post[2]