# -*- coding: utf-8 -*-  

"""


"""
a = [2, 5, 1, 2, 3, 4, 7, 7, 6]
a = [11, 0, 7, 0, 5, 0, 3, 0, 1]

def max_pos(a):
	m = 0
	p = -1
	for i in range(0, len(a)):
		if a[i] > m:
			m = a[i]
			p = i
	return m, p


def area(a, m, left):
	if len(a) == 0:
		return 0

	m2, p = max_pos(a)
	print '=>', m2 , p, left 
	if p != -1:
		if left:
			d = map(lambda x: m2 - x, a[p+1:])
			print "S:",sum(d), d
			return sum(d) + area(a[0:p], m2, left)
		else:
			d = map(lambda x: m2 - x, a[:p+1])
			print "S:",sum(d), d
			return sum(d) + area(a[p + 1:len(a)], m2, left)
	return 0

m, p = max_pos(a)
print m, p
print area(a[0: p], m, True) + area(a[p + 1:len(a)], m, False)
