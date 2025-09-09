
# Here we initialize eff to False
>>> def tst(x,y,eff=False):
...   print "X,Y =",x,y
...   if eff:
...     print "eff must be non-false"
...     print "eff =",eff
...
>>> tst(1,2)
X,Y = 1 2
>>> tst(1,2,eff=True)
X,Y = 1 2
eff must be non-false
eff = True
>>> tst(1,2,eff=133)
X,Y = 1 2
eff must be non-false
eff = 133
>>>
# Here we initialize cc to True
>>> cc=True
>>> def tst(x,y,cc=cc):
...   print "X,Y =",x,y
...   if cc: print "cc true -->",x**2
...   else: print "cc false -->",-x**2
...
>>> tst(1,2)
X,Y = 1 2
cc true --> 1
>>> cc=False
>>> tst(1,2)
X,Y = 1 2
cc true --> 1
>>> tst(1,2,cc=False)
X,Y = 1 2
cc false --> -1
>>>

