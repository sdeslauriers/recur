import unittest

from recur.graphs import Undirected as Node


class TestUndirected(unittest.TestCase):
    """Test the recur.graphs.Undirected class"""

    def test_simple_loop(self):
        """Test that we can traverse a simple graph"""

        # Create a chain A-B-C-D-E
        nodes = [Node()]
        for _ in range(5):
            nodes.append(Node())
            nodes[-2].add(nodes[-1])

        # The nodes should be traversed from A to E.
        iterated_nodes = []
        for node in nodes[0]:
            iterated_nodes.append(node)

        self.assertEqual(nodes, iterated_nodes)

        # The nodes should be traversed E to A.
        iterated_nodes = []
        for node in reversed(nodes[0]):
            iterated_nodes.append(node)

        self.assertEqual(nodes[::-1], iterated_nodes)

    def test_cylic_loop(self):
        """Test that we can loop even if there is a cycle"""

        # Create a triangle of nodes.
        node_a = Node()
        node_b = Node()
        node_c = Node()
        node_a.add(node_b)
        node_b.add(node_c)
        node_c.add(node_a)

        nodes = [node_a, node_b, node_c]

        # This should not loop forever.
        iterated_nodes = []
        for node in node_a:
            iterated_nodes.append(node)

        # The order for the second node is undetermined. What matters is
        # that they both be there.
        self.assertEqual(nodes[0], iterated_nodes[0])
        self.assertSetEqual(set(nodes[1:]), set(iterated_nodes[1:]))

        # This should not loop forever.
        iterated_nodes = []
        for node in reversed(node_a):
            iterated_nodes.append(node)

        # The order for the second node is undetermined. What matters is
        # that they both be there.
        self.assertEqual(nodes[0], iterated_nodes[-1])
        self.assertSetEqual(set(nodes[1:]), set(iterated_nodes[:-1]))
