from .abc import Recursive


class Undirected(Recursive):
    def __init__(self):
        """Node in an undirected graph

        Because the graph is implemented as a recursive structure, there is no
        distinction between the graph and its nodes. Every node is a graph.
        This also implies that this class can only represent connected graphs,
        since there is no way to add a node without linking it.

        The implementation handles cycles and will loop over all nodes once.

        """

        self._links = set()

    def __recur__(self, visited=None):

        if visited is not None:
            links = self._links - visited
        else:
            links = self._links

        return tuple(links)

    def add(self, node):
        """Adds a node to the graph by linking it with the current node

        Because the graph is undirected, this adds a link between the current
        node and the new node and between the new node and the current node.

        """

        self._links.add(node)
        node._links.add(self)

        return self
