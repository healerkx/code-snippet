
class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

	def __str__(self):
		if self.next:
			return "[ <%d>-><%d> ]" % (self.data, self.next.data)
		else:
			return "[ <%d>->End ]" % (self.data)

	def show(self, header = None):
		if not header:
			header = '-' * 30
		print(header)
		p = self
		while p != None:
			print("%d " % p.data, end = '')
			p = p.next
		print()


def insertsort(l):
	if l == None or l.next == None:
		return l
	o = None
	p = l
	q = p.next
	
	while q != None:
		o = None
		t = l
		s = o
		while q.data > t.data:
			o = t
			t = t.next
		else:
			if q == t:
				o = p
				p = q
				q = q.next
				print("q == t ", end='')
				l.show()
				continue

			print('change two nodes', q, t)
			r = q.next
			p.next = q.next
			
			if o:
				o.next = q
				q.next = t
			else:
				q.next = t
				l = q
			l.show()

			q = r
		
		l.show("------------ End of while -----------")

	return l


n0 = Node(8)
n1 = Node(2)
n2 = Node(1)
n3 = Node(4)
n4 = Node(3)
n5 = Node(7)
n6 = Node(5)
n7 = Node(0)
n8 = Node(9)
n9 = Node(6)

n0.next = n1
n1.next = n2
n2.next = n3
n3.next = n4
n4.next = n5
n5.next = n6
n6.next = n7
n7.next = n8
n8.next = n9

n0.show()
n = insertsort(n0)
n.show()


