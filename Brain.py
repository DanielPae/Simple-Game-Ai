from random import randint, randrange, random, uniform
from Edge import Edge
import copy

class Brain:
    def __init__(self, inCol, inRow, outSize, hiddenSize):
        self.inSize = (inRow, inCol)
        self.outSize = outSize
        self.hiddenSize = hiddenSize
        self.conInHidden = []
        self.conHiddenOut = []
        self.hidden = [2] * hiddenSize
        self.output = [2] * outSize
        self.fitness = 0
        self.bias = 1

    def createNewEdge(self):
        w = uniform(-1, 1)
        created = False
        if -.01 < w < .01:
            w = -1
        if randint(0, 1) == 0:
            while not created:
                i = randint(0, self.inSize[1]-1)
                ir = randint(0, self.inSize[0]-1)
                h = randint(0, self.hiddenSize-1)
                ed = Edge(ir, h, w, i)
                index = -1
                try:
                    index = self.conInHidden.index(ed)
                except ValueError:
                    run = False
                if index == -1:
                    self.conInHidden.append(ed)
                    created = True
        else:
            while not created:
                h = randint(0, self.hiddenSize-1)
                o = randint(0, self.outSize-1)
                ed = Edge(h, o, w, -1)
                index = -1
                try:
                    index = self.conHiddenOut.index(ed)
                except ValueError:
                    run = False
                if index == -1:
                    self.conHiddenOut.append(ed)
                    created = True

    def deleteEdge(self):
        lih = len(self.conInHidden)
        lho = len(self.conHiddenOut)
        r = randint(0, lih + lho - 1)
        if r < lih:
            self.conInHidden.remove(self.conInHidden[r])
        else:
            r -= lih
            self.conHiddenOut.remove(self.conHiddenOut[r])

    def randomWeight(self):
        lih = len(self.conInHidden)
        lho = len(self.conHiddenOut)
        r = randint(0, lih + lho - 1)
        scratch = False
        if uniform(0, 1) < .2:
            scratch = True
        if r < lih:
            self.conInHidden[r].randomWeight(scratch)
        else:
            r -= lih
            self.conHiddenOut[r].randomWeight(scratch)

    def randomThreshold(self):
        r = randint(0, self.hiddenSize + self.outSize - 1)
        v = uniform(-1, 1) * .5
        if r < self.hiddenSize:
            self.hidden[r] += v
        else:
            r -= self.hiddenSize
            self.output[r] += v

    def runInput(self, inp):
        h = [self.bias] * self.hiddenSize
        o = [self.bias] * self.outSize
        for e in self.conInHidden:
            h[e.output] += inp[e.input][e.inpr] * e.weight
        for e in self.conHiddenOut:
            if h[e.input] >= self.hidden[e.input]:
                o[e.output] += h[e.input] * e.weight
        for i in range(self.outSize):
            if o[i] >= self.output[i]:
                o[i] = 1
            else:
                o[i] = 0
        return o

    def cloneWithRandom(self):
        b = self.clone()
        r = random()
        if len(b.conInHidden) + len(b.conHiddenOut) > 0:
            b.randomWeight()
            b.randomWeight()
            b.randomWeight()
            if r < .2:
                b.deleteEdge()
        else:
            b.createNewEdge()
        if r < .7:
            b.createNewEdge()
        b.randomThreshold()
        return b

    def clone(self):
        b = Brain(self.inSize[1], self.inSize[0], self.outSize, self.hiddenSize)
        b.conInHidden = copy.deepcopy(self.conInHidden)
        b.conHiddenOut = copy.deepcopy(self.conHiddenOut)
        b.hidden = copy.deepcopy(self.hidden)
        b.output = copy.deepcopy(self.output)
        b.bias = self.bias
        return b

    def print(self):
        print("\nBrain: ")
        ih = ""
        ho = ""
        for e in self.conInHidden:
            ih += ","+str(e)
        for e in self.conHiddenOut:
            ho += ","+str(e)
        print("Input to hidden: " + ih)
        print("Hidden to output: " + ho)
        print("Hidden threshold: " + str(self.hidden))
        print("Output threshold: " + str(self.output) + "\n")
