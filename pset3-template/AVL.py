class BST(object):
    def __init__(self, key = None, parent = None):
        "Initializes a BST node"
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def find_min(self):
        "Returns min of self's subtree, or self if no key"
        if self.key is None:
            return None
        node = self
        while node.left is not None:
            node = node.left
        return node
  
    def find(self, key): 
        "Returns node with key in self's subtree if exists, else None"
        node = self
        while (node is not None) and (node.key != key):
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def find_next(self): 
        "Returns node with smallest key larger than self if exists, else None"
        if self.right is not None:
            return self.right.find_min() 
        node = self.parent
        while (node is not None) and (node.key < self.key):
            node = node.parent
        return node

    def insert(self, key):
        "Inserts key into self's subtree and returns its node"
        if self.key is None:
            self.key = key
        node = self
        while node.key is not key:
            if key < node.key:
                if node.left is None:
                    node.left = self.__class__(key, node)
                node = node.left
            else:
                if node.right is None:
                    node.right = self.__class__(key, node)
                node = node.right
        return node

    def replace(self, node):
        "Replaces self's key, left, and right with node's key, left, and right"
        self.key = node.key
        self.left = node.left
        self.right = node.right
        if self.left is not None:
            self.left.parent = self
        if self.right is not None:
            self.right.parent = self
        
    def delete(self):
        "Deletes self's key from subtree and returns parent of removed node"
        node = self
        if (self.left is not None) and (self.right is not None):
            node = self.right.find_min()
            self.key = node.key
        if node.right is not None:
            node.replace(node.right)
        elif node.left is not None:
            node.replace(node.left)
        else:
            if node.parent is None:
                node.key = None
            elif node.parent.right is node:
                node.parent.right = None
            elif node.parent.left is node:
                node.parent.left = None
        return node

    def __str__(self):
        "Returns ASCII drawing of the tree"
        s = str(self.key)
        if (self.left is not None) or (self.right is not None):
            ws = len(s)
            sl, wl, cl = [''], 0, 0
            if self.left is not None:
                sl = str(self.left).splitlines()
                wl = len(sl[0])
                cl = len(sl[0].lstrip(' _'))
            sr, wr, cr = [''], 0, 0
            if self.right is not None:
                sr = str(self.right).splitlines()
                wr = len(sr[0])
                cr = len(sr[0].rstrip(' _'))
            while len(sl) < len(sr):
                sl.append(' ' * wl) 
            while len(sr) < len(sl):
                sr.append(' ' * wr)
            s = s.rjust(ws + cl, '_').ljust(ws + cl + cr, '_')
            s = [s.rjust(ws + wl + cr).ljust(ws + wl + wr)]
            s = '\n'.join(s + [l + (' ' * ws) + r for (l,r) in zip(sl, sr)])
        return s

class AVL(BST):
    def __init__(self, key = None, parent = None):
        "Augments BST to include height and skew"
        super().__init__(key, parent)
        self.height = -1
        self.skew = 0

    def insert(self, key):
        "Modifies BST insert to rebalance after insertion"
        node = super().insert(key)
        node.rebalance()
        return node

    def delete(self):
        "Modifies BST delete to rebalance after deletion"
        node = super().delete()
        node.rebalance()
        return node

    def update(self):
        "Updates height and skew at self"
        left_height  = -1 if (self.left  is None) else self.left.height
        right_height = -1 if (self.right is None) else self.right.height
        self.height = max(left_height, right_height) + 1
        self.skew = right_height - left_height

    def right_rotate(self):
        "Rotates left to right, assuming left is not None "
        node, a, b, c = self.left, self.left.left, self.left.right, self.right
        self.key, node.key = node.key, self.key
        if a is not None:
            a.parent = self
        if c is not None:
            c.parent = node
        self.left, self.right = a, node
        node.left, node.right = b, c
        node.update()
        self.update()

    def left_rotate(self):
        "Rotates right to left, assuming right is not None"
        node, a, b, c = self.right, self.left, self.right.left, self.right.right
        self.key, node.key = node.key, self.key
        if a is not None:
            a.parent = node
        if c is not None:
            c.parent = self
        self.left, self.right = node, c
        node.left, node.right = a, b
        node.update()
        self.update()

    def rebalance(self):
        "Fixes AVL balance at self and ancestors"
        node = self
        while node is not None:
            node.update()
            if node.skew == 2:
                if node.right.skew == -1:
                    node.right.right_rotate() 
                node.left_rotate()
            elif node.skew == -2:
                if node.left.skew == 1:
                    node.left.left_rotate() 
                node.right_rotate()
            node = node.parent

##################
# Test your code #
##################
def test_random_insert_delete(tree, population, num_insert, num_delete):
    from random import sample, choice
    print('\n*\nBuilding new tree on ' + str(num_insert) + ' random keys\n*\n')
    keys = sample(population, num_insert)
    print('Keys: ' + str(keys))
    for key in keys:
        tree.insert(key)
        print('\nInserting ' + str(key) + '...\n')
        print(tree) 
    print('\n*****\nNow deleting ' + str(num_delete) + ' random keys\n****')
    print('Keys: ' + str(keys))
    for i in range(num_delete):
        key = choice(population)
        print('\n*\nAttemping to remove ' + str(key) + '...\n*')
        node = tree.find(key)
        if node is None:
            print('\n' + str(key) + ' not found... :(')
        else:
            node.delete()
            print('\n' + str(key) + ' removed!\n')
            print(tree)

def test_BST(max_key, num_inserts, num_deletes):
    print('\n***********\nTesting BST\n***********')
    tree = BST()
    test_random_insert_delete(tree, range(max_key), num_inserts, num_deletes)
    print('\n*\nTest worst case: inserting 10 keys in order\n*\n')
    tree = BST()
    for i in range(max_key):
        tree.insert(i)
    print(tree)

def test_AVL(max_key, num_inserts, num_deletes):
    print('\n***********\nTesting AVL\n***********')
    tree = AVL()
    test_random_insert_delete(tree, range(max_key), num_inserts, num_deletes)

if __name__ == '__main__':
    test_BST(10, 10, 5)
    test_AVL(10, 10, 5)
