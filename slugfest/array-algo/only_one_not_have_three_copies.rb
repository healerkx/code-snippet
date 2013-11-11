
# 9 is the result
a = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 100]
max = a.max

v = 0
max.to_s(2).length.times{ |t|
	s = 0
	a.each{|i| s += i & 1 << t }
	v |= ((s % 3 + 1) / 2) << t
}

p v