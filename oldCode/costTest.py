import scipy.optimize

mat = [[1,2,3],
        [3,2,1],
        [1,3,2]]
print(scipy.optimize.linear_sum_assignment(mat))
#first array is row indices, second is columns, this gives total cost of 4 (which is minimum!)
