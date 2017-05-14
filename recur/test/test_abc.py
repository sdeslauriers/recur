import unittest

from recur import postorder, preorder
import recur.tree


class FlatTree(recur.tree.Tree):
    """Test class for decorators"""

    @preorder
    def flatten(self, output):
        output.append(self.value)

    @postorder
    def reverse_flatten(self, output):
        output.append(self.value)


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
