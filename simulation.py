import math
import random
from PyQt5.QtGui import QColor
from datastruct import UniformGrid, KDTree

class Ball:
    """
    Represents a ball with position, velocity, radius, color and mass.
    The mass is computed as radius / 10.0.
    """
    def __init__(self, x, y, radius, vx, vy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = self.radius / 10.0

class SimulationEngine:
    """
    Manages the simulation including ball movement, collision detection and collision resolution.
    Supports switching between Uniform Grid and KD-Tree for collision detection.
    """
    def __init__(self, width, height, cell_size=120, collision_method="uniform"):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.collision_detection_method = collision_method
        self.balls = []

    def set_collision_method(self, method):
        """
        Set the collision detection method.
        Accepts "uniform" or "kd".
        """
        self.collision_detection_method = method

    def add_ball(self):
        """
        Try to add a new ball without overlapping existing balls.
        """
        for _ in range(20):
            x = random.randint(100, 800)
            y = random.randint(150, 500)
            radius = random.randrange(20, 60, 10)
            vx = random.randint(-10, 10)
            vy = random.randint(-10, 10)
            if vx == 0:
                vx = 1
            if vy == 0:
                vy = 1
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            overlap = False
            for b in self.balls:
                if math.hypot(b.x - x, b.y - y) < b.radius + radius:
                    overlap = True
                    break
            if not overlap:
                self.balls.append(Ball(x, y, radius, vx, vy, color))
                return
        print("Failed to place a new ball after multiple attempts.")
        
    def remove_ball(self):
        """
        Remove one ball from the simulation.
        This function removes the last ball in the list if any exist.
        """
        if self.balls:
            self.balls.pop()
        else:
            print("No ball to remove.")

    def handle_boundary(self, ball):
        """
        Check ball position against simulation boundaries and reflect velocity if needed.
        """
        if ball.x - ball.radius < 0:
            ball.x = ball.radius
            ball.vx = -ball.vx
        elif ball.x + ball.radius > self.width:
            ball.x = self.width - ball.radius
            ball.vx = -ball.vx
        if ball.y - ball.radius < 0:
            ball.y = ball.radius
            ball.vy = -ball.vy
        elif ball.y + ball.radius > self.height:
            ball.y = self.height - ball.radius
            ball.vy = -ball.vy

    def resolve_collision(self, b1, b2):
        """
        Resolve the collision between two balls by applying an impulse and correcting their positions.
        """
        dx = b2.x - b1.x
        dy = b2.y - b1.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        nx = dx / dist
        ny = dy / dist
        vx_rel = b1.vx - b2.vx
        vy_rel = b1.vy - b2.vy
        rel_vel_norm = vx_rel * nx + vy_rel * ny

        e = 1.0
        m1 = b1.mass
        m2 = b2.mass
        J = -(1 + e) * rel_vel_norm / (1 / m1 + 1 / m2)
        b1.vx += (J / m1) * nx
        b1.vy += (J / m1) * ny
        b2.vx -= (J / m2) * nx
        b2.vy -= (J / m2) * ny

        if abs(rel_vel_norm) < 0.05:
            separationImpulse = 0.05
            b1.vx -= separationImpulse * nx
            b1.vy -= separationImpulse * ny
            b2.vx += separationImpulse * nx
            b2.vy += separationImpulse * ny

        overlap_depth = (b1.radius + b2.radius) - dist
        if overlap_depth > 0:
            bias = 0.1 * overlap_depth
            corr1 = (overlap_depth + bias) * (m2 / (m1 + m2))
            corr2 = (overlap_depth + bias) * (m1 / (m1 + m2))
            b1.x -= corr1 * nx
            b1.y -= corr1 * ny
            b2.x += corr2 * nx
            b2.y += corr2 * ny

    def update(self):
        """
        Update the simulation by moving balls and checking collisions.
        The update is performed in substeps to improve stability.
        """
        dt_total = 1.0
        substeps = 10
        dt_sub = dt_total / substeps

        for _ in range(substeps):
            for ball in self.balls:
                ball.x += ball.vx * dt_sub
                ball.y += ball.vy * dt_sub
                self.handle_boundary(ball)

            if self.collision_detection_method == "uniform":
                ds = UniformGrid(self.balls, self.cell_size)
                query_func = ds.query_range
            elif self.collision_detection_method == "kd":
                ds = KDTree(self.balls)
                query_func = ds.range_search
            else:
                ds = UniformGrid(self.balls, self.cell_size)
                query_func = ds.query_range

            for ball in self.balls:
                candidates = query_func(ball.x, ball.y, ball.radius + 60)
                for other in candidates:
                    if other is ball or id(other) < id(ball):
                        continue
                    dx = other.x - ball.x
                    dy = other.y - ball.y
                    dist = math.hypot(dx, dy)
                    if dist < ball.radius + other.radius:
                        self.resolve_collision(ball, other)
