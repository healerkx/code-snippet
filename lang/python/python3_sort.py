
import functools

def c(x, y):
	if x % 2 == y % 2:
		if x < y:
			return -1
		return 0
	elif x % 2 == 1:
		return -1
	return 0

def sort(a):
	l = len(a)
	i = 0

	while i < l:
		j = i + 1
		while j < l:
			if c(a[i], a[j]) >= 0:
				a[i], a[j] = a[j], a[i]
			j += 1
		i += 1


a = [1, 2, 10, 5, 4, 3, 6, 8, 7, 9, 11, 0]
#sort(a)
a.sort(key=functools.cmp_to_key(c))
print(a)
