import pickle
from random import randint

from Brain import Brain
from Game import MyGame


class Population:

    def __init__(self, size, inCol, inRow, outSize, hiddenSize, cont, fast):
        self.size = size
        self.inCol = inCol
        self.inRow = inRow
        self.outSize = outSize
        self.fast = fast
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
            b.fitness = self.game.aiRunGame(b, self.inRow, self.inCol, False)
            if b.fitness >= highestF:
                biggestBrain = b
                highestF = b.fitness
        self.biggestBrain = biggestBrain
        return biggestBrain

    def getNextGeneration(self):
        brains = [self.biggestBrain.clone()]
        sum = 0
        for i in range(int((self.size-3) / 3)):
            brains.append(self.biggestBrain.cloneWithRandom())
        for b in self.brains:
            sum += max(b.fitness - 70, 1)
        for i in range(2):
            r = randint(0, int(sum))
            for b in self.brains:
                if b.fitness - 70 >= r:
                    brains.append(b.clone())
                    for t in range(int((self.size-3) / 3)):
                        brains.append(b.cloneWithRandom())
                    break
                else:
                    r -= max(b.fitness - 70, 1)
        for i in range(self.size - len(brains)):
            brains.append(self.biggestBrain.cloneWithRandom())
        self.brains = brains
        self.generation += 1
        print("Generation " + str(self.generation) + " created")

    def train(self, show):
        while self.generation < 1000:
            self.biggestBrain = self.testGeneration()
            print(self.biggestBrain.fitness)
            if show:
                self.showGame.aiRunGame(self.biggestBrain, self.inRow, self.inCol, self.fast)
            if self.generation % 3 == 0:
                fileName = "brains/BestOfGen" + str(self.generation) + ".p"
                pickle.dump(self.biggestBrain, open(fileName, 'wb'))
                print("Best of Generation " + str(self.generation) + " saved.")
            self.biggestBrain.print()
            self.getNextGeneration()

    def watchAi(self, gen):
        try:
            fileName = "brains/BestOfGen" + str(gen) + ".p"
            b = pickle.load(open(fileName, 'rb'))
            self.showGame.aiRunGame(b, self.inRow, self.inCol, self.fast)
            return True
        except FileNotFoundError:
            print("Generation " + str(gen) + " not found. Can't show brain")
            return False


if __name__ == '__main__':
    quit = -1
    while quit == -1:
        print("Welcome to the \"Mario\" game ai trainer\n")
        print("Please press 1 to play the game yourself.")
        print("Please press 2 to train a fresh ai and see the best ai of each generation.")
        print("Please press 3 to continue training an ai from a generation in the ./brains folder.")
        print("Please press 4 to see the best of every 3rd generation quickly.")
        print("Please press 5 to see the best of every 3rd generation slowly.")
        print("Please press 6 to see a specific generation.")
        pick = input("")
        if pick == "1":
            g = MyGame(False)
            g.runGame()
        if pick == "2":
            p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=-1, fast=False)
            p.train(True)
        if pick == "3":
            gen = ""
            while gen == "":
                gen = input("Please input a valid generation number of a brain in the ./brains folder.")
            ran = False
            while not ran:
                try:
                    g = int(gen)
                    ran = True
                except ValueError:
                    gen = input("Please enter a number.")
            p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=g, fast=False)
            p.train(True)
        if pick == "4":
            stop = False
            gen = 3
            p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=-1, fast=False)
            while not stop:
                stop = not p.watchAi(gen)
                gen += 3
        if pick == "5":
            stop = False
            gen = 3
            p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=-1, fast=True)
            while not stop:
                stop = not p.watchAi(gen)
                gen += 3
        if pick == "6":
            gen = ""
            while gen == "":
                gen = input("Please input a valid generation number of a brain in the ./brains folder.")
            p = Population(size=20, inCol=45, inRow=30, outSize=4, hiddenSize=15, cont=-1, fast=True)
            ran = False
            while not ran:
                try:
                    ran = p.watchAi(int(gen))
                except ValueError:
                    gen = input("Please enter a number.")