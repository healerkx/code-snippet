


def print_array(r):
	for line in r:
		print line

w = [1, 2, 6, 2, 4]
v = [6, 3, 5, 4, 1]
s = len(w)
m = 10

r = []
for i in range(0, s + 1):
	r.append([0] * (m + 1))

print_array(r)

for i in range(1, s + 1):
	for j in range(1, m + 1):
		a, b = r[i-1][j], 0
		if j >= w[i-1]:
			b = r[i-1][j - w[i - 1]] + v[i - 1]
		r[i][j] = max(a, b)

print
print_array(r)


