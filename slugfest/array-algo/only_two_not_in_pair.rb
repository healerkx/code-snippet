

# 
a = [1, 1, 2, 2, 3, 3, 4, 9]

x = a.inject{|s, i| s ^ i}
f = 2 ** (x.to_s(2).size - 1)

p a.collect{|j| j if j & f == 0}.compact.inject{|s, i| s ^ i}
p a.collect{|j| j if j & f != 0}.compact.inject{|s, i| s ^ i}