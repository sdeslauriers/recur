from abc import ABC, abstractmethod


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
