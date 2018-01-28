from recur import Recursive


class Tree(Recursive):

    def __init__(self):
        """A tree data structure

        The Tree class implements a simple tree data structure where each
        node of the tree can iterate over its descendants.

        """

        super().__init__()

        self._children = []

        # Remember whether the tree is a root or not. Only roots can be added
        # as children to other trees.
        self._is_root = True

    def __recur__(self):
        return self._children

    @property
    def is_leaf(self):
        """Indicates if the tree is a leaf (has no children)"""
        return len(self._children) == 0

    @property
    def is_root(self):
        """Indicates if the tree is a root (is not a child)"""
        return self._is_root

    def add(self, tree):
        """Adds a child to the tree

        Adds a child to the tree by listing the supplied tree as a child.
        The supplied tree must be a root.

        Args:
            tree (Tree): The tree to add as a child. Must be a root.

        Raises:
            ValueError if the supplied tree is not a root.

        """

        if not tree.is_root:
            raise ValueError('\'tree\' already belongs to another tree.')

        # Once a tree is added as a child, it is not longer a root. Unless
        # it is tampered with, this will prevent cycles in the tree.
        tree._is_root = False
        self._children.append(tree)


def leaves(tree):
    """Iterator for the leaves of a tree

    Returns a generator that iterates over the leaves of a tree, i.e. the
    nodes of the tree with no children.

    Args:
        tree (Tree): The tree for which we want the leaves. It does not need
            to be the root of a tree.

    """

    return (t for t in tree if t.is_leaf)
