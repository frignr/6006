def catwidth(n, s1, s2, connections):
    """
    Given a list containing triples (i, j, w) representing the bandwidth w 
    between servers i and j, return the catwidth between them.
    Input: 
        'n' is the number of servers
        'connections' is a list of triples (i, j, w) 
        i, j, 's1', 's2' are server IDs, while w are bandwidth values
        Servers IDs are unique numbers in range [0,n-1]
    Output: 
        'cw' is the catwidth between servers i and j
    """
    
    cw = 0
    ############################
    #  Part (c): Implement me  #
    ############################
    nodeCW = {}
    output = {}
    edges = {}
    for x in range (0, n):
        nodeCW[x] = 0
        output[x] = 0
        edges[x] = []
        
    
    for e in connections:
        edges[e[0]].append((e[1], e[2]))
        edges[e[1]].append((e[0], e[2]))

    nodeCW[s1] = float('infinity')
    while len(nodeCW) != 0:
        currentNode = max(nodeCW, key=nodeCW.get)
        for e in edges[currentNode]:
            if e[1] > nodeCW[currentNode]:
                currentCW = nodeCW[currentNode]
            else:
                currentCW = e[1]

            if e[0] in nodeCW:
                if currentCW> nodeCW[e[0]]:
                    nodeCW[e[0]] = currentCW
            if e[0] not in output:
                output[e[0]]= currentCW
            else:
                if currentCW> output[e[0]]:
                    output[e[0]] = currentCW
        del nodeCW[currentNode]
   
    return output[s2]

##################
# Test your code #
##################
def test_on_case(case):
    with open('cases/' + str(case) + '.in', 'r') as f:
        s = f.read()
    lines = s.split('\n')
    parameters = [[int(i) for i in line.split(' ')] for line in lines]
    n, s1, s2 = parameters[0]
    connections = parameters[1:]
    cw = catwidth(n, s1, s2, connections)
    with open('cases/' + str(case) + '.out', 'r') as f:
        golden = int(f.read())
    print(golden)
    print(cw)
    if cw == golden:
        print('Passed test case ' + str(case) + '!')
    else:
        print('Failed test case ' + str(case) + '... :(')

if __name__ == '__main__':
    for case in [1, 2, 3]:
        test_on_case(case)
