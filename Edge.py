from random import randrange, uniform


class Edge:
    def __init__(self, inp, out, weight, inpr):
        self.input = inp
        self.output = out
        self.weight = weight
        self.inpr = -1
        if not inpr == -1:
            self.inpr = inpr

    def __eq__(self, other):
        if self.input == other.input and self.output == other.output and self.inpr == other.inpr:
            return True
        return False

    def __str__(self):
        return "(" + str(self.inpr) + "," + str(self.input) + "," + str(self.output) + "," + str(self.weight) + ")"

    def __copy__(self):
        return Edge(self.input, self.output, self.weight, self.inpr)

    def randomWeight(self, scratch):
        if scratch:
            self.weight = uniform(-1.5, 1.5)
        else:
            self.weight += uniform(-1.5, 1.5) * .3
