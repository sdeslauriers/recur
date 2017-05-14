import unittest

import recur.tree


class Tree(unittest.TestCase):

    def test_iter_reversed(self):
        """Test that the tree class iterates correctly"""

        left_leaf = recur.tree.Tree("left leaf")
        right_leaf = recur.tree.Tree("right leaf")
        branch = recur.tree.Tree("branch")
        root = recur.tree.Tree("root")
        branch.add(left_leaf, right_leaf)
        root.add(branch)

        expected = [root, branch, left_leaf, right_leaf]
        self.assertEqual([n for n in root], expected)
        expected = list(reversed(expected))
        self.assertEqual([n for n in reversed(root)], expected)
