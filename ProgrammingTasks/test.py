
class Node:
            def __init__(self,value,left=None,right=None):
                self.value = value
                self.left = left
                self.right = right
            def __str__(self):
                return "Node (" + str(self.value) + ")"

def walk(tree):
                    if tree is not None:
                        print(tree)
                    walk(tree.left)
                    walk(tree.right)