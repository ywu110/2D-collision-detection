import math

class UniformGrid:
    """
    Implements a uniform grid spatial index to reduce the number of collision checks.
    """
    def __init__(self, balls, cell_size):
        self.cell_size = cell_size
        self.grid = {}
        self.build_grid(balls)

    def build_grid(self, balls):
        """
        Build the grid by mapping each cell to the list of balls that occupy it.
        """
        self.grid = {}
        for ball in balls:
            min_cell_x = int((ball.x - ball.radius) // self.cell_size)
            max_cell_x = int((ball.x + ball.radius) // self.cell_size)
            min_cell_y = int((ball.y - ball.radius) // self.cell_size)
            max_cell_y = int((ball.y + ball.radius) // self.cell_size)
            for cx in range(min_cell_x, max_cell_x + 1):
                for cy in range(min_cell_y, max_cell_y + 1):
                    if (cx, cy) not in self.grid:
                        self.grid[(cx, cy)] = []
                    self.grid[(cx, cy)].append(ball)

    def query_range(self, cx, cy, r):
        """
        Return a list of balls whose centers are within a circle centered at (cx, cy) with radius r.
        """
        result = []
        seen = set()
        min_cell_x = int((cx - r) // self.cell_size)
        max_cell_x = int((cx + r) // self.cell_size)
        min_cell_y = int((cy - r) // self.cell_size)
        max_cell_y = int((cy + r) // self.cell_size)
        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                if (cell_x, cell_y) in self.grid:
                    for ball in self.grid[(cell_x, cell_y)]:
                        if id(ball) in seen:
                            continue
                        seen.add(id(ball))
                        dx = ball.x - cx
                        dy = ball.y - cy
                        if dx * dx + dy * dy <= r * r:
                            result.append(ball)
        return result

class KDNode:
    """
    A node used in the KD-Tree.
    """
    def __init__(self, ball, plane, left=None, right=None):
        self.ball = ball
        self.plane = plane
        self.left = left
        self.right = right

    def __getitem__(self, idx):
        return self.ball.x if idx == 0 else self.ball.y

class KDTree:
    """
    Implements a KD-Tree for spatial queries.
    """
    def __init__(self, balls):
        self.root = self.build(balls)

    def build(self, balls, depth=0):
        if not balls:
            return None
        axis = depth % 2
        if axis == 0:
            balls.sort(key=lambda b: b.x)
        else:
            balls.sort(key=lambda b: b.y)
        median = len(balls) // 2
        node = KDNode(
            ball=balls[median],
            plane=axis,
            left=self.build(balls[:median], depth + 1),
            right=self.build(balls[median + 1:], depth + 1)
        )
        return node

    def range_search(self, cx, cy, r, result=None):
        if result is None:
            result = []
        self._range_search(self.root, cx, cy, r, 0, result)
        return result

    def _range_search(self, node, cx, cy, r, depth, result):
        if node is None:
            return
        dx = node.ball.x - cx
        dy = node.ball.y - cy
        if dx * dx + dy * dy <= r * r:
            result.append(node.ball)
        axis = node.plane
        if axis == 0:
            diff = cx - node.ball.x
        else:
            diff = cy - node.ball.y
        if diff < 0:
            self._range_search(node.left, cx, cy, r, depth + 1, result)
            if abs(diff) < r:
                self._range_search(node.right, cx, cy, r, depth + 1, result)
        else:
            self._range_search(node.right, cx, cy, r, depth + 1, result)
            if abs(diff) < r:
                self._range_search(node.left, cx, cy, r, depth + 1, result)
