


# Max
def max(a, b)
	return a if a > b
	return b
end

############################################################
# Longest common subsequence.
# o(n**2), o(n*2)
def lcs(a, b)
	l = max(a.size, b.size)
	s1 = Array.new(a.size + 1, 0)
	s2 = Array.new(a.size + 1, 0)
	i = 1
	while i <= l
		j = 1
		while j <= l
			if a[i - 1] == b[j - 1]
				s2[j] = s1[j - 1] + 1
			else
				s2[j] = max(s1[j], s2[j - 1])
			end

			j += 1
		end
		p s2
		s1 = s2
		s2 = Array.new(a.size + 1, 0)
		i += 1
	end
	s1[a.size]
end

############################################################
# Test
p lcs([1,2,3,4,5,6,7,8], [2,4,5,8,7])
