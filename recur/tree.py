from recur import Recursive


class Tree(Recursive):
    def __init__(self, value):
        self.value = value
        self.forest = []

    def __recur__(self):
        return self.forest

    def add(self, *forest):
        """Adds one or many children to the current node"""
        [self.forest.append(tree) for tree in forest]
