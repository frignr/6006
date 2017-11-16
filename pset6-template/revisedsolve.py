def solve_special(C):

    
    #Setting up adjacency list
    adjList = {}
    visited = [0] * len(C)  #0 if not visited, 1 if temp visited, 2 if permanent
    topList = []    #List to store nodes in topological order
    
    def dfs(node):
        if visited[node] == 2:
            return
        if visited[node] == 1:
            raise ValueError('cyclic')
        visited[node] = 1
        for x in adjList[node]:
            dfs(x)

        visited[node] = 2
        topList.insert(0, node)
        return
            
    for i in range(len(C)):
        adjList[i] = []

    
    starts = []         #Stores variables without dependency
    #Build the adjacency list while checking for delegatedness and a bit of specialness
    for i in range(len(C)):
        iStart = True       #Stores whether this node can be a start node ie no dependencies
        
        for j in range(len(C)):  
            if i != j :
                if C[i][j+1] != 0:
                    iStart = False
                    adjList[j].append(i)
                    
            #Check for delegatedness
            if i == j:
                if C[i][j+1] != -1:
                    print("Not delegated")
                    return None

        if iStart == True:
            starts.append(i)

    if len(starts) == 0:
        print("Not special")
        return None

    for x in starts:
        try:
            dfs(x)
        except ValueError as err:
            print(err.ergs)
            return None

    answer = [0] * len(C)
    for x in topList:
        answer[x] = C[x][0]
        for i in range(len(C)):
            if i != x:
                answer[x] = answer[x] + (C[x][i+1] * answer[i])

    return answer
        
    """
    Given a set of linear equations C, returns a solving assignment to variables
    if the set of equations is delegated and special, and None otherwise
    Input: 
        C is a list of n lists, each with length n + 1
        C_i = [d_i, c_i1, c_i2, ... c_in]
        C_i represents equation:  0 = d_i + \sum_j c_ij * x_j
    Output: 
        x = [x_1, ... x_n] 
        solving assignment of variables
    """

##################
# Test your code #
##################
def test_on_case(case):
    with open('cases/' + str(case) + '.in', 'r') as f:
        s = f.read()
        C = s.split('\n')
        n = len(C)
        for i in range(n):
            C[i] = C[i].split(' ')
            for j in range(n + 1):
                C[i][j] = int(C[i][j])
        x = solve_special(C)
    with open('cases/' + str(case) + '.out', 'r') as f:
        golden = f.read()
        if golden == 'None':
            golden = None 
        else:
            golden = [int(i) for i in golden.split(' ')]
        print(golden)
        print(x)
        if x == golden:
            print('Passed test case ' + str(case) + '!')
        else:
            print('Failed test case ' + str(case) + '... :(')

if __name__ == '__main__':
    for case in [1, 2]:
        test_on_case(case)
