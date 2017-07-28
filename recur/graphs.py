from itertools import combinations

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

        # Even if the links are unordered, we want to be able to iterate over
        # them with reverse (for compatibility), so we return a tuple.
        return tuple(links)

    @property
    def family(self):
        """Get the family of a node"""

        return set(self._links) | set(self)

    @property
    def is_isolated(self):
        """Indicates if a node is isolated (has no links)"""

        return len(self._links) == 0

    @property
    def is_simplicial(self):
        """Indicates if a node is simplicial

        A node is simplicial if all the nodes it is linked to are pairwise
        link. In other words, the family of the node form a clique.

        """

        for node, other_node in combinations(self.neighbors, 2):
            if node not in other_node.neighbors:
                return False

        return True

    @property
    def nb_missing_links(self):
        """Counts the number of missing links to make the node simplicial"""

        missing = 0
        for node, other_node in combinations(self.neighbors, 2):
            if node not in other_node.neighbors:
                missing += 1

        return missing

    @property
    def neighbors(self):
        """Get the neighbors of a node"""

        return set(self._links)

    def add(self, node):
        """Adds a node to the graph by linking it with the current node

        Because the graph is undirected, this adds a link between the current
        node and the new node and between the new node and the current node.

        """

        self._links.add(node)
        node._links.add(self)

        return self
