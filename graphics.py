import pyglet
from pyglet.gl import glColor3f


class Graphics(object):
    # Pixels per cell
    ppc = 20

    @classmethod
    def draw(cls, i, j, rgb):
        x1, y1 = i * cls.ppc + 1, j * cls.ppc + 1
        x2, y2 = i * cls.ppc + cls.ppc - 1, y1
        x3, y3 = x2, j * cls.ppc + cls.ppc - 1
        x4, y4 = x1, y3
        pyglet.gl.glColor3f(rgb[0], rgb[1], rgb[2])
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (x1, y1, x2, y2, x3, y3, x4, y4)))
