from random import randint
from Edge import Edge


class Brain:
    def __init__(self, inCol, inRow, outSize, hiddenSize):
        self.inSize = (inCol, inRow)
        self.outSize = outSize
        self.hiddenSize = hiddenSize
        self.hidden = [0] * hiddenSize
        self.output = [0] * hiddenSize
        self.conInHidden = []
        self.conHiddenOut = []
        self.fitness = 0

    def createNewEdge(self):
        w = randint(0, 1)
        if w == 0:
            w = -1
        if randint(0, 1) == 0:
            self.conInHidden.append(Edge(randint(0, self.inSize[0]), randint(0, self.hiddenSize), w, randint(0, self.inSize[1])))
        else:
            self.conHiddenOut.append(Edge(randint(0, self.hiddenSize), randint(0, self.outSize), w, -1))

    def runInput(self, inp):
        for e in self.conInHidden:
            self.hidden[e.output] += inp[e.input][e.inpr] * e.weight
        for e in self.conHiddenOut:
            self.output[e.output] += inp[e.input] * e.weight
        return self.output