


s = 0
for g in 1 .. 100
	a = 0
	for p in 1 .. g
		a += 1 if (g % p == 0)
		
	end
	s += a % 2
	p "#{g} #{a} #{s}"
end
