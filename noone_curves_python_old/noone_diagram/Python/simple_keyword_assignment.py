####
# CCD Just testing use of keyword arguments ....

>>> HDO = True         # Initialize HDO and use it in function
>>> definition def tst(x,hdo=HDO):
>>> This has the advantage that the value of HDO is seen right up front
>>> in some global assignment.
...   print x
...   if hdo: print "hdo is true"
...   else: print "hdo is false"
...
>>> tst(3)
3
hdo is true
>>> tst(3,hdo=False)
3
hdo is false

# Now initialize hdo to True in the funtion def itself:
>>> def tst(x,hdo=True):
...   if hdo: print "hdo is true"
...   else: print "hdo is false"
...
>>>
>>> tst(4)
hdo is true
>>> tst(4,hdo=False)
hdo is false
>>> tst(4,hdo=133)
hdo is true

