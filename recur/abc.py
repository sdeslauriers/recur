from abc import ABC, abstractmethod
from enum import Enum
from collections.abc import Iterator


# Possible iteration order.
Order = Enum('Order', 'PRE POST')


class Recursive(ABC):
    """Abstract base class for classes that provide the __recur__() method"""

    @abstractmethod
    def __recur__(self):
        """Returns an iterable of instances of the same class as the caller"""
        pass

    def __iter__(self):
        """Iterate recursively over the structure in pre-order"""
        return RecursiveIterator(self, Order.PRE)

    def __reversed__(self):
        """Iterate recursively over the structure in post-order"""
        return RecursiveIterator(self, Order.POST)

    @classmethod
    def __subclasshook__(cls, subclass):

        # The instance must provide __recur__.
        if not any('__recur__' in s.__dict__ for s in subclass.__mro__):
            return False

        return True


class RecursiveIterator(Iterator):
    """Iterator for Recursive instances"""

    def __init__(self, recursive, order):

        super().__init__()

        if not isinstance(recursive, Recursive):
            raise TypeError(
                '\'recursive\' must be an instance of {} or implement '
                'the __recur__ method'.format(Recursive))
        self.recursive = recursive

        if order != Order.PRE and order != Order.POST:
            raise ValueError('\'order\' must be {} or {}, not {}'
                             .format(Order.PRE, Order.POST, order))
        self.order = order

        self.nextfun = (n for n in _nextfun(self))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nextfun)

    def __reversed__(self):
        self.order = Order.POST
        return self

    @property
    def item(self):
        return self.recursive

    @property
    def subitems(self):
        if self.order == Order.PRE:
            return self.recursive.__recur__()
        else:
            return reversed(self.recursive.__recur__())

    @property
    def subiterators(self):
        return (RecursiveIterator(i, self.order) for i in self.subitems)


class MultiRecursive(ABC):
    """Abstract base class for classes that provide __multirecur__ method

    This abstract base class can be used to generate data structures where
    and instance can provide several lists of instances of the same class.
    A simple example is a graph which can provide an list of children and
    a list of parents.

    """

    def __iter__(self):
        return MultiRecursiveIterator(self, 0, Order.PRE)

    @abstractmethod
    def __multirecur__(self, index):
        """Returns the ith iterable of instances of MultiRecursive"""
        pass

    def __reversed__(self):
        return MultiRecursiveIterator(self, 0, Order.POST)

    @classmethod
    def __subclasshook__(cls, subclass):

        # and have __multirecur__.
        if not any('__multirecur__' in s.__dict__ for s in subclass.__mro__):
            return False

        return True


class MultiRecursiveIterator(Iterator):
    """Iterator for MultiRecursive instances"""

    def __init__(self, multirecursive, index, order):

        super().__init__()

        if not isinstance(multirecursive, MultiRecursive):
            raise TypeError(
                '\'multirecursive\' must be an instance of {} or implement '
                'the __multirecur__ method'.format(MultiRecursive))
        self.multirecursive = multirecursive

        if order != Order.PRE and order != Order.POST:
            raise ValueError('\'order\' must be {} or {}, not {}'
                             .format(Order.PRE, Order.POST, order))
        self.order = order

        self.index = index
        self.nextfun = (n for n in _nextfun(self))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nextfun)

    def __reversed__(self):
        self.order = Order.POST
        return self

    @property
    def item(self):
        return self.multirecursive

    @property
    def subitems(self):
        if self.order == Order.PRE:
            return self.multirecursive.__multirecur__(self.index)
        else:
            return reversed(self.multirecursive.__multirecur__(self.index))

    @property
    def subiterators(self):
        def new(i):
            return MultiRecursiveIterator(i, self.index, self.order)
        return (new(i) for i in self.subitems)


def postorder(iterable):
    """Iterates over a Recursive or MultiRecursive structure in postorder"""

    iterator = iter(iterable)
    iterator.order = Order.POST
    return iterator


def preorder(iterable):
    """Iterate in preorder

    Explicitly states that the Recursive or MultiRecursive structure should be
    interated in preorder. This is the default, so this function mostly
    serves to make the code more explicit.

    """

    iterator = iter(iterable)
    iterator.order = Order.PRE
    return iterator


def postorderfunction(func):
    """Decorator for functions that iterate in postorder"""
    def nested(obj, *args):
        for subobj in reversed(obj):
            func(subobj, *args)
    return nested


def preorderfunction(func):
    """Decorator for functions that iterate in preorder"""
    def nested(obj, *args):
        for subobj in obj:
            func(subobj, *args)
    return nested


def _nextfun(iter):

    if iter.order == Order.PRE:
        yield iter.item

    for subiter in iter.subiterators:
        yield from subiter

    if iter.order == Order.POST:
        yield iter.item
