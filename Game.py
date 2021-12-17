import sys

import pygame
from Platform import Platform
from Enemy import Enemy
import pickle


class MyGame:
    state = 0
    x = 0
    y = 0
    vx = 0
    vy = 0
    pw = 25
    ph = 31
    placeChoice = 0
    p = False
    RUN_ACCEL = .01
    WALK_ACCEL = .055
    MAX_RUN = 8
    JUMP_START_BOOST = -5.5
    JUMP_HOLD_GRAV = 0
    JUMP_APEX = 90
    GRAV = .35
    PLAYER_COLOR = pygame.Color(180, 176, 255)
    GROUND_COLOR = pygame.Color(7, 99, 81)
    PLAT_COLOR = pygame.Color(255, 226, 176)
    ENEMY_COLOR = pygame.Color(255, 179, 218)
    DEFEATED_COLOR = pygame.Color(250, 103, 97)
    jump_start = -1
    printTimer = 0
    FRIC = .075
    killTimer = -1
    farthestRight = 425
    ground_limit = MAX_RUN
    air_limit = MAX_RUN
    left = False
    right = False
    jump = False
    run = False
    grounded = False
    platforms = []
    enemies = []

    sx = 0
    sy = 0

    def __init__(self, forAi):
        pygame.init()
        self.d = pygame.draw
        self.width = 0
        self.forAi = forAi
        self.height = 0
        self.screen = pygame.display.set_mode((self.width, self.height)).convert()
        self.frameCount = 0
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def setup(self):
        self.state = 0
        self.width = 900
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.score = 0
        self.frameCount = 0
        self.killTimer = -1
        self.x = 75
        self.y = self.height - 350
        self.vx = 0
        self.vy = 0

        self.platforms = [Platform([0, self.height - 100, 2000, 100], 0, self.GROUND_COLOR),
                          Platform([400, self.height - 200, 100, 20], 1, self.PLAT_COLOR),
                          Platform([750, self.height - 250, 50, 50], 1, self.PLAT_COLOR)]

        self.enemies = [Enemy([900, self.height - 200, 40, 40], 1, self.ENEMY_COLOR),
                        Enemy([1100, self.height - 200, 40, 40], 1, self.ENEMY_COLOR)]

        try:
            self.platforms = pickle.load(open("Level1Platforms.p", "rb"))
            for plat in self.platforms:
                if plat.ty == 1:
                    plat.c = self.PLAT_COLOR
                else:
                    plat.c = self.GROUND_COLOR
            self.enemies = pickle.load(open("Level1Enemies.p", "rb"))
            for en in self.enemies:
                en.c = self.ENEMY_COLOR
        except FileNotFoundError:
            print("Level 1 files not found")

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.state == 0:
            self.handlePlayer()
            self.handlePlatforms()
            self.handleEnemies()

            pressed = pygame.mouse.get_pressed(3)

            if pressed[0] and self.sx == 0:
                loc = pygame.mouse.get_pos()
                self.sx = loc[0] + self.x - self.farthestRight
                self.sy = loc[1]
                if self.sx % 10 < 5:
                    self.sx = self.sx - self.sx % 10
                else:
                    self.sx = self.sx + (10 - self.sx % 10)
                if self.sy % 10 < 5:
                    self.sy = self.sy - self.sy % 10
                else:
                    self.sy = self.sy + (10 - self.sy % 10)

            if not pressed[0] and self.sx != 0:
                self.addObj()
                self.sx = 0
                self.sy = 0

            if pressed[2]:
                loc1 = pygame.mouse.get_pos()
                loc = [loc1[0] + self.x - self.farthestRight, loc1[1]]
                for plat in self.platforms:
                    if plat.dims[0] + plat.dims[2] > loc[0] > plat.dims[0] and plat.dims[1] + plat.dims[3] > loc[
                        1] > plat.dims[1]:
                        if self.placeChoice != 5:
                            self.platforms.remove(plat)
                        else:
                            plat.dims[0] = loc[0] - plat.dims[2] / 2
                            plat.dims[1] = loc[1] - plat.dims[3] / 2
                            for i in range(2):
                                if plat.dims[i] % 10 < 5:
                                    plat.dims[i] -= plat.dims[i] % 10
                                else:
                                    plat.dims[i] += (10 - plat.dims[i] % 10)
                for en in self.enemies:
                    if en.dims[0] + en.dims[2] > loc[0] > en.dims[0] and en.dims[1] + en.dims[3] > loc[
                        1] > en.dims[1]:
                        self.enemies.remove(en)

        if self.state == -1:
            text = self.font.render(str("Game Over"), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (self.width / 2, self.height / 2)
            self.screen.blit(text, textRect)

            text = self.font.render(str("Press space to try again"), True, (0, 0, 0))
            textRect.center = (self.width / 2, self.height / 2 + 100)
            self.screen.blit(text, textRect)

            keys = pygame.key.get_pressed()
            if keys[pygame.key.key_code(" ")]:
                self.state = 0

        if not self.forAi:
            pygame.display.update()

    def handleEnemies(self):
        for enemy in self.enemies:
            enemy.display(self.x, self.farthestRight, self.screen, self.d)
            if enemy.ty == 1:
                if not self.p and enemy.dims[0] - self.x < self.width:
                    enemy.dims[0] += enemy.vx
                    if self.x == self.farthestRight:
                        enemy.dims[0] -= self.vx
                    enemy.dims[1] += enemy.vy
                    enemy.vy += self.GRAV
                    for plat in self.platforms:
                        enemy.platCollision(plat)
            if enemy.ty == -1:
                if self.x == self.farthestRight:
                    enemy.dims[0] += self.vx
                enemy.dims[1] += enemy.vy
                enemy.vy += self.GRAV
                if enemy.fc <= self.frameCount:
                    enemy.ty = 0
                    enemy.dims[0] = -10000
                    enemy.dims[1] = -10000
            c = 0
            if enemy.ty > 0:
                c = self.detectEnemyCollision(enemy)
            if c == 1:
                enemy.ty *= -1
                enemy.fc = self.frameCount + 300
                enemy.vy = -2
                enemy.c = self.DEFEATED_COLOR
                self.score += 50
            if c == 2:
                self.state = -1
                self.enemies = [Enemy([900, self.height - 200, 40, 40], 1, self.ENEMY_COLOR),
                                Enemy([1100, self.height - 200, 40, 40], 1, self.ENEMY_COLOR)]

    def handlePlatforms(self):
        for platform in self.platforms:
            platform.display(self.x, self.farthestRight, self.screen, self.d)
            dc = self.detectPlatCollision(platform)
            if dc == 1:
                self.grounded = True
                self.y = platform.dims[1] - self.ph
                self.vy = 0
            if dc == 2:
                self.vy = .1
                self.y = platform.dims[1] + platform.dims[3] + 1
                self.jump_start = self.y + 1
            if dc == 3:
                self.vx = 0
                self.x = platform.dims[0] - self.pw
            if dc == 4:
                self.vx = 0
                self.x = platform.dims[0] + platform.dims[2]

    def handlePlayer(self):
        rx = self.farthestRight
        if self.x < self.farthestRight:
            rx = self.x
        self.d.rect(self.screen, self.PLAYER_COLOR, [rx, self.y, self.pw, self.ph])

        self.x += self.vx
        self.y += self.vy
        self.vy += self.GRAV

        if self.y > self.height - self.ph:
            self.state = 1
        if self.x <= 0:
            self.x = 0
            self.vx = 0

        if self.run:
            if self.right:
                self.vx += self.RUN_ACCEL
            if self.left:
                self.vx -= self.RUN_ACCEL
            self.ground_limit = self.MAX_RUN
        else:
            if self.right:
                self.vx += self.WALK_ACCEL
            if self.left:
                self.vx -= self.WALK_ACCEL
            self.ground_limit = self.MAX_RUN * 3 / 5

        if self.grounded:
            if (not self.left and not self.right) or (self.left and self.vx > 0) or (self.right and self.vx < 0):
                self.vx -= self.vx * self.FRIC

            if self.vx > self.ground_limit:
                self.vx = self.ground_limit
            if self.vx < -self.ground_limit:
                self.vx = -self.ground_limit

            if self.jump:
                self.vy = self.JUMP_START_BOOST
                self.grounded = False
                self.jump_start = self.y - self.JUMP_APEX
                self.air_limit = self.ground_limit
        else:
            if self.vy < 0 and self.jump and self.y >= self.jump_start:
                self.vy -= self.GRAV * (1 - self.JUMP_HOLD_GRAV)
            else:
                self.jump_start = self.height + self.JUMP_APEX
            if self.vx > self.air_limit:
                self.vx = self.air_limit
            if self.vx < -self.air_limit:
                self.vx = -self.air_limit
            if self.air_limit == self.MAX_RUN and abs(self.vx) < self.MAX_RUN * 3 / 5:
                self.air_limit = self.MAX_RUN * 3 / 5
        if int(self.vx) == 0 and self.killTimer == -1:
            self.killTimer = self.frameCount + 500
        if int(self.vx) != 0:
            self.killTimer = -1
        if self.killTimer == self.frameCount:
            self.state = 1
            self.killTimer = -1

    def detectPlatCollision(self, p):
        bw = p.dims[2]
        bh = p.dims[3]
        bx = p.dims[0]
        by = p.dims[1]
        tx = self.x
        ty = self.y
        if abs((tx + self.pw / 2) - (bx + bw / 2)) < (bw / 2 + self.pw / 2) and abs(
                (ty + self.ph / 2) - (by + bh / 2)) < (
                bh / 2 + self.ph / 2):
            if ty + self.ph < by + self.vy and self.vy > 0:
                return 1
            if ty > by + bh + self.vy - 1 and self.vy < 0:
                return 2
            if tx + self.pw < bx + self.vx and self.vx > 0:
                return 3
            if self.vx < 0 and tx > bx + bw - self.MAX_RUN - 1:
                return 4
            return 0

    def detectEnemyCollision(self, e):
        bw = e.dims[2]
        bh = e.dims[3]
        bx = e.dims[0]
        by = e.dims[1]
        tx = self.x
        ty = self.y
        if abs((tx + self.pw / 2) - (bx + bw / 2)) < (bw / 2 + self.pw / 2) and abs(
                (ty + self.ph / 2) - (by + bh / 2)) < (
                bh / 2 + self.ph / 2):
            if ty + self.ph < by + self.vy and self.vy > 0:
                return 1
            else:
                return 2
        else:
            return 0

    def keyPressed(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.key.key_code("a")]:
            self.left = True
        else:
            self.left = False
        if keys[pygame.key.key_code("d")]:
            self.right = True
        else:
            self.right = False
        if keys[pygame.key.key_code(" ")]:
            self.jump = True
        else:
            self.jump = False
        if keys[pygame.key.key_code("w")]:
            self.run = True
        else:
            self.run = False
        if keys[pygame.key.key_code("p")]:
            self.p = not self.p
        if keys[pygame.key.key_code("1")]:
            self.placeChoice = 1
        if keys[pygame.key.key_code("2")]:
            self.placeChoice = 2
        if keys[pygame.key.key_code("3")]:
            self.placeChoice = 3
        if keys[pygame.key.key_code("4")]:
            self.placeChoice = 4
        if keys[pygame.key.key_code("5")]:
            self.placeChoice = 5
        if keys[pygame.key.key_code("0")]:
            self.printStarts()
        if keys[pygame.key.key_code("4")]:
            self.aiGetInput(30, 45)

    def aiKeyPress(self, output):
        if output[0] == 1:
            self.jump = True
        else:
            self.jump = False

        if output[1] == 1:
            self.left = True
        else:
            self.left = False

        if output[2] == 1:
            self.right = True
        else:
            self.right = False

        if output[3] == 1:
            self.run = True
        else:
            self.run = False

    def printStarts(self):
        if self.frameCount >= self.printTimer:
            pickle.dump(self.platforms, open("Level1Platforms.p", 'wb'))
            pickle.dump(self.enemies, open("Level1Enemies.p", 'wb'))
            self.printTimer = self.frameCount + 90

    def addObj(self):
        pos = pygame.mouse.get_pos()
        x_2 = max(self.sx, pos[0] + self.x - self.farthestRight)
        x_1 = min(self.sx, pos[0] + self.x - self.farthestRight)
        y_2 = max(self.sy, pos[1])
        y_1 = min(self.sy, pos[1])
        if self.placeChoice == 1:
            self.platforms.append(Platform([x_1, y_1, x_2 - x_1, y_2 - y_1], 0, self.GROUND_COLOR))
        if self.placeChoice == 2:
            self.platforms.append(Platform([x_1, y_1, x_2 - x_1, y_2 - y_1], 1, self.PLAT_COLOR))
        if self.placeChoice == 3:
            self.enemies.append(Enemy([x_1, y_1, x_2 - x_1, y_2 - y_1], 1, self.ENEMY_COLOR))
        if self.placeChoice == 4:
            self.platforms.append(Platform([self.sx, self.sy, 30, 30], 1, self.PLAT_COLOR))

    def runGame(self):
        self.setup()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            self.keyPressed()
            self.draw()
            self.frameCount += 1
            clock.tick(60)
            if self.state == 1:
                return 0

    def aiGetInput(self, inputr, inputc):
        input = [[0 for x in range(inputc)] for y in range(inputr)]
        rScale = int(self.screen.get_height() / inputr)
        cScale = int(self.screen.get_width() / inputc)

        offset = 0
        if self.x >= self.farthestRight:
            offset = self.farthestRight - self.x
        value = 14
        r = self.y
        while r < self.y + self.ph:
            c = self.x
            if c > self.farthestRight:
                c = self.farthestRight
            while c < min(self.farthestRight, self.x) + self.pw:
                input[int(r / rScale)][int(c / cScale)] = value
                c += cScale
            r += rScale
        for plat in self.platforms:
            if 0 <= plat.dims[0] + offset <= self.width:
                if plat.ty == 0:
                    value = 11
                else:
                    value = 12
                r = plat.dims[1]
                while r < plat.dims[1] + plat.dims[3]:
                    if int(r / rScale) >= inputr:
                        break
                    c = plat.dims[0] + offset
                    while c < plat.dims[0] + plat.dims[2]:
                        if int(c/cScale) >= inputc:
                            break
                        if input[int(r / rScale)][int(c / cScale)] < value:
                            input[int(r / rScale)][int(c / cScale)] = value
                        c += cScale
                    r += rScale

        for en in self.enemies:
            if 0 <= en.dims[0] + offset <= self.width:
                if en.ty == 1:
                    value = 13
                else:
                    value = 10
                r = en.dims[1]
                while r < en.dims[1] + en.dims[3]:
                    if int(r / rScale) >= inputr:
                        break
                    c = en.dims[0] + offset
                    while c < en.dims[0] + en.dims[2]:
                        if int(c/cScale) >= inputc-1:
                            break
                        if input[int(r / rScale)][int(c / cScale)] < value:
                            input[int(r / rScale)][int(c / cScale)] = value
                        c += cScale
                    r += rScale

        #for row in input:
        #    print(row)
        return input

    def aiRunGame(self, b, inpr, inpc):
        print("Ai running game")
        self.setup()
        while self.state == 0 and self.frameCount < 21000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            self.draw()
            if self.frameCount % 3 == 0:
                self.aiKeyPress(b.runInput(self.aiGetInput(inpr, inpc)))
            self.frameCount += 1
        b.fitness = self.x + self.score
        if self.x > 3000:
            b.fitness += 500
        print("ai lost with score of " + str(b.fitness))
        return self.x + self.score


if __name__ == '__main__':
    g = MyGame(False)
    g.runGame()


"""
    def aiGetInput(self, inputr, inputc):
        input = [[0 for x in range(inputc)] for y in range(inputr)]
        r = 0
        rScale = int(self.screen.get_height() / inputr)
        cScale = int(self.screen.get_width() / inputc)
        while r < inputr:
            c = 0
            while c < inputc:
                colorsInArea = dict()
                pr = r * rScale
                while pr < (r + 1) * rScale:
                    pc = c * cScale
                    while pc < (c + 1) * cScale:
                        color = self.convertColortoNum(self.screen.get_at((pc, pr)))
                        if not color == 0:
                            if colorsInArea.__contains__(color):
                                colorsInArea[color] += 1
                            else:
                                colorsInArea[color] = 1
                        pc += 3
                    pr += 3
                highest = 0
                for (color, value) in colorsInArea.items():
                    if value > highest:
                        if not color == 0:
                            input[r][c] = color
                            highest = value
                c += 1
            r += 1
        #for row in input:
        #    print(row)
        return input
    """
