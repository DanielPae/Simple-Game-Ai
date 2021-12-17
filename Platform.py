class Platform:
    def __init__(self, dims, ty, c):
        self.dims = dims
        self.ty = ty
        self.c = c

    def display(self, x, farthestRight, screen, d):
        cop = self.dims[0]
        if x >= farthestRight:
            self.dims[0] = cop - x + farthestRight
        d.rect(screen, self.c, self.dims)
        self.dims[0] = cop

    def move(self, x):
        self.dims[0] += x

    def moveTo(self, x, y):
        self.dims[0] = x
        self.dims[1] = y

