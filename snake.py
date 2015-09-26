import pyglet
from pyglet.gl import glColor3f



# From http://stackoverflow.com/a/1695250
def _enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Direction = _enum("UP", "DOWN", "LEFT", "RIGHT")



class LinkedList(object):
    def __init__(self):
        self.head, self.tail = None, None

    def append(self, data):
        if self.head is None:
            self.head = self.tail = _Node(data=data)
        else:
            new_node = _Node(prev=self.tail, data=data)
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self, data):
        if self.head is None:
            self.head = self.tail = _Node(data=data)
        else:
            new_node = _Node(next=self.head, data=data)
            self.head.prev = new_node
            self.head = new_node

    def remove_head(self):
        data = self.head.data
        self.head.next.prev = None
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data

    def remove_tail(self):
        data = self.tail.data
        self.tail.prev.next = None
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        return data

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __getitem__(self, i):
        for idx, data in enumerate(self):
            if idx == i:
                return data
        raise IndexError()

    def __len__(self):
        return sum([1 for _ in self])

    def __repr__(self):
        return " --> ".join([str(data) for data in self])

class _Node(object):
    def __init__(self, next=None, prev=None, data=None):
        self.next, self.prev, self.data = next, prev, data



CellValue = _enum("WALL", "SNAKE", "EMPTY", "FOOD")

class Grid(object):
    def __init__(self, width, height, pixels_per_cell=20):
        self.ppc, self.width, self.height = pixels_per_cell, width, height
        # Initialize 2D array of booleans to 'False'
        self._cells = [[CellValue.EMPTY] * width for _ in xrange(height)]
        # Set boundary cells to 'WALL'
        for i in xrange(width):
            self._cells[i][0] = self._cells[i][height - 1] = CellValue.WALL
        for i in xrange(1, height - 1):
            self._cells[0][i] = self._cells[width - 1][i] = CellValue.WALL

    def draw(self):
        for i, column in enumerate(self._cells):
            for j, cell in enumerate(column):
                if cell is not CellValue.EMPTY:
                    self._draw_cell(i, j, cell)

    def _draw_cell(self, i, j, cell):
        x1, y1 = i * self.ppc + 1, j * self.ppc + 1
        x2, y2 = i * self.ppc + self.ppc - 1, y1
        x3, y3 = x2, j * self.ppc + self.ppc - 1
        x4, y4 = x1, y3
        if cell is CellValue.WALL:
            pyglet.gl.glColor3f(0, 0, 1)
        elif cell is CellValue.SNAKE:
            pyglet.gl.glColor3f(0, 1, 0)
        elif cell is CellValue.FOOD:
            pyglet.gl.glColor3f(1, 0, 0)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (x1, y1, x2, y2, x3, y3, x4, y4)))

    def set_cell(self, i, j, value):
        self._cells[i][j] = value



class Snake(object):
    def __init__(self, x, y, grid, length=5):
        self._segments = LinkedList()
        self._grid = grid
        self._timer = 0
        self._TIMER_THRESHOLD = 0.75
        for i in xrange(length):
            self._segments.append(_SnakeSegment(x, y - i, Direction.UP))
        self._register_snake_on_grid()

    def _register_snake_on_grid(self):
        for segment in self._segments:
            self._grid.set_cell(segment.x, segment.y, CellValue.SNAKE)

    def move(self):
        head = self._segments[0]
        new_segment = _SnakeSegment(head.x,
                                    head.y,
                                    head.direction)
        old_segment = self._segments.remove_tail()

        if head.direction == Direction.UP:
            new_segment.y += 1
        elif head.direction == Direction.LEFT:
            new_segment.x -= 1
        elif head.direction == Direction.DOWN:
            new_segment.y -= 1
        elif head.direction == Direction.RIGHT:
            new_segment.x += 1

        self._grid.set_cell(new_segment.x, new_segment.y, CellValue.SNAKE)
        self._grid.set_cell(old_segment.x, old_segment.y, CellValue.EMPTY)
        self._segments.prepend(new_segment)

    def update(self, dt):
        self._timer += dt
        if self._timer >= self._TIMER_THRESHOLD:
            self.move()
            self._timer = self._timer % self._TIMER_THRESHOLD

    def set_direction(self, dir):
        head, prev = self._segments[0], self._segments[1]
        if not ((dir == Direction.UP and prev.direction == Direction.DOWN) or
                (dir == Direction.LEFT and prev.direction == Direction.RIGHT) or
                (dir == Direction.DOWN and prev.direction == Direction.UP) or
                (dir == Direction.RIGHT and prev.direction == Direction.LEFT)):
            head.direction = dir

class _SnakeSegment(object):
    def __init__(self, x, y, direction):
        self.x, self.y, self.direction = x, y, direction

    def __repr__(self):
        return "_SnakeSegment({0}, {1}, {2})".format(self.x, self.y,
                                                     self.direction)

