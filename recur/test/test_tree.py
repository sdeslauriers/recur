import unittest

from recur.abc import postorder
from recur.trees import Tree


class TestTree(unittest.TestCase):

    def test_iter_reversed(self):
        """Test that the tree class iterates correctly"""

        left_leaf = Tree()
        right_leaf = Tree()
        branch = Tree()
        root = Tree()
        branch.add(left_leaf)
        branch.add(right_leaf)
        root.add(branch)

        expected = [root, branch, left_leaf, right_leaf]
        self.assertEqual([n for n in root], expected)
        expected = [left_leaf, right_leaf, branch, root]
        self.assertEqual([n for n in postorder(root)], expected)
