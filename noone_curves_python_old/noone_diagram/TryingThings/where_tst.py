# Python program explaining 
# where() function 

import numpy as np 

# a is an array of integers. 
a = np.array([[1, 2, 3], [4, 5, 6]]) 

print(a) 

print ('Indices of elements <4') 

b = np.where(a<4) 
print(b) 

print("Elements which are <4") 
print(a[b]) 

# example 2:

a = np.array([1,2,3,4,5,6,7,8,9,10])
print(a[np.where(a<4)])

b = np.where(a > 4)

c=a*a

c

--> array([  1,   4,   9,  16,  25,  36,  49,  64,  81, 100])

b = np.where(c > 10)
b
==> (array([3, 4, 5, 6, 7, 8, 9]),)

b[0]

--> array([3, 4, 5, 6, 7, 8, 9])
>>> b[0][0]
3
>>> b[0][5]
8
>>>

#=============================================================
>>> import numpy as np
>>> a = np.array([12,32,54,11,-2,-7,10,-100])
>>> a
array([  12,   32,   54,   11,   -2,   -7,   10, -100])
>>> np.nonzero(a)
(array([0, 1, 2, 3, 4, 5, 6, 7]),)
>>> np.nonzero(a-12)
(array([1, 2, 3, 4, 5, 6, 7]),)
>>> a[np.nonzero(a-12)]
array([  32,   54,   11,   -2,   -7,   10, -100])
>>> np.nonzero(a*a-12)
(array([0, 1, 2, 3, 4, 5, 6, 7]),)
>>> a*a
array([  144,  1024,  2916,   121,     4,    49,   100, 10000])
>>> np.nonzero(a*a-4)
(array([0, 1, 2, 3, 5, 6, 7]),)
>>> np.where(a*a>20)
(array([0, 1, 2, 3, 5, 6, 7]),)
>>> a[np.where(a*a>20)]
array([  12,   32,   54,   11,   -7,   10, -100])
>>> a[np.where(a*a>20)]**2
array([  144,  1024,  2916,   121,    49,   100, 10000])

