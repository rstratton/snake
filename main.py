#!/usr/bin/env python2

import pyglet
from snake import Grid

grid   = Grid(40, 40)
window = pyglet.window.Window(width=grid.ppc*grid.width,
                              height=grid.ppc*grid.height)

@window.event
def on_draw():
    window.clear()
    grid.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        pyglet.app.exit()

pyglet.app.run()
