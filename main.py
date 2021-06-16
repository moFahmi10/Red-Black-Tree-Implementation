import sys


class RBnode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1


class RBtree():
    def __init__(self):
        self.TNULL = RBnode(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.key) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def get_root(self):
        return self.root

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        # If parent of x is null then x was the root and y will be the root
        if x.parent == None:
            self.root = y
        # Else If x was the left child of its parent, set y to be the left of the parent
        elif x == x.parent.left:
            x.parent.left = y
        # Else if x was the right child of its parent, set y to be the right child of the parent
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, node):
        # Repeats while color of parent to the node is red
        while node.parent.color == 1:
            # If the parent of the node is the right child
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right

                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = 0

    def insert(self, key):
        node = RBnode(key)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        # Traverse the tree to find the position to insert the node
        while x != self.TNULL:
            # Y is a pointer to x
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        # Y is a pointer to the parent of the inserted node
        node.parent = y
        # If the parent to the item is none then this item is the root of the tree
        if y is None:
            self.root = node
        # Put the inserted item to the left or right of its parent according to its value
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        # If the node inserted is the root, then color it black and the insertion is done
        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return
        # If the parent of the inserted node is red then we call fix_insert to fix the RB tree according to its
        # properties
        self.fix_insert(node)

    def height(self, node):
        if node == self.TNULL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def size(self, node):
        if node == self.TNULL:
            return 0
        return 1 + self.size(node.left) + self.size(node.right)

    def search(self, node, key):
        if node == self.TNULL or key == node.key:
            return node.key
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

rbt = RBtree()
dictf = open('EN-US-Dictionary.txt', 'r')
dictionary = dictf.read().splitlines()
for word in dictionary:
    rbt.insert(word)
while True:
    choice = input('1- SIZE\n2- INSERT\n3- LOOK UP\n4- TREE HEIGHT\n5- QUIT\n\nEnter the number associated with your choice: ')
    if choice == '1':
        print(f'\nDictionary size: {rbt.size(rbt.get_root())}\n')
    elif choice == '2':
        word = input('\nEnter word you want to insert: ')
        found = rbt.search(rbt.get_root(), word) == word
        if found:
            print('\nERROR: Word already in the dictionary!\n')
        elif not found:
            rbt.insert(word)
            print(f'\nDictionary size: {rbt.size(rbt.get_root())}\n')
            print(f'Dictionary height: {rbt.height(rbt.get_root())}\n')
    elif choice == '3':
        word = input('\nEnter word you want to look up: ')
        found = rbt.search(rbt.get_root(), word) == word
        if found:
            print('\nYES\n')
        elif not found:
            print('\nNO\n')
    elif choice == '4':
        print(f'\nDictionary height: {rbt.height(rbt.get_root())}\n')
    elif choice == '5':
        break
    else:
        print('\nPlease enter a valid choice (1-5)\n')
dictf.close()