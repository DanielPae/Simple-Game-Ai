import pygame

pygame.init()
d = pygame.draw
width = 0
height = 0
screen = pygame.display.set_mode((width, height))
frameCount = 0
font = pygame.font.Font('freesansbold.ttf', 32)


class Platform:
    def __init__(self, dims, ty):
        self.dims = dims
        self.ty = ty

    def display(self):
        c = (0, 0, 0)
        if self.ty == 0:
            c = (7, 99, 81)
        if self.ty == 1:
            c = (255, 226, 176)
        if self.ty == 2:
            c = (255, 226, 176)
        d.rect(screen, c, self.dims)

    def move(self, x):
        self.dims[0] += x

    def moveTo(self, x, y):
        self.dims[0] = x
        self.dims[1] = y

    def detectCollision(self):
        bw = self.dims[2]
        bh = self.dims[3]
        bx = self.dims[0]
        by = self.dims[1]
        tx = x
        ty = y
        if abs((tx + pw / 2) - (bx + bw / 2)) < (bw / 2 + pw / 2) and abs((ty + ph / 2) - (by + bh / 2)) < (
                bh / 2 + ph / 2):
            if ty + ph < by + vy and vy > 0:
                return 1
            if ty > by + bh + vy and vy < 0:
                return 2
            if tx + pw < bx + vx and vx > 0:
                return 3
            if vx < 0 and tx > bx + bw/2:
                return 4
            return 0


class Enemy:
    def __init__(self, dims, ty):
        dims[2] = 40
        dims[3] = 40
        self.dims = dims
        self.ty = ty
        self.vx = 0
        self.vy = 0
        self.fc = 0
        if ty == 1:
            self.vx = -2

    def platCollision(self, p):
        bx = p.dims[0]
        by = p.dims[1]
        bw = p.dims[2]
        bh = p.dims[3]
        tx = self.dims[0]
        ty = self.dims[1]
        if abs((tx + self.dims[2] / 2) - (bx + bw / 2)) < (bw / 2 + self.dims[2] / 2) and abs(
                (ty + self.dims[3] / 2) - (by + bh / 2)) < (bh / 2 + self.dims[3] / 2):
            if ty + self.dims[3] < by + self.vy and self.vy > 0:
                self.vy = 0
                self.dims[1] = by - self.dims[3]
            else:
                self.vx *= -1

    def playerCollision(self):
        bw = self.dims[2]
        bh = self.dims[3]
        bx = self.dims[0]
        by = self.dims[1]
        tx = x
        ty = y
        if abs((tx + pw / 2) - (bx + bw / 2)) < (bw / 2 + pw / 2) and abs((ty + ph / 2) - (by + bh / 2)) < (
                bh / 2 + ph / 2):
            if ty + ph < by + vy and vy > 0:
                return 1
            else:
                return 2
        else:
            return 0

    def display(self):
        if self.ty == 1:
            d.rect(screen, (255, 179, 218), self.dims)
            if not p:
                self.dims[0] += self.vx
                if x == 300:
                    self.dims[0] -= vx
                self.dims[1] += self.vy
                self.vy += GRAV
                for plat in platforms:
                    self.platCollision(plat)
        if self.ty == -1:
            d.rect(screen, (250, 103, 97), self.dims)
            if x == 300:
                self.dims[0] += self.vx - vx
            self.dims[1] += self.vy
            self.vy += GRAV
            if self.fc <= frameCount:
                self.ty = 0
                self.dims[0] = -10000
                self.dims[1] = -10000


state = 0
x = 0
y = 0
vx = 0
vy = 0
pw = 40
ph = 60
placeChoice = 0
p = False
GRAV = .2
FRIC = .075
MAX_RUN = 8
ground_limit = MAX_RUN
air_limit = MAX_RUN
left = False
right = False
jump = False
run = False
grounded = False
platforms = [Platform([0, 0, 150, 20], 0)]
enemies = [Enemy([900, height - 200, 40, 40], 0)]

sx = 0
sy = 0


def setup():
    global width
    global height
    global screen
    global x
    global y
    global platforms
    global enemies

    width = 1500
    height = 800
    screen = pygame.display.set_mode((width, height))

    x = 300
    y = height - 350

    platforms = [Platform([0, height - 100, 2000, 100], 0),
                 Platform([400, height - 200, 100, 20], 1),
                 Platform([750, height - 250, 50, 50], 1)]

    enemies = [Enemy([900, height - 200, 40, 40], 1),
               Enemy([1100, height - 200, 40, 40], 1)]


def draw():
    global screen
    global state
    global sx
    global sy

    screen.fill((255, 255, 255))

    if state == 0:
        handlePlayer()
        handlePlatforms()
        handleEnemies()

        pressed = pygame.mouse.get_pressed(3)

        if pressed[0] and sx == 0:
            loc = pygame.mouse.get_pos()
            sx = loc[0]
            sy = loc[1]
            if sx % 10 < 5:
                sx = sx - sx % 10
            else:
                sx = sx + (10 - sx % 10)
            if sy % 10 < 5:
                sy = sy - sy % 10
            else:
                sy = sy + (10 - sy % 10)

        if not pressed[0] and sx != 0:
            addObj()
            sx = 0
            sy = 0

        if pressed[2]:
            loc = pygame.mouse.get_pos()
            for plat in platforms:
                if plat.dims[0] + plat.dims[2] > loc[0] > plat.dims[0] and plat.dims[1] + plat.dims[3] > loc[
                1] > plat.dims[1]:
                    platforms.remove(plat)
            for en in enemies:
                if en.dims[0] + en.dims[2] > loc[0] > en.dims[0] and en.dims[1] + en.dims[3] > loc[
                1] > en.dims[1]:
                    enemies.remove(en)

    if state == -1:
        text = font.render(str("Game Over"), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (width / 2, height / 2)
        screen.blit(text, textRect)

        text = font.render(str("Press space to try again"), True, (0, 0, 0))
        textRect.center = (width / 2, height / 2 + 100)
        screen.blit(text, textRect)

        keys = pygame.key.get_pressed()
        if keys[pygame.key.key_code(" ")]:
            state = 0

    pygame.display.update()


def handleEnemies():
    global state
    global x
    global y
    global enemies

    for enemy in enemies:
        enemy.display()
        c = 0
        if enemy.ty > 0:
            c = enemy.playerCollision()
        if c == 1:
            enemy.ty *= -1
            enemy.fc = frameCount + 300
            enemy.vy = -2
        if c == 2:
            state = -1
            enemies = [Enemy([900, height - 200, 40, 40], 1),
                       Enemy([1100, height - 200, 40, 40], 1)]


def handlePlatforms():
    global grounded
    global y
    global vy
    global x
    global vx

    m = x == 300 and platforms[0].dims[0] - vx <= 0
    for platform in platforms:
        platform.display()
        if m:
            platform.move(-vx)
        dc = platform.detectCollision()
        if dc == 1:
            grounded = True
            y = platform.dims[1] - ph
            vy = 0
        if dc == 2:
            vy *= -1
        if dc == 3:
            vx = 0
            x = platform.dims[0] - pw
        if dc == 4:
            vx = 0
            x = platform.dims[0] + platform.dims[2]


def handlePlayer():
    global x
    global y
    global vx
    global vy
    global grounded
    global air_limit
    global ground_limit

    d.rect(screen, (180, 176, 255), [x, y, pw, ph])

    if platforms[0].dims[0] - vx >= 0 or x < 300:
        x += vx
    y += vy
    vy += GRAV

    if y > height - ph:
        y = height - ph
        vy = 0
        grounded = True
    if x <= 0:
        x = 0
        vx = 0
    if x > 300:
        x = 300

    if run:
        if right:
            vx += .2
        if left:
            vx -= .2
        ground_limit = MAX_RUN
    else:
        if right:
            vx += .175
        if left:
            vx -= .175
        ground_limit = MAX_RUN * 3 / 5

    if grounded:
        if not left and not right:
            vx -= vx * FRIC

        if vx > ground_limit:
            vx = ground_limit
        if vx < -ground_limit:
            vx = -ground_limit

        if jump:
            vy = -5
            grounded = False
            air_limit = ground_limit
    else:
        if vy < 0 and jump:
            vy -= GRAV * 2 / 3
        if vx > air_limit:
            vx = air_limit
        if vx < -air_limit:
            vx = -air_limit
        if air_limit == MAX_RUN and abs(vx) < MAX_RUN * 3 / 5:
            air_limit = MAX_RUN * 3 / 5


def keyPressed():
    global left
    global right
    global jump
    global run
    global p
    global placeChoice

    keys = pygame.key.get_pressed()

    if keys[pygame.key.key_code("a")]:
        left = True
    else:
        left = False
    if keys[pygame.key.key_code("d")]:
        right = True
    else:
        right = False
    if keys[pygame.key.key_code(" ")]:
        jump = True
    else:
        jump = False
    if keys[pygame.key.key_code("w")]:
        run = True
    else:
        run = False
    if keys[pygame.key.key_code("p")]:
        p = not p
    if keys[pygame.key.key_code("1")]:
        placeChoice = 1
    if keys[pygame.key.key_code("2")]:
        placeChoice = 2
    if keys[pygame.key.key_code("3")]:
        placeChoice = 3
    if keys[pygame.key.key_code("4")]:
        placeChoice = 4
    if keys[pygame.key.key_code("0")]:
        printStarts()


def printStarts():
    print("Platforms:")
    for plat in platforms:
        print("Platform([" + str(plat.dims[0]) + ", " + str(plat.dims[1]) + ", " +
              str(plat.dims[2]) + ", " + str(plat.dims[3]) + "], " + str(plat.ty) + ")")
    print("Enemies:")
    for en in enemies:
        print("Enemy([" + str(en.dims[0]) + ", " + str(en.dims[1]) + ", " +
              str(en.dims[2]) + ", " + str(en.dims[3]) + "], " + str(en.ty) + ")")


def addObj():
    global platforms
    global enemies

    pos = pygame.mouse.get_pos()
    x_2 = max(sx, pos[0])
    x_1 = min(sx, pos[0])
    y_2 = max(sy, pos[1])
    y_1 = min(sy, pos[1])
    if placeChoice == 1:
        platforms.append(Platform([x_1, y_1, x_2 - x_1, y_2 - y_1], 0))
    if placeChoice == 2:
        platforms.append(Platform([x_1, y_1, x_2 - x_1, y_2 - y_1], 1))
    if placeChoice == 3:
        enemies.append(Enemy([x_1, y_1, x_2 - x_1, y_2 - y_1], 1))
    if placeChoice == 4:
        platforms.append(Platform([sx, sy, 40, 40], 1))


if __name__ == '__main__':
    setup()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keyPressed()
        draw()
        frameCount += 1
        clock.tick(60)
