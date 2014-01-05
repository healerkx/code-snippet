

class Node

	def initialize(value)
		self.value = value
	end

	def to_s
		self.value
	end

	attr_accessor :next, :value
end

def to_list(array)
	len = array.length
	last = nil
	first = nil
	i = 0
	while (i < len)
		n = Node.new(array[i])
		if (!first)
			first = n
		end
		if (last)
			last.next = n
		end
		last = n
		i += 1
	end
	first
end


def print_list(h)
	p = h
	while (p)
		p p
		p = p.next
	end
end


def merge_list(h1, h2)
	print_list(h1)
	puts
	print_list(h2)
end


h1 = to_list([1, 3, 14, 8, 10, 9, 4])
h2 = to_list([2, 3, 11, 5, 6, 7, 0])

h = merge_list(h1, h2)
