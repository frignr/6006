from math import ceil

class MinPriorityQueue:
    def __init__(self):     # initialize
        self.A = []         # list where heap is stored

    def best(self):         # returns best, without modifying heap
        if len(self.A) < 1:
            return None     # return None if queue empty
        return self.A[0]

    def insert(self, v):    # inserts v, maintaining heap
        self.A.append(v)
        node = len(self.A) - 1
        parent = (node - 1) // 2 
        while (0 <= parent) and (self.A[node] < self.A[parent]):
            self.A[parent], self.A[node] = self.A[node], self.A[parent]
            node = parent
            parent = (node - 1) // 2

    def extract_best(self): # removes best, maintaining heap
        if len(self.A) < 1:
            return None     # return None if queue empty
        node = 0
        out = self.A[node]
        self.A[node] = self.A[-1]
        self.A.pop()
        while True:
            left  = 2 * node + 1
            right = 2 * node + 2
            best = node
            if right < len(self.A) and self.A[right] < self.A[best]:
                best = right
            if left  < len(self.A) and self.A[left]  < self.A[best]:
                best = left
            if node != best:
                self.A[best], self.A[node] = self.A[node], self.A[best]
                node = best
            else:
                return out

class MaxPriorityQueue:
    def __init__(self):     # Implement me
        self.A = []         #Initialization of storage array
    def best(self):         # Implement me
        if len(self.A) < 1:
            return None     # return None if queue empty
        return self.A[0]
    def insert(self, v):    # Implement me
        self.A.append(v)
        node = len(self.A) - 1
        parent = (node - 1) // 2 
        while (0 <= parent) and (self.A[node] > self.A[parent]):
            self.A[parent], self.A[node] = self.A[node], self.A[parent]
            node = parent
            parent = (node - 1) // 2
    def extract_best(self): # Implement me
        if len(self.A) < 1:
            return None     # return None if queue empty
        node = 0
        out = self.A[node]
        self.A[node] = self.A[-1]
        self.A.pop()
        while True:
            left  = 2 * node + 1
            right = 2 * node + 2
            best = node
            if right < len(self.A) and self.A[right] > self.A[best]:
                best = right
            if left  < len(self.A) and self.A[left]  > self.A[best]:
                best = left
            if node != best:
                self.A[best], self.A[node] = self.A[node], self.A[best]
                node = best
            else:
                return out

class RPriorityQueue:
    def __init__(self, r):  # Implement me
        self.r = r          # r should not change after initialization
        self.left = MaxPriorityQueue()       # Max priority queue should be less than middle
        self.leftSize = 0
        self.right = MinPriorityQueue() #Min priority queue should be greater than middle
        self.rightSize = 0
        self.size = 0
        self.middle = 0
    def best(self):         # Implement me
        if self.size < 1:
            return None
        return self.middle
    def insert(self, v):    # Implement me
        if self.size == 0:
            self.middle = v
            self.size = 1
        else:
            self.size += 1
            if v <= self.middle:
                self.left.insert(v)
                self.leftSize += 1
                if self.leftSize >= ceil(self.size * self.r) :
                    self.right.insert(self.middle)
                    self.rightSize += 1
                    self.middle = self.left.extract_best()
                    self.leftSize -= 1
            else:
                self.right.insert(v)
                self.rightSize += 1
                if self.leftSize < ceil(self.size * self.r) - 1:
                    self.left.insert(self.middle)
                    self.leftSize += 1
                    self.middle = self.right.extract_best()
                    self.rightSize -= 1
##
##        print(self.leftSize, self.rightSize, self.size)
##            if self.leftSize >= (ceil(self.size*self.r) - 1 ): #max queue is big enough add to min queue
##                print("in min queue", v)
##                if v >= self.middle:
##                    self.right.insert(v)
##                    self.rightSize +=1
##                else:
##                    self.right.insert(self.middle)
##                    self.rightSize += 1
##                    self.middle = v
##            else: #Otherwise there is room in max queue
##                print("in max queue", v)
##                if v <= self.middle:
##                    self.left.insert(v)
##                    self.leftSize+=1
##                else:
##                    self.left.insert(self.middle)
##                    self.leftSize +=1
##                    self.middle = v

                    
    def extract_best(self): # Implement me
        if self.size < 1:
            return None     # return None if queue empty
        out = self.middle
        self.size -= 1
        if self.leftSize >= ceil(self.size*self.r):
            if self.leftSize > 0:
##                print("from max queue")
                self.middle = self.left.extract_best()
                self.leftSize -=1
        else:
            if self.rightSize > 0:
##                print("from min queue")
                self.middle = self.right.extract_best()
                self.rightSize -=1
        if self.size == 0:
            self.middle = None
        return out
    

##################
# Test your code #
##################
def parse_input(s):
    ops = s.split('\n')[:-1]
    for i in range(len(ops)):
        ops[i] = ops[i].split(' ')
        if 1 < len(ops[i]):
            ops[i] = [ops[i][0], int(ops[i][1])]
    return ops

def out_from_in(kind, ops):
    # outputs return values from best() and extract_best() on separate lines
    if kind == 'min':
        q = MinPriorityQueue()
    elif kind == 'max':
        q = MaxPriorityQueue()
    elif kind[0] == 'r':
        r = float(kind[1:])
        q = RPriorityQueue(r)
    else:    
        print('kind not recognized... :(')
        return ''
    s = ''
    for op in ops:
        if op[0] == 'insert':
            q.insert(op[1])
        if op[0] == 'best':
            best = q.best()
            s += str(best) + ' '
        if op[0] == 'extract_best':
            best = q.extract_best()
            s += str(best) + ' '
    return s

def test_queue_on_case(kind, case):
    with open('cases/' + str(case) + '.in', 'r') as f:
        s = out_from_in(kind, parse_input(f.read()))
    with open('cases/' + str(case) + kind + '.out', 'r') as f:
        if s == f.read():
            print(f'{kind} queue passed test case {case}!')
        else:
            print(f'{kind} queue failed test case {case}... :(')

if __name__ == '__main__':
    for case in [1, 2]:
        for kind in ['min', 'max', 'r0.5', 'r0.4', 'r0.8']:
            test_queue_on_case(kind, case)
