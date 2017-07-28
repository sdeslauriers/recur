import unittest

from recur.graphs import Undirected as Node


class TestUndirected(unittest.TestCase):
    """Test the recur.graphs.Undirected class"""

    def triangle_graph(self):
        """Returns a triangle graph

        A--B
        | /
        |/
        C

        """

        # Create a triangle of nodes.
        node_a = Node()
        node_b = Node()
        node_c = Node()
        node_a.add(node_b)
        node_b.add(node_c)
        node_c.add(node_a)

        return node_a

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

        graph = self.triangle_graph()
        nodes = [graph] + list(graph.neighbors)

        # This should not loop forever.
        iterated_nodes = []
        for node in graph:
            iterated_nodes.append(node)

        # The order for the second node is undetermined. What matters is
        # that they both be there.
        self.assertEqual(nodes[0], iterated_nodes[0])
        self.assertSetEqual(set(nodes[1:]), set(iterated_nodes[1:]))

        # This should not loop forever.
        iterated_nodes = []
        for node in reversed(graph):
            iterated_nodes.append(node)

        # The order for the second node is undetermined. What matters is
        # that they both be there.
        self.assertEqual(nodes[0], iterated_nodes[-1])
        self.assertSetEqual(set(nodes[1:]), set(iterated_nodes[:-1]))

    def test_family(self):
        """Test the family property"""

        # The family of an isolated node is just itself.
        graph = Node()
        self.assertSetEqual(graph.family, set(graph))

        # The family of a node is itself and its neighbors.
        graph = self.triangle_graph()
        nodes = [graph] + list(graph.neighbors)
        self.assertSetEqual(graph.family, set(nodes))

    def test_is_isolated(self):
        """Test the is_isolated property"""

        # A node is isolated if it has no links.
        graph = Node()
        self.assertTrue(graph.is_isolated)

        graph.add(Node())
        self.assertFalse(graph.is_isolated)

    def test_is_simplicial(self):
        """Test the is_simplicial property"""

        node_a = Node()
        self.assertTrue(node_a.is_simplicial)

        node_b = Node()
        node_b.add(node_a)
        self.assertTrue(node_a.is_simplicial)
        self.assertTrue(node_b.is_simplicial)

        node_c = Node()
        node_c.add(node_a)
        self.assertFalse(node_a.is_simplicial)
        self.assertTrue(node_b.is_simplicial)
        self.assertTrue(node_c.is_simplicial)

        node_c.add(node_b)
        self.assertTrue(node_a.is_simplicial)
        self.assertTrue(node_b.is_simplicial)
        self.assertTrue(node_c.is_simplicial)

    def test_nb_missing_links(self):
        """Test the nb_missing_links property"""

        node_a = Node()
        self.assertEqual(node_a.nb_missing_links, 0)

        node_b = Node()
        node_b.add(node_a)
        self.assertEqual(node_a.nb_missing_links, 0)
        self.assertEqual(node_b.nb_missing_links, 0)

        node_c = Node()
        node_c.add(node_a)
        self.assertEqual(node_a.nb_missing_links, 1)
        self.assertEqual(node_b.nb_missing_links, 0)
        self.assertEqual(node_c.nb_missing_links, 0)

        node_c.add(node_b)
        self.assertEqual(node_a.nb_missing_links, 0)
        self.assertEqual(node_b.nb_missing_links, 0)
        self.assertEqual(node_c.nb_missing_links, 0)
