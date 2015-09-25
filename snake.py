import pyglet

class Grid(object):
    def __init__(self, width, height, pixels_per_cell=20):
        self.ppc, self.width, self.height = pixels_per_cell, width, height
        # Initialize 2D array of booleans to 'False'
        self._cells = [[False] * width for _ in xrange(height)]
        # Set boundary cells to 'True'
        for i in xrange(width):
            self._cells[i][0] = self._cells[i][height - 1] = True
        for i in xrange(1, height - 1):
            self._cells[0][i] = self._cells[width - 1][i] = True

    def draw(self):
        for i, column in enumerate(self._cells):
            for j, cell in enumerate(column):
                if cell:
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1, y1 = i * self.ppc, j * self.ppc
        x2, y2 = i * self.ppc + self.ppc, y1
        x3, y3 = x2, j * self.ppc + self.ppc
        x4, y4 = x1, y3
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (x1, y1, x2, y2, x3, y3, x4, y4)))
