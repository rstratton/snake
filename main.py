#!/usr/bin/env python2

import pyglet
from snake import Grid, Snake, Direction

grid   = Grid(40, 40)
snake  = Snake(20, 20, grid)
window = pyglet.window.Window(width=grid.ppc * grid.width,
                              height=grid.ppc * grid.height)

@window.event
def on_draw():
    window.clear()
    grid.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        snake.set_direction(Direction.UP)
    elif symbol == pyglet.window.key.A:
        snake.set_direction(Direction.LEFT)
    elif symbol == pyglet.window.key.S:
        snake.set_direction(Direction.DOWN)
    elif symbol == pyglet.window.key.D:
        snake.set_direction(Direction.RIGHT)

def update(dt):
    snake.update(dt)

pyglet.clock.schedule_interval(update, 0.0166666)
pyglet.app.run()
