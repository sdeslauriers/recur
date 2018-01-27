import unittest

from random import randint

from recur.abc import MultiRecursiveIterator, Recursive, RecursiveIterator
from recur.abc import Order, postorder, preorder
from recur.abc import postorderfunction, preorderfunction
import recur.tree


class FlatTree(recur.tree.Tree):
    """Test class for decorators"""

    @preorderfunction
    def flatten(self, output):
        output.append(self.value)

    @postorderfunction
    def reverse_flatten(self, output):
        output.append(self.value)


class DirectedGraphNode(Recursive):
    """Test class for the Recursive"""

    def __init__(self):
        self.children = []

    def __recur__(self):
        return self.children

    def link(self, child):
        self.children.append(child)


class Node(Recursive):
    """Test class for pruning"""

    def __init__(self, value):
        super().__init__()
        self._children = []
        self.value = value

    def __recur__(self):
        return self._children

    def __repr__(self):
        return str(self.value)

    def add(self, node):
        self._children.append(node)


def add_leafs(node, depth, max_children):
    """Recursively add nodes up to depth levels"""

    if depth > 0:

        for i in range(1, randint(2, max_children + 1)):
            new_node = node.__class__(i + node.value)
            node.add(new_node)
            add_leafs(new_node, depth - 1, max_children)


class Decorators(unittest.TestCase):

    def test_preorder(self):
        """Test the recur.abc.preorder decorator function"""

        right_leaf = FlatTree(4)
        left_leaf = FlatTree(3)
        branch = FlatTree(2)
        root = FlatTree(1)
        branch.add(left_leaf, right_leaf)
        root.add(branch)

        flat = []
        root.flatten(flat)
        self.assertEqual(flat, [1, 2, 3, 4])

    def test_postorder(self):
        """Test the recur.abc.postorder decorator function"""

        right_leaf = FlatTree('a')
        left_leaf = FlatTree('b')
        branch = FlatTree('c')
        root = FlatTree('d')
        branch.add(left_leaf, right_leaf)
        root.add(branch)

        flat = []
        root.reverse_flatten(flat)
        self.assertEqual(flat, [l for l in 'abcd'])


class MultiRecursiveSubClass(recur.abc.MultiRecursive):
    """A mockup class to test the MultiRecursive ABC"""

    def __init__(self, value):
        super().__init__()
        self.value = value
        self.links = ([], [])  # (children, parents)

    def __multirecur__(self, index):
        return self.links[index]


class TestMultiRecursive(unittest.TestCase):

    def test_recur_simple(self):
        """Test that MultiRecursive behaves like Recursive"""

        nodes = [MultiRecursiveSubClass(i) for i in range(4)]
        for n1, n2 in zip(nodes[:-1], nodes[1:]):
            n1.links[0].append(n2)
            n2.links[1].append(n1)

        output = [n.value for n in nodes[0]]
        self.assertListEqual(output, [0, 1, 2, 3])

        output = [n.value for n in reversed(nodes[0])]
        self.assertListEqual(output, [3, 2, 1, 0])

    def test_multi_recursive_iterator_simple_list(self):
        """Test the MultiRecursiveIterator for a list

        This test verifies that the MultiRecursiveIterator can traverse
        lists in pre and post order and for ancestors and descendants.

        """

        nodes = [MultiRecursiveSubClass(i) for i in range(4)]
        for n1, n2 in zip(nodes[:-1], nodes[1:]):
            n1.links[0].append(n2)
            n2.links[1].append(n1)

        iterator = MultiRecursiveIterator(nodes[0], 0, Order.PRE)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [0, 1, 2, 3])

        iterator = MultiRecursiveIterator(nodes[0], 0, Order.POST)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [3, 2, 1, 0])

        iterator = MultiRecursiveIterator(nodes[-1], 1, Order.PRE)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [3, 2, 1, 0])

        iterator = MultiRecursiveIterator(nodes[-1], 1, Order.POST)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [0, 1, 2, 3])

        # Override order using reverse.
        iterator = MultiRecursiveIterator(nodes[-1], 1, Order.PRE)
        output = [n.value for n in reversed(iterator)]
        self.assertListEqual(output, [0, 1, 2, 3])

    def test_multi_recursive_iterator_functions(self):
        """Test the MultiRecusiveIterator with explicit order functions

        This test verifies that the order of iteration can be explicitly
        indicated using the preorder and postorder functions.

        """

        values = list(range(10))
        nodes = [MultiRecursiveSubClass(i) for i in values]
        for n1, n2 in zip(nodes[:-1], nodes[1:]):
            n1.links[0].append(n2)
            n2.links[1].append(n1)

        output = [n.value for n in preorder(nodes[0])]
        self.assertListEqual(output, values)

        output = [n.value for n in postorder(nodes[0])]
        self.assertListEqual(output, list(reversed(values)))

    def test_multi_recursive_iterator_tree(self):
        """Test the MultiRecursiveIterator for a tree

        This test verifies that the MultiRecursiveIterator can traverse
        a tree in pre/post order and for ancestors and descendants.

        """

        nodes = [MultiRecursiveSubClass(i) for i in range(5)]

        nodes[0].links[0].append(nodes[1])
        nodes[1].links[1].append(nodes[0])

        nodes[0].links[0].append(nodes[2])
        nodes[2].links[1].append(nodes[0])

        nodes[2].links[0].append(nodes[3])
        nodes[3].links[1].append(nodes[2])

        nodes[2].links[0].append(nodes[4])
        nodes[4].links[1].append(nodes[2])

        # Descendents, preorder.
        iterator = MultiRecursiveIterator(nodes[0], 0, Order.PRE)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [0, 1, 2, 3, 4])

        # Descendents, postorder.
        iterator = MultiRecursiveIterator(nodes[0], 0, Order.POST)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [4, 3, 2, 1, 0])

        # Ancestors, preorder.
        iterator = MultiRecursiveIterator(nodes[-1], 1, Order.PRE)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [4, 2, 0])

        # Ancestors, postorder.
        iterator = MultiRecursiveIterator(nodes[-1], 1, Order.POST)
        output = [n.value for n in iterator]
        self.assertListEqual(output, [0, 2, 4])


class TestMultiRecursiveIterator(unittest.TestCase):

    def test_init(self):
        """Test the __init__ method of the MultiRecursiveIterator class"""

        class ValidRecur(object):
            def __multirecur__(self):
                pass

        # Must get an object that implements __multirecur__.
        self.assertRaises(TypeError, MultiRecursiveIterator,
                          None, 0, Order.PRE)

        # Must get pre or post for the order'.
        self.assertRaises(ValueError, MultiRecursiveIterator,
                          ValidRecur(), 0, 'a')


class TestRecursiveIterator(unittest.TestCase):

    def test_cycles(self):
        """Test that we can iterate on a recursive struture with cycles"""

        # The simplest case with 2 nodes linking to each other.
        one = DirectedGraphNode()
        two = DirectedGraphNode()
        one.link(two)
        two.link(one)

        # Iterating on the nodes should yield just the two
        # nodes (no repeats).
        nodes = [node for node in one]
        self.assertListEqual(nodes, [one, two])
        nodes = [node for node in two]
        self.assertListEqual(nodes, [two, one])

        # Should also work in postorder.
        nodes = [node for node in RecursiveIterator(one, Order.POST)]
        self.assertListEqual(nodes, [two, one])
        nodes = [node for node in RecursiveIterator(two, Order.POST)]
        self.assertListEqual(nodes, [one, two])

        # More complicated example with a tree where the leaf
        # link to the root.
        root = DirectedGraphNode()
        left_leaf = DirectedGraphNode()
        right_leaf = DirectedGraphNode()
        root.link(left_leaf)
        root.link(right_leaf)
        left_leaf.link(root)
        right_leaf.link(root)

        # Iterating from any of the nodes should yield just the three
        # nodes (no repeats).
        nodes = [node for node in root]
        self.assertListEqual(nodes, [root, left_leaf, right_leaf])
        nodes = [node for node in left_leaf]
        self.assertListEqual(nodes, [left_leaf, root, right_leaf])
        nodes = [node for node in right_leaf]
        self.assertListEqual(nodes, [right_leaf, root, left_leaf])

    def test_pruning(self):
        """Test pruning with a simple tree"""

        def prune(node):
            return node.value > 4

        # Create a tree for testing.
        root = Node(0)
        add_leafs(root, depth=4, max_children=3)

        # Find all the nodes with a value above 4.
        valid_nodes = [node for node in root if node.value <= 4]

        # Pruning the nodes should give the same result.
        iterator = RecursiveIterator(root, Order.PRE, prune=prune)
        nodes = [node for node in iterator]

        self.assertListEqual(valid_nodes, nodes)
