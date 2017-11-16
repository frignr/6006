from AVL import AVL

class Transaction():
    def __init__(self, shares, price):
        self.shares = shares
        self.price = price
        #############################################
        # Part (a): Add any additional storage here #
        #############################################
        self.sharesIST = shares     #number of shares in this subtree
    
    def __lt__(self, other):
        "Evaluate comparison between two transactions: (self < other)"
        ##########################
        # Part (b): Implement me #
        ##########################
        if self.price < other.price:
            return True         # return a boolean
        else:
            return False

    def __str__(self):
        return str(self.shares) + '@' + str(self.price)

class TransactionLog(AVL):
    def add_transaction(self, shares, price):
        "Adds a transaction to the transaction log"
        node = super().insert(Transaction(shares, price))

    def update(self):
        "Augments AVL update() to fix any properties calculated from children"
        super().update()
        #################################################
        # Part (a): Add any additional maintenence here #
        #################################################
        self.key.sharesIST = self.key.shares
        if self.left is not None:
            self.key.sharesIST += self.left.key.sharesIST
        if self.right is not None:
            self.key.sharesIST += self.right.key.sharesIST

    def sold_in_range(self, range_min, range_max):
        "Returns the number of shares sold within an inclusive price range"
        if self.key is None:
            return 0
        count = 0
        ##########################
        # Part (d): Implement me #
        ##########################
        #Finding a node within the range
        node = self
        while node.key.price > -range_min or node.key.price < -range_max:
            if node.key.price > -range_min:
                node = node.left
                if node is None:
                    return 0
            elif node.key.price <-range_max:
                node = node.right
                if node is None:
                    return 0
##        if node.key.price > -range_min:
##            while node.key.price > -range_min:
##                node = node.left
##                if node is None:
##                    return 0
##        elif node.key.price < -range_max:
##            while node.key.price < -range_max:
##                node = node.right
##                if node is None:
##                    return 0
        count = node.key.sharesIST
        

        #Going down the left side and subtracting from count number of shares outside range
        leftNode = node.left
        while leftNode is not None:
            if leftNode.key.price < -range_max:
                count -= leftNode.key.sharesIST
                if leftNode.right is not None:
                    count += leftNode.right.sold_in_range(range_min, range_max)
                break
            leftNode = leftNode.left

        #Same with right side
        rightNode = node.right
        while rightNode is not None:
            if rightNode.key.price > -range_min:
                count -= rightNode.key.sharesIST
                if rightNode.left is not None:
                    count += rightNode.left.sold_in_range(range_min, range_max)
                break
            rightNode = rightNode.right


        return count
        
    def bought_in_range(self, range_min, range_max):
        "Returns the number of shares bought within an inclusive price range"
        if self.key is None:
            return 0
        count = 0
        ##########################
        # Part (d): Implement me #
        ##########################

        #Finding a node within the range
        node = self

        while node.key.price > range_max or node.key.price < range_min:
            if node.key.price > range_max:
                node = node.left
                if node is None:
                    return 0
            elif node.key.price <range_min:
                node = node.right
                if node is None:
                    return 0
                
##        if node.key.price > range_max:
##            while node.key.price > range_max:
##                node = node.left
##                if node is None:
##                    return 0
##        elif node.key.price < range_min:
##            while node.key.price < range_min:
##                node = node.right
##                if node is None:
##                    return 0
        count = node.key.sharesIST
        

        #Going down the left side and subtracting from count number of shares outside range
        leftNode = node.left
        while leftNode is not None:
            if leftNode.key.price < range_min:
                count -= leftNode.key.sharesIST
                if leftNode.right is not None:
                    count += leftNode.right.bought_in_range(range_min, range_max)
                break
            leftNode = leftNode.left

        #Same with right side
        rightNode = node.right
        while rightNode is not None:
            if rightNode.key.price > range_max:
                count -= rightNode.key.sharesIST
                if rightNode.left is not None:
                    count += rightNode.left.bought_in_range(range_min, range_max)
                break
            rightNode = rightNode.right

        
        return count


##################
# Test your code #
##################
def parse_input(s):
    ops = s.split('\n')
    for i in range(len(ops)):
        ops[i] = ops[i].split(' ')
        for j in range(1, len(ops[i])):
            ops[i][j] = int(ops[i][j])
    return ops

def out_from_in(ops):
    # outputs return values from range queries on separate lines
    t = TransactionLog()
    outs = []
    for i, op in enumerate(ops):
        if op[0] == 'add':
            t.add_transaction(op[1], op[2])
        if op[0] == 'bought':
            n = t.bought_in_range(op[1], op[2])
            outs.append(str(n))
        if op[0] == 'sold':
            n = t.sold_in_range(op[1], op[2])
            outs.append(str(n))
    return ' '.join(outs)

def test_on_case(case):
    with open('cases/' + str(case) + '.in', 'r') as f:
        s = f.read()
        out = out_from_in(parse_input(s))
    with open('cases/' + str(case) + '.out', 'r') as f:
        golden = f.read()
        print(golden)
        print(out)
        if out == golden:
            print('Passed test case ' + str(case) + '!')
        else:
            print('Failed test case ' + str(case) + '... :(')

if __name__ == '__main__':
    for i in [1, 2]:
        test_on_case(i)
