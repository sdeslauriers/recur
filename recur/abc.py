from abc import ABC, abstractmethod
from enum import Enum
from collections.abc import Callable, Iterator


# Possible iteration orders.
Order = Enum('Order', 'PRE POST')
Direction = Enum('Direction', 'FORWARD REVERSE')


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

    def __init__(self, recursive, order, direction=Direction.FORWARD,
                 visited=None, prune=None):
        """Iterator for Recursive instances

        The RecursiveIterator class allows iteration on any subclass of
        Recursive. It provides support for pre and postorder iteration along
        the possibility of pruning the iterated instances.

        Args:
             recursive (Recursive): The instance on which the iterator
                 operates. The iterator will iterator over this instance and
                 its sub instances returned by the __recur__ method.
            order (Order): The iteration order. If Order.PRE, the iterator
                returns the instance before its sub instances. If
                Order.POST, the iterator returns the sub instances before
                the instance.
            direction (Direction, optional): Indicates whether the subitems
                should be reversed before being traversed.
            visited (Sequence): The sequence of already visited instances.
                For internal use only.
            prune (Callable): A callable that receives an instance of
                Recursive and returns a boolean value. If the returned value is
                True for a given instance, it and all its sub instances are
                ignored by the iterator.

        """

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

        # direction must be a Direction, verified in the setter.
        self.direction = direction

        # Prune must be callable, verified in the setter.
        self.prune = prune

        self._visited = [] if visited is None else visited
        self.nextfun = (n for n in _nextfun(self))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nextfun)

    def __reversed__(self):
        self.order = Order.POST
        return self

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if not isinstance(direction, Direction):
            raise ValueError('\'direction\' must be and instance of {}, '
                             'not {}.'.format(Direction, direction.__class__))
        self._direction = direction

    @property
    def item(self):
        return self.recursive

    @property
    def prune(self):
        """Indicates if the item and the subitems should be pruned"""
        return self._prune is not None and self._prune(self.item)

    @prune.setter
    def prune(self, prune):
        if prune is not None and not isinstance(prune, Callable):
            raise ValueError('\'prune must be a Callable, not {}'
                             .format(prune))
        self._prune = prune

    @property
    def subitems(self):

        items = self.recursive.__recur__()
        if self.direction == Direction.REVERSE:
            items = reversed(items)

        items = (item for item in items if item not in self._visited)

        return items

    @property
    def subiterators(self):
        return (self.copy(i) for i in self.subitems)

    def copy(self, recursive):
        """Returns a new iterator with the same iteration properties

        Returns a new iterator with the same iteration properties as the
        one supplied, but that iterates on a different Recursive
        instance.

        """
        return RecursiveIterator(recursive, self.order,
                                 direction=self.direction,
                                 visited=self._visited,
                                 prune=self._prune)


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

    def __init__(self, multirecursive, index, order,
                 direction=Direction.FORWARD, visited=None, prune=None):

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

        # direction must be a Direction, verified in the setter.
        self.direction = direction

        # Prune must be callable, verified in the setter.
        self.prune = prune

        self._visited = [] if visited is None else visited
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
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if not isinstance(direction, Direction):
            raise ValueError('\'direction\' must be and instance of {}, '
                             'not {}.'.format(Direction, direction.__class__))
        self._direction = direction

    @property
    def item(self):
        return self.multirecursive

    @property
    def prune(self):
        """Indicates if the item and the subitems should be pruned"""
        return self._prune is not None and self._prune(self.item)

    @prune.setter
    def prune(self, prune):

        if prune is not None and not isinstance(prune, Callable):
            raise ValueError('\'prune must be a Callable, not {}'
                             .format(prune))
        self._prune = prune

    @property
    def subitems(self):

        items = self.multirecursive.__multirecur__(self.index)
        if self.direction == Direction.REVERSE:
            items = reversed(items)

        items = (item for item in items if item not in self._visited)

        return items

    @property
    def subiterators(self):
        return (self.copy(i) for i in self.subitems)

    def copy(self, multirecursive):
        """Returns a new iterator with the same iteration properties

        Returns a new iterator with the same iteration properties as the
        one supplied, but that iterates on a different MultiRecursive
        instance.

        """
        return MultiRecursiveIterator(multirecursive, self.index, self.order,
                                      direction=self.direction,
                                      visited=self._visited,
                                      prune=self._prune)


def ancestors(multirecursive):
    return MultiRecursiveIterator(multirecursive, 1, Order.PRE)


def descendants(multirecursive):
    return MultiRecursiveIterator(multirecursive, 0, Order.PRE)


def postorder(iterable, prune=None):
    """Iterates over a Recursive or MultiRecursive structure in postorder"""

    iterator = iter(iterable)
    iterator.order = Order.POST
    iterator.prune = prune
    return iterator


def preorder(iterable, prune=None):
    """Iterate in preorder

    Explicitly states that the Recursive or MultiRecursive structure should be
    iterated in preorder. This is the default, so this function mostly
    serves to make the code more explicit.

    """

    iterator = iter(iterable)
    iterator.order = Order.PRE
    iterator.prune = prune
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

    # Remember that this node was visited. We have to do it before
    # processing the node otherwise we fall in an infinite loop.
    iter._visited.append(iter.item)

    # If the item must be pruned, stop iterating right away.
    if iter.prune:
        return

    if iter.order == Order.PRE:
        yield iter.item

    for subiter in iter.subiterators:
        yield from subiter

    if iter.order == Order.POST:
        yield iter.item
