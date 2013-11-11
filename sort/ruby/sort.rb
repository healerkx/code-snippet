

############################################################
# Selection sort
# http://en.wikipedia.org/wiki/Selection_sort
# 
def select_sort array
	a = array.clone
	len = a.length
	i = 0

	while i < len - 1
		min = i
		j = i + 1
		while j < len
			if a[j] < a[min]
				min = j
			end
			j += 1
		end

		if i != min
			a[i], a[min] = a[min], a[i]
		end

		i += 1
	end
	return a
end


############################################################
# Bubble sort
# http://en.wikipedia.org/wiki/Bubble_sort
# 
def bubble_sort array
	a = array.clone
	len = a.length
	b = len - 1
	
	while b > 0
		j, k = 0, 0
		while j < b
			if a[j] > a[j + 1]
				a[j], a[j + 1] = a[j + 1], a[j]
				k = j
			end
			j += 1
		end
		b = k
	end
	return a
end

############################################################
# Insertion sort
# http://en.wikipedia.org/wiki/Insertion_sort
#
def insert_sort array
	a = array.clone
	len = a.length
	i = 1
	while i < len
		j = i - 1
		v = a[i]
		while j >= 0
			if v <= a[j]
				a[j + 1] = a[j]
			else
				break
			end
			j -= 1

		end

		a[j + 1] = v
		i += 1
	end
	return a
end


############################################################
#
def quick_sort_internal(a, from, to)
	return if from >= to
	m = a[to]
	i1, i2 = from, to
	while true
		while m > a[i1]
			i1 += 1
		end

		i2 -= 1
		while m < a[i2]
			i2 -= 1
			break if (i2 == from)
		end

		break if i1 >= i2

		a[i1], a[i2] = a[i2], a[i1] 

	end
	a[i1], a[to] = a[to], a[i1] 
	quick_sort_internal(a, from, i1 - 1)
	quick_sort_internal(a, i1 + 1, to)
end

def quick_sort(array)
	a = array.clone
	quick_sort_internal(a, 0, a.size - 1)
	return a
end

############################################################
#
def heap_sort_create_heap a
end

def heap_sort array
	a = array.clone
	heap_sort_create_heap(a)
end

############################################################
#
def array_in_order(array)
	len = array.length
	i = 0
	flag = array[0] < array.last
	while i < len - 1
		if array[i] != array[i + 1] 
			if (array[i] < array[i + 1]) != flag
				return false
			end
		end
		i += 1
	end		
	return true
end

a = [5, 1, 3, 3, 2, 0, 4, 6, 4, 7, 2, 9]

p select_sort(a) 
p bubble_sort(a)
p quick_sort(a)
p insert_sort(a)

p array_in_order([1,1,1,1,1])
p array_in_order([1,2,1,1,1])
p array_in_order([1,1,2,1,1])
p array_in_order([1,1,1,2,1])
p array_in_order([1,1,1,1,2])
p array_in_order([2,1,1,1,1])
p array_in_order([1,1,3,4,6])
p array_in_order([7,4,3,3,2])
