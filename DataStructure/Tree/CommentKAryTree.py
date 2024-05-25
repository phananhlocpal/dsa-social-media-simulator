class CommentNode:
    def __init__(self, commentId: int, commentContent:str, isRoot:bool):
        """
        Initialize a new Node with the given comment.

        :param commentId: The ID of the comment.
        :param commentContent: The content of the comment.
        """
        self.commentId = commentId
        self.commentContent = commentContent
        self.firstChild = None
        self.nextSibling = None
        self.isRoot = isRoot

class CommentKaryTree:
    def __init__(self):
        """
        Initialize an empty k-ary tree.
        """
        self.root = None

    def build_tree(self, comment_list):
        """
        Build a k-ary tree from a list of comments.

        :param comment_list: A list of comments where each comment is a tuple
                             containing (comment_id, comment_content, comment_sibling,
                             comment_child, isRoot).
        """
        if not comment_list:
            return

        # Create a dictionary to map comment_id to CommentNode
        nodes = {}
        for comment in comment_list:
            comment_id = comment[0]
            comment_content = comment[2]
            isRoot = comment[5]
            nodes[comment_id] = CommentNode(comment_id, comment_content, isRoot)

        # Set up the tree structure
        root_found = False
        for comment in comment_list:
            comment_id = comment[0]
            comment_sibling = comment[3]
            comment_child = comment[4]
            is_root = comment[5]

            node = nodes[comment_id]

            if is_root and not root_found:
                self.root = node
                root_found = True

            if comment_sibling is not None:
                node.nextSibling = nodes[comment_sibling]

            if comment_child is not None:
                node.firstChild = nodes[comment_child]

    def get_root(self):
        """
        Get the root of the k-ary tree.

        :return: The root node of the tree.
        """
        return self.root

    def get_last_sibling_of_parent(self, commendParentId: int):
        """
        Get the last sibling node of a specified parent node.

        :param commendParentId: The ID of the parent node.
        :return: The last sibling node of the parent node, or None if the parent node does not exist.
        """
        parent_node = self.find_node_by_id(commendParentId)
        if parent_node is None:
            return None

        last_sibling = parent_node.firstChild
        while last_sibling and last_sibling.nextSibling:
            last_sibling = last_sibling.nextSibling

        if last_sibling:
            return int(last_sibling.commentId)
        else: return None

    def find_node_by_id(self, commentId: int, node:CommentNode=None):
        """
        Find a node in the tree by its ID.

        :param commentId: The ID of the node to find.
        :param node: The node to start the search from. Default is the root node.
        :return: The node with the specified ID, or None if the node does not exist.
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        if node.commentId == commentId:
            return node

        # Recursively search in the children of the current node
        child = node.firstChild
        while child:
            found_node = self.find_node_by_id(commentId, child)
            if found_node:
                return found_node
            child = child.nextSibling

        return None