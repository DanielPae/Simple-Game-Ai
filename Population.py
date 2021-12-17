import pickle
from random import randint

from Brain import Brain
from Game import MyGame


class Population:

    def __init__(self, size, inCol, inRow, outSize, hiddenSize, cont):
        self.size = size
        self.inCol = inCol
        self.inRow = inRow
        self.outSize = outSize
        self.hiddenSize = hiddenSize
        self.generation = 1
        b = Brain(inCol, inRow, outSize, hiddenSize)
        if cont != -1:
            try:
                fileName = "brains/BestOfGen" + str(cont) + ".p"
                b = pickle.load(open(fileName, 'rb'))
                self.generation = cont
            except FileNotFoundError:
                print("Generation " + str(cont) + " not found. Starting from scratch.")
        self.biggestBrain = b
        brains = [b]
        for i in range(size - 1):
            brains.append(b.cloneWithRandom())
        self.brains = brains
        self.game = MyGame(True)
        self.showGame = MyGame(False)

    def getBiggerBrain(self, b1, b2):
        if self.brains[b1].fitness >= self.brains[b2].fitness:
            return b1
        else:
            return b2

    def testGeneration(self):
        highestF = -400
        biggestBrain = self.biggestBrain
        for i in range(0, self.size):
            b = self.brains[i]
            b.fitness = self.game.aiRunGame(b, self.inRow, self.inCol)
            if b.fitness >= highestF:
                biggestBrain = b
                highestF = b.fitness
        self.biggestBrain = biggestBrain
        return biggestBrain

    def getNextGeneration(self):
        brains = [self.biggestBrain.clone()]
        sum = 0
        for i in range(self.size - int(2*(self.size-3) / 3)):
            brains.append(self.biggestBrain.cloneWithRandom())
        for b in self.brains:
            sum += max(b.fitness - 70, 1)
        for i in range(2):
            r = randint(0, int(sum))
            for b in self.brains:
                if b.fitness - 70 >= r:
                    brains.append(b)
                    for t in range(int((self.size-3) / 3)):
                        brains.append(b.cloneWithRandom())
                    break
                else:
                    r -= max(b.fitness - 70, 1)
        self.brains = brains
        self.generation += 1
        print("Generation " + str(self.generation) + " created")

    def train(self, show):
        while self.generation < 100:
            self.biggestBrain = self.testGeneration()
            print(self.biggestBrain.fitness)
            if show:
                self.showGame.aiRunGame(self.biggestBrain, self.inRow, self.inCol)
            else:
                self.game.aiRunGame(self.biggestBrain, self.inRow, self.inCol)
            if self.generation % 3 == 0:
                fileName = "brains/BestOfGen" + str(self.generation) + ".p"
                pickle.dump(self.biggestBrain, open(fileName, 'wb'))
                print("Best of Generation " + str(self.generation) + " saved.")
            self.biggestBrain.print()
            self.getNextGeneration()


if __name__ == '__main__':
    p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=-1)
    p.train(True)
