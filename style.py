import os

class BoxStyle:
    def __init__(self, textList: list):
        """
        Initialize a new Box with the given text and console width.

        :param text: The text to display in the box.
        :param console_width: The width of the console window.
        """
        self.textList = textList
        self.console_width = os.get_terminal_size().columns

    def print(self):
        """
        Print the box with the stored text.
        """
        box_length = len(self.find_max_string(self.textList)) + 4
        if box_length > self.console_width:
            box_length = self.console_width

        # Print the top of the box
        print("+" + "-" * box_length + "+")

        for i in self.textList:
            # Print the text
            space = int(box_length - 2 - len(str(i)))
            print("| " + str(i) + " " *space +" |")

        # Print the bottom of the box
        print("+" + "-" * box_length + "+")
    
    def find_max_string(self, textList:list):
        text_max = str(textList[0])
        for text in textList:
            if len(str(text)) > len(str(text_max)):
                text_max = str(text)
        return str(text_max)

from DataStructure.Tree.CommentKAryTree import * 

class CommentTreeStyle:
    def __init__(self, comment_tree: CommentKaryTree):
        self.comment_tree = comment_tree
        self.node = self.comment_tree.root  

    def print_tree(self, node, prefix="", is_last=True):
        if node is not None:
            # Print node
            print(prefix + ("" if is_last else "└── ") + str(node.commentId) + " - " + node.commentContent)

            # Update the prefix for children
            new_prefix = prefix + ("    " if is_last else "│   ")

            # Print child node recursively
            self.print_tree(node.firstChild, new_prefix, False)

            # Print sibling node recursively
            if node.isRoot:
                self.print_tree(node.nextSibling, "", True )
            else: self.print_tree(node.nextSibling, prefix , False)