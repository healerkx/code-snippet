# -*- coding: utf-8 -*-  

"""


"""
a = [2, 5, 1, 2, 3, 4, 7, 7, 6]
a = [7, 0, 11, 0, 5, 0, 11, 0, 100]

def max_pos(a):
	return max(a), a.index(max(a))

def area(a, left):
	if (len(a) == 0):
		return 0
	m, p = max_pos(a)
	if p == -1:
		return 0
	if left:
		d = map(lambda x: m - x, a[p+1:])
		#print "S:",sum(d), d
		return sum(d) + area(a[0:p], left)
	else:
		d = map(lambda x: m - x, a[:p+1])
		#print "S:",sum(d), d
		return sum(d) + area(a[p + 1:len(a)], left)

m, p = max_pos(a)
s = area(a[0: p], True) + area(a[p + 1:len(a)], False)
print(s)
