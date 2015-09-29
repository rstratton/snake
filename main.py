#!/usr/bin/env python2

import random
import pyglet

from graphics import Graphics
from gameobj import Snake
from gameobj import Food
from gameobj import Walls
from gameobj import World
from util import Direction

world  = World.instance
snake  = Snake(5, 5)
Walls()
Food(random.choice(world.get_free_positions()))
Food(random.choice(world.get_free_positions()))
Food(random.choice(world.get_free_positions()))

window = pyglet.window.Window(width  = Graphics.ppc * world.width,
                              height = Graphics.ppc * world.height)

@window.event
def on_draw():
    window.clear()
    world.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        snake.direction = Direction.UP
    elif symbol == pyglet.window.key.A:
        snake.direction = Direction.LEFT
    elif symbol == pyglet.window.key.S:
        snake.direction = Direction.DOWN
    elif symbol == pyglet.window.key.D:
        snake.direction = Direction.RIGHT

def update(dt):
    world.update(dt)

pyglet.clock.schedule_interval(update, 0.0166666)
pyglet.app.run()
