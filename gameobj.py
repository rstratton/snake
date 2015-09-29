import pyglet
import random

from graphics import Graphics
from util import enum
from util import Vector
from util import Direction
from util import Singleton



class GameObject(object):
    _next_id = 0

    def __init__(self):
        self._id = GameObject.get_id()
        World.instance.add_obj(self)

    def kill(self):
        World.instance.remove_obj(self)

    @classmethod
    def get_id(cls):
        id = cls._next_id
        cls._next_id += 1
        return id


class Drawable(object):
    def __init__(self, pos, rgb_color):
        self.pos, self.color = pos, rgb_color

    def draw(self):
        Graphics.draw(self.pos.x, self.pos.y, self.color)


class Wall(GameObject, Drawable):
    def __init__(self, pos):
        Drawable.__init__(self, pos, (0, 0, 1))
        GameObject.__init__(self)


class Food(GameObject, Drawable):
    def __init__(self, pos):
        Drawable.__init__(self, pos, (1, 0, 0))
        GameObject.__init__(self)

    def kill(self):
        GameObject.kill(self)
        Food.spawn_random()

    @staticmethod
    def spawn_random(count=1):
        for _ in xrange(count):
            Food(random.choice(World.instance.get_free_positions()))



class _SnakeSegment(GameObject, Drawable):
    def __init__(self, pos, direction):
        self.direction = direction
        Drawable.__init__(self, pos, (0, 1, 0))
        GameObject.__init__(self)


class Snake(GameObject):
    def __init__(self, x, y, length=3):
        self._timer, self._TIMER_THRESHOLD = 0, 0.50
        self._segments = []
        for i in xrange(length):
            self._segments.append(_SnakeSegment(Vector(x, y - i), Direction.UP))
        GameObject.__init__(self)

    def move(self):
        head = self._segments[0]
        next_position = head.pos + head.direction
        obj_positions = World.instance.get_obj_positions()
        colliding_obj = obj_positions.get(next_position, None)
        if isinstance(colliding_obj, Wall):
            pyglet.app.exit()
        elif isinstance(colliding_obj, _SnakeSegment):
            pyglet.app.exit()
        elif isinstance(colliding_obj, Food):
            colliding_obj.kill()
        else:
            self._segments.pop().kill()
        self._segments.insert(0, _SnakeSegment(next_position, head.direction))

    @property
    def direction(self):
        return self._segments[0].direction

    @direction.setter
    def direction(self, value):
        head, prev = self._segments[0], self._segments[1]
        if not value + prev.direction == Direction.NEUTRAL:
            head.direction = value

    def update(self, dt):
        self._timer += dt
        if self._timer >= self._TIMER_THRESHOLD:
            self.move()
            self._timer = self._timer % self._TIMER_THRESHOLD


class Walls(GameObject):
    def __init__(self):
        self._walls = []
        for i in xrange(World.instance.width):
            self._walls.append(Wall(Vector(i, 0)))
            self._walls.append(Wall(Vector(i, World.instance.height - 1)))
        for j in xrange(1, World.instance.height - 1):
            self._walls.append(Wall(Vector(0, j)))
            self._walls.append(Wall(Vector(World.instance.width - 1, j)))


@Singleton
class World(object):
    def __init__(self):
        self._objects, self._positions = {}, None
        self.width, self.height = 10, 10

    def add_obj(self, obj):
        self._objects[obj._id] = obj

    def remove_obj(self, obj):
        del self._objects[obj._id]

    def get_obj_positions(self):
        if self._positions is None:
            self._positions = { obj.pos: obj for obj in self._objects.values() \
                                             if hasattr(obj, "pos") }
        return self._positions

    def get_free_positions(self):
        all_positions = [Vector(x, y) for x in xrange(self.width) \
                                      for y in xrange(self.height)]
        occupied_positions = [ obj.pos for obj in self._objects.values() \
                                       if hasattr(obj, "pos") ]
        return list(set(all_positions).difference(set(occupied_positions)))

    def draw(self):
        for obj in self._objects.values():
            if hasattr(obj, "draw"):
                obj.draw()

    def update(self, dt):
        self._positions = None
        for obj in self._objects.values():
            if hasattr(obj, "update"):
                obj.update(dt)
