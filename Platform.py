class Platform:
    def __init__(self, dims, ty, screen, d):
        self.dims = dims
        self.ty = ty
        self.screen = screen
        self.d = d

    def display(self, x, farthestRight):
        c = (0, 0, 0)
        if self.ty == 0:
            c = (7, 99, 81)
        if self.ty == 1:
            c = (255, 226, 176)
        if self.ty == 2:
            c = (255, 226, 176)
        cop = self.dims[0]
        if x >= farthestRight:
            self.dims[0] = cop - x + farthestRight
        self.d.rect(self.screen, c, self.dims)
        self.dims[0] = cop

    def move(self, x):
        self.dims[0] += x

    def moveTo(self, x, y):
        self.dims[0] = x
        self.dims[1] = y

