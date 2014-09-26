

class tree:

	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
	def __str__(self):
		return "%s" % self.value

prev = None

def btree2dlist(treenode):
	global prev
	if not treenode:
		return
	btree2dlist(treenode.left)
	treenode.left = prev

	if prev:
		prev.right = treenode
	prev = treenode
	btree2dlist(treenode.right)

root = tree(4)
lefttree = tree(2)
lefttree.left = tree(1)
lefttree.right = tree(3)

root.left = lefttree
root.right = tree(5)
btree2dlist(root)


n = prev
while n:
	print n, n.right
	n = n.left

