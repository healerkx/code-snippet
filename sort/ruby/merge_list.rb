

class Node
	def initialize(value)
		self.value = value
	end

	def to_s
		"#{self.value}"
	end

	attr_accessor :next, :value
end

def to_list(array)
	len = array.length
	first = last = Node.new(array[0])
	i = 1
	while (i < len)
		n = Node.new(array[i])
		last.next = n
		last = n
		i += 1
	end
	first
end


def print_list(h)
	p = h
	while (p)
		print(p, " ")
		p = p.next
	end
end


def merge_list(h1, h2)
	if h1.value < h2.value
		h = h1
		h1 = h1.next
	else
		h = h2
		h2 = h2.next
	end

	p = h
	while h1 && h2
		if h1.value < h2.value
			p.next = h1
			p = h1
			h1 = h1.next
		else
			p.next = h2
			p = h2
			h2 = h2.next
		end
	end

	if h1
		p.next = h1
	elsif h2
		p.next = h2
	end
		
	return h
end


h1 = to_list([1, 3, 8, 10, 19, 24, 25])
h2 = to_list([2, 4, 11, 15, 16, 17, 20, 33, 35])

h = merge_list(h1, h2)
#puts
print_list(h)