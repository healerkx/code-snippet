
class Vertex:

    def __init__(self, inner):
        self.inner = inner
        self.visit = 0
        self.adjacencies = []

    def add_adjacency(self, *adjacencies):
        for adjacency in adjacencies:
            self.adjacencies.append(adjacency)

    def can_visit_next(self):
        return self.visit + 1 <= len(self.adjacencies)

    def visit_next(self):
        if self.can_visit_next():
            cur = self.adjacencies[self.visit]
            self.visit += 1
            return cur
        else:
            return None

    def adjacency_list(self):
        return ','.join(map(lambda x: str(x.inner), self.adjacencies))

    def __str__(self):
        return "%s -> [%s]" % (str(self.inner), self.adjacency_list())


# here are the vertexes
a = Vertex('A')
b = Vertex('B')
c = Vertex('C')
d = Vertex('D')
e = Vertex('E')
f = Vertex('F')
g = Vertex('G')
h = Vertex('H')
i = Vertex('I')
j = Vertex('J')

# init the graph
a.add_adjacency(b, c)
b.add_adjacency(c, d)
c.add_adjacency(d, e)
d.add_adjacency(f)
e.add_adjacency(g, i, j)
g.add_adjacency(h)
i.add_adjacency(g)

graph = [a, b, c, d, e, f, g, h, i, j]     


def print_all(graph):
    for a in graph:
        print(a)

print_all(graph)


def can_walk(begin, end):
    """
    Depth first search
    using stack
    """
    v = begin
    stack = []
    
    while len(stack) >= 0:
        if v.can_visit_next():
            stack.append(v)
            v = v.visit_next()
            print("Move to", v)
            if v == end:
                print("Found")
                break
        elif len(stack) > 0:
            v = stack.pop()
            print("Back to", v)
        else:
            print('Not Found')
            break

    print_all(stack)
    return v

def partial_path(graph, end):
    return [each for each in graph if end in each.adjacencies]


def all_walk_partial(begin, end):
    results = []
    middles = partial_path(graph, end)
    for middle in middles:
        if begin != middle:
            paths = all_walk_partial(begin, middle)
            for path in paths:
                results.append(path + [end])
        else:
            results.append([begin, end])
    return results


def all_walk(begin, end):
    """
    Broad first search
    using ...
    """
    return all_walk_partial(begin, end)
    

if __name__ == '__main__':
    print('-' * 40)
    print('-' * 40)

    print('-' * 5, "One Way from <%s> to <%s>." % (a, j), '-' * 5)
    print(can_walk(a, j))

    print('-' * 5, "All Ways from <%s> to <%s>" % (a, g), '-' * 5)
    count = 1
    for walk in all_walk(a, g):
        print('-' * 5, "Way %d" % count, '-' * 5)
        print_all(walk)
        count += 1
    