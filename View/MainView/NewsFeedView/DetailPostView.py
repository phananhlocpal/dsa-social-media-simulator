from style import *
from Repository.MainRepository.DetailPostRepository import *
from Database.Utils.PostUtil import *
class DetailPostView:
    def __init__(self, postId):
        self.postId = postId
        postUtil = PostUtil()
        post = postUtil.getPostById(int(self.postId))
        self.username = post[1]
        self.caption = post[2]
        self.time = post[3]
        self.detailRepo = DetailPostRepository()

    def showView(self):
        choice = -1
        while choice != "3":
            os.system('cls')
            # Show name, time and caption
            print("Detail post")
            box = BoxStyle([self.username, str(self.time), self.getPostCaption(int(self.postId))])
            box.print()
            # Show comment (Tree)
            print("Comments:")
            self.getComment()
            if self.commentTree != None:
                commentTreeStyle = CommentTreeStyle(self.commentTree)
                node = commentTreeStyle.node
                commentTreeStyle.print_tree(node)
            # Show choice
            print("\n\n1. Edit your caption")
            print("2. Comment")
            print("3. Back")
            choice = input("Select your choice: ")
            if choice == "1":
                editContent = input("Your new caption: ")
                if editContent:
                    self.editCaption(editContent)
            elif choice == "2":
                commentContent = input("Your comment: ")
                # Create comment chid
                if commentContent.split(" ")[0] == "cd": 
                    try:
                        command = commentContent.split(" ", 2)
                        # Check sibling exist?
                        if self.checkExistCommentId(int(command[1])):
                            # Find sibling
                            commentSibling = self.commentTree.get_last_sibling_of_parent(int(command[1]))
                            # Case 1: Comment has parent, does not have sibling
                            if commentSibling == None:
                                comment_child = self.createComment(self.postId, command[2], None, None, False)
                                self.updateComment(int(command[1]), None, None, comment_child) # Update child comment into parent comment
                            # Case 2: Comment has parent and sibling
                            else:
                                comment_child = self.createComment(self.postId, command[2], None, None, False)
                                self.updateComment(int(commentSibling), None,comment_child, None ) # Update child comment, sibling_comment into parent comment
                                print(f"CommentChild: {comment_child}")
                                input()
                    except ValueError:
                        print("Invalid command")
                        input("Press any key to continue")
                # Create comment root sibling
                elif commentContent.split(" ")[0] == "root":
                    command = commentContent.split(" ", 1)
                
                    comment_root_sibling_id = self.findCommentRootSiblingId(int(self.postId)) # Find parent comment by Id
                    comment = self.createComment(self.postId, command[1], None, None, True)
                    if comment_root_sibling_id:
                        self.updateComment(comment_root_sibling_id, None, comment, None) # Update child comment, sibling_comment into parent comment
                else:
                    print("Invalid command")
                    input("Press any key to continue")
                self.getComment()

    def getComment(self):
        self.commentTree = self.detailRepo.getAllCommentByPostId(self.postId, 'tree')
        return self.commentTree
    
    def createComment(self, postId, commentContent, commentSibling, commentChild, isRoot):
        return self.detailRepo.insertComment(postId, commentContent, commentSibling, commentChild, isRoot)

    def editCaption(self, editContent):
        self.detailRepo.updatePost(self.postId, editContent)

    def updateComment(self, commentId, commentContent, commentSibling, commentChild):
        self.detailRepo.updateComment(commentId, commentContent, commentSibling, commentChild)

    def findCommentRootSiblingId(self, postId):
        return self.detailRepo.findCommentRootSiblingId(postId)
    
    def checkExistCommentId(self, commentId: int):
        return self.detailRepo.checkExistCommentId(commentId)

    def getPostCaption(self, postId):
        return self.detailRepo.getPostCaption(postId)