from graphics import *


class Draw:
    def __init__(self, field):
        self.border = 20
        self.bsize = 20

        self.field = field
        self.shape = self.field.shape

        self.win = GraphWin(width=self.shape[0] * self.bsize + self.border * 2,
                            height=self.shape[1] * self.bsize + self.border * 2)
        self.draw()

    def update(self, field):
        self.field = field
        self.draw()

    def draw(self):
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                rect = Rectangle(Point(x * self.bsize + self.border, y * self.bsize + self.border),
                                 Point(x * self.bsize + self.border + self.bsize,
                                       y * self.bsize + self.border + self.bsize))
                rect.setFill(self.get_color(self.field[x, y]))
                rect.setOutline(self.get_color(self.field[x, y]))
                rect.draw(self.win)

    def get_color(self, num):
        return color_rgb(int(0 + num * 200), int(200 - num * 200), int(100 + num * 100))
