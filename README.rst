recur
=====
A Python package to simplify the creation and manipulation of recursive data
structures.

Quickstart
----------
Install the package by running: ::

    pip install recursive-abc

Verify the installation by importing the package in ipython: ::

    import recur

If this succeeds, you have successfully installed the ``recur`` package. You
can now use it to define you own recursive data structures. Here is an
example that defines a new class named ``MyRecursiveClass`` which
illustrates the basic features of the package. ::

    from recur.abc import Recursive

    class MyRecursiveClass(Recursive):

        def __init__(self, name):
            super().__init__()
            self.name = name
            self._children = []

        def __recur__(self):
            return self._children

        def __repr__(self):
            return self.name

        def add_child(self, child):
            self._children.append(child)

The ``__recur__`` method is the centerpiece of this example. It is a method
which must be implemented by concrete subclasses of ``Recursive``. It must
return an iterable of objects of the same class as the one implementing
it. We can now create instances of ``MyRecursiveClass`` and link them
together. ::

    root = MyRecursiveClass('root')
    left = MyRecursiveClass('left')
    center = MyRecursiveClass('center')
    right = MyRecursiveClass('right')

    root.add_child(left)
    root.add_child(center)
    root.add_child(right)
    center.add_child(root)  # Cycles are fine.

The key feature of ``recur`` is how it facilitates iteration over recursive
structures. To iterate over the structure defined above, we can simply
write: ::

    for node in root:
        print(node.name)

Note that we iterated in preorder. To iterate in postorder, we can simply
use ``reversed``. ::

    for node in reversed(root):
        print(node.name)

