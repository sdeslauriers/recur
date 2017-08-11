from abc import ABC, abstractmethod
from collections.abc import Iterator


class Recursive(ABC):
    """Abstract base class for classes that provide the __recur__() method"""

    @abstractmethod
    def __recur__(self):
        """Returns an iterable of instances of the same class as the caller"""
        pass

    def __iter__(self):
        """Iterate recursively over the structure in pre-order"""
        yield self
        for item in self.__recur__():
            yield from item.__iter__()

    def __reversed__(self):
        """Iterate recursively over the structure in post-order"""
        for item in reversed(self.__recur__()):
            yield from item.__reversed__()
        yield self


class MultiRecursive(Recursive):
    """Abstract base class for classes that provide __multirecur__ method

    This abstract base class can be used to generate data structures where
    and instance can provide several lists of instances of the same class.
    A simple example is a graph which can provide an list of children and
    a list of parents.

    """

    @abstractmethod
    def __multirecur__(self, index):
        """Returns the ith iterable of instances of MultiRecursive"""
        pass

    def __recur__(self):
        return self.__multirecur__(0)

    @classmethod
    def __subclasshook__(cls, subclass):

        # Must meet the requirements of Recursive.
        if not super().__subclasshook__(subclass):
            return False

        # and have __multirecur__.
        if not any('__multirecur__' in s.__dict__ for s in subclass.__mro__):
            return False

        return True


class MultiRecursiveIterator(Iterator):
    """Iterator for MultiRecursive instances"""

    PREORDER = 'pre'
    POSTORDER = 'post'

    def __init__(self, multirecursive, index, order):
        super().__init__()

        if not isinstance(multirecursive, MultiRecursive):
            raise TypeError(
                '\'multirecursive\' must be an instance of {} or implement '
                'the __recur__ and __multirecur__ methods')
        self.multirecursive = multirecursive

        if order != self.PREORDER and order != self.POSTORDER:
            raise ValueError('\'order\' must be {} or {}, not {}'
                             .format(self.PREORDER, self.POSTORDER, order))
        self.order = order

        self.index = index
        self.nextfun = (n for n in _nextfun(self))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nextfun)


def postorder(func):
    """Decorator function for methods that iterate in postorder"""
    def nested(obj, *args):
        for subobj in reversed(obj):
            func(subobj, *args)
    return nested


def preorder(func):
    """Decorator function for methods that iterate in preorder"""
    def nested(obj, *args):
        for subobj in obj:
            func(subobj, *args)
    return nested


def _nextfun(iter):

    if iter.order == 'pre':
        yield iter.multirecursive

    items = iter.multirecursive.__multirecur__(iter.index)
    for item in items:
        yield from MultiRecursiveIterator(item, iter.index, iter.order)

    if iter.order == 'post':
        yield iter.multirecursive
