class Edge:
    def __init__(self, inp, out, weight, inpr):
        self.input = inp
        self.output = out
        self.weight = weight
        self.inpr = -1
        if inpr != -1:
            self.inpr = inpr

