import numpy as np

a1 = np.arange(10)
print(a1)

a5 = np.full((2,3), 8) # array of rank 2 with all 8s
print(a5)

a6 = np.eye(4) # 4x4 identity matrix
print(a6)

a5 = np.full((2,3), 8) # array of rank 2 with all 8s
print(a5)

a7 = np.random.random((2,4)) # rank 2 array (2 rows 4 columns) with
# random values
# in the half-open interval [0.0, 1.0)
print(a7)

list1 = [1,2,3,4,5]
a8 = np.array(list1)

print(a8)

a5 = np.full((2,3), 8) # array of rank 2 with all 8s
print(a5)

a = np.array([[1,2,3,4,5],
[4,5,6,7,8],
[9,8,7,6,5]]) # rank 2 array

b4 = a[2:, :] # row 2 onwards and all columns
print(b4)
print(b4.shape)
