import numpy as np
import warnings

def swapRows(A, i, j):
    """
    interchange two rows of A
    operates on A in place
    """
    tmp = A[i].copy()
    A[i] = A[j]
    A[j] = tmp

def relError(a, b):
    """
    compute the relative error of a and b
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        try:
            return np.abs(a-b)/np.max(np.abs(np.array([a, b])))
        except:
            return 0.0

def rowReduce(A, i, j, pivot):
    """
    reduce row j using row i with pivot pivot, in matrix A
    operates on A in place
    """
    factor = A[j][pivot] / A[i][pivot]
    for k in range(len(A[j])):
        if np.isclose(A[j][k], factor * A[i][k]):
            A[j][k] = 0.0
        else:
            A[j][k] = A[j][k] - factor * A[i][k]


# stage 1 (forward elimination)
def forwardElimination(B):
    """
    Return the row echelon form of B
    """
    A = B.copy().astype(float)
    m, n = np.shape(A)
    for i in range(m-1):
        # Let lefmostNonZeroCol be the position of the leftmost nonzero value 
        # in row i or any row below it 
        leftmostNonZeroRow = m
        leftmostNonZeroCol = n
        ## for each row below row i (including row i)
        for h in range(i,m):
            ## search, starting from the left, for the first nonzero
            for k in range(i,n):
                if (A[h][k] != 0.0) and (k < leftmostNonZeroCol):
                    leftmostNonZeroRow = h
                    leftmostNonZeroCol = k
                    break
        # if there is no such position, stop
        if leftmostNonZeroRow == m:
            break
        # If the leftmostNonZeroCol in row i is zero, swap this row 
        # with a row below it
        # to make that position nonzero. This creates a pivot in that position.
        if (leftmostNonZeroRow > i):
            swapRows(A, leftmostNonZeroRow, i)
        # Use row reduction operations to create zeros in all positions 
        # below the pivot.
        for h in range(i+1,m):
            rowReduce(A, i, h, leftmostNonZeroCol)
    return A

#################### 

# If any operation creates a row that is all zeros except the last element,
# the system is inconsistent; stop.
def inconsistentSystem(A):
    """
    B is assumed to be in echelon form; return True if it represents
    an inconsistent system, and False otherwise
    """
    # get shape of array
    rows, cols = np.shape(A)
    # get zeroes of the last row
    non_zeroes = np.nonzero(A[-1])
    # have to do zeroes[0] to access the actual array
    len_non_zeroes = len(non_zeroes[0])
    # if the length of zeroes is greater than 1 or is 0 it can't be inconsistent
    if len_non_zeroes > 1 or len_non_zeroes == 0:
        return False
    # We know there is only 1 element by now so if it's equal to the last col then its inconsistent
    elif non_zeroes[0][0] == (cols - 1):
        return True
    # if the nonzero is not in the end col then its consistent cause x * 0 = 0
    return False



def backsubstitution(B):
    """
    return the reduced row echelon form matrix of B
    """
    rows, cols = np.shape(B)
    # Beginning with the rightmost pivot and working upward and left
    # the rightmost pivot will be in the bottomest nonzero row
    for i in range(rows - 1, -1, -1):
        non_zeroes = np.nonzero(B[i])
        if len(non_zeroes[0]) == 0:
            continue
        # we can assume its consistent because it will be checked before this function
        # get the first non_zero
        pivot_pos = non_zeroes[0][0]
        # if it's not already 1, make it 1
        if B[i][pivot_pos] != 1.0:
            B[i] /= B[i][pivot_pos]
        # reduce rows accordingly
        for j in range(i - 1, -1, -1):
            rowReduce(B, i, j, pivot_pos)
    return B





    # if pivot isn't 1 make it 1 through scaling
    # create zeros above each pivot

#####################

A = np.array([[2, 2, 6, 0], 
              [5, -4, -3, 5], 
              [2, 1, 4, -4]])
B = np.array( [[ 1, 6, 1,-1, 4], [-5, 4, 1, 0,-5], [-6, 4,-2, 3,-3], [ 5,-3,-2, 0,-4]] )
print(A)
AEchelon = forwardElimination(B)
if (not inconsistentSystem(AEchelon)):
    AReducedEchelon = backsubstitution(AEchelon)
    print(AReducedEchelon)
else:
    print("inconsistent")

