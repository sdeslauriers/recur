from abc import ABC, abstractmethod


class Recursive(ABC):
    """Abstract base class for classes that provide the __recur__() method"""

    @abstractmethod
    def __recur__(self, visited=None):
        """Returns an iterable of instances of the same class as the caller

        The visited parameter is and iterable of instances that have already
        been visited. This allows recur to terminate even in the case of
        cyclic structures.

        """
        pass

    def __iter__(self, visited=None):
        """Iterate recursively over the structure in pre-order"""

        if visited is None:
            visited = set()
        visited.add(self)

        items = self.__recur__(visited)
        for item in items:
            visited.add(item)

        yield self
        for item in items:
            yield from item.__iter__(visited)

    def __reversed__(self, visited=None):
        """Iterate recursively over the structure in post-order"""

        if visited is None:
            visited = set()
        visited.add(self)

        items = self.__recur__(visited)
        for item in items:
            visited.add(item)

        for item in reversed(self.__recur__()):
            yield from item.__reversed__()
        yield self


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
