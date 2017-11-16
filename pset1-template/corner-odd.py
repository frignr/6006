def smallest_corner_odd(A, r = None):
    '''
    Input: 2D array A, subarray indices ((px, py), (qx, qy))
    Output: a smallest corner-odd subarray if the input
        subarray is corner-odd, else return None.
        Your output should be a tuple of tuples
        representing the indices of the upper left
        and lower right corners of the subarray.
    '''
    n, m = len(A[0]), len(A)
    if r is None:
        r = ((0, 0), (n - 1, m - 1))
    (px, py), (qx, qy) = r # (upper left), (lower right)
    ##################
    # YOUR CODE HERE #
    ##################

    if ((A[py][px] + A[py][qx] + A[qy][px] + A[qy][qx]) % 2 ==0):
        return None
    #Reduce the x dimension to 2
    while (qx - px >= 2):
        mx = px + int((qx - px)/2) #column in the middle
        if((A[py][mx] + A[qy][mx])%2 == 1): #Ends of the middle sum to odd
            if((A[py][px] + A[qy][px])% 2 == 0):
                qx = mx
            else:
                px = mx
        else: #Ends of the middle some to even
            if((A[py][px] + A[qy][px])% 2 == 1):
                qx = mx
            else:
                px = mx

    #Reduce the y dimension to 2
    while (qy - py > 1):
        my = py + int((qy - py)/2)
        if((A[my][px] + A[my][qx])%2 == 1):
            if((A[py][px] + A[py][qx])% 2 == 0):
                qy = my
            else:
                py = my
        else:
            if((A[py][px] + A[py][qx])% 2 == 1):
                qy = my
            else:
                py = my

    return [[px,py],[qx,qy]]

##################
# Test your code #
##################
def parse_2D_int_array(s):
    return [[int(v) for v in line.split()] for line in s.split('\n')[:-1]]

def test():
    with open('cases/1.in', 'r') as f:
        A = parse_2D_int_array(f.read())
        print(smallest_corner_odd(A))
        # [[4, 2], [5, 3]] would be a correct output for test case 1.in
    with open('cases/2.in', 'r') as f:
        A = parse_2D_int_array(f.read())
        print(smallest_corner_odd(A))
        # --None-- would be a correct output for test case 2.in

if __name__ == '__main__':
    test()

