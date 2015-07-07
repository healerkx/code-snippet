
from numpy import * 
mat = [[1, 2, 3], [4, 5, 9], [4, 2, 2]]

m = len(mat)

print m
print linalg.det(mat)

s = 0
t = 0
while t < m:
	p = 1
	q = 1
	i = 0
	while i < m:
		j = (i + t) % m;
		k = (m + t - i) % m;
		p *= mat[i][j]
		q *= mat[i][k]
		i += 1
	t += 1
	s += (p - q)
print s