class Enemy:
    def __init__(self, dims, ty, c):
        dims[2] = 35
        dims[3] = 35
        self.dims = dims
        self.ty = ty
        self.vx = 0
        self.vy = 0
        self.fc = 0
        self.c = c
        if ty == 1:
            self.vx = -.8

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

    def display(self, x, farthestRight, screen, d):
        cop = self.dims[0]
        if x >= farthestRight:
            self.dims[0] = cop - x + farthestRight
        d.rect(screen, self.c, self.dims)
        self.dims[0] = cop
