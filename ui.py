import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from simulation import SimulationEngine

class BallWidget(QWidget):
    """
    A widget that displays the simulation. It uses a SimulationEngine instance
    to update the physics and draw the balls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create the simulation engine with the widget size.
        self.simulation_engine = SimulationEngine(width=1200, height=1000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # Around 60 frames per second.
        self.setMinimumSize(1200, 1000)

    def add_ball(self):
        """
        Add a new ball to the simulation.
        """
        self.simulation_engine.add_ball()
    
    def remove_ball(self):
        """
        Remove one ball from the simulation.
        """
        self.simulation_engine.remove_ball()

    def update_simulation(self):
        """
        Update the simulation and request a redraw.
        """
        self.simulation_engine.update()
        self.update()

    def paintEvent(self, event):
        """
        Draw all balls from the simulation engine onto the widget.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)
        for ball in self.simulation_engine.balls:
            painter.setBrush(ball.color)
            painter.drawEllipse(int(ball.x - ball.radius),
                                int(ball.y - ball.radius),
                                int(ball.radius * 2),
                                int(ball.radius * 2))

class MainWindow(QWidget):
    """
    Main window that contains the simulation display and a control panel.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt 2D Collision with Switchable Data Structures")
        self.layout_main = QHBoxLayout(self)
        self.ball_widget = BallWidget(self)
        self.layout_main.addWidget(self.ball_widget, 1)
        self.right_panel = QVBoxLayout()
        self.layout_main.addLayout(self.right_panel)

        # Button to add a new ball.
        self.button_add_ball = QPushButton("Add Ball")
        self.button_add_ball.clicked.connect(self.ball_widget.add_ball)
        self.right_panel.addWidget(self.button_add_ball)
        
        # Button to remove a ball.
        self.button_remove_ball = QPushButton("Remove Ball")
        self.button_remove_ball.clicked.connect(self.ball_widget.remove_ball)
        self.right_panel.addWidget(self.button_remove_ball)

        # Dropdown to select collision detection method.
        self.combo_collision = QComboBox()
        self.combo_collision.addItem("Uniform Grid")
        self.combo_collision.addItem("KD-Tree")
        self.combo_collision.setMinimumWidth(260)
        self.combo_collision.currentIndexChanged.connect(self.change_collision_method)
        self.right_panel.addWidget(self.combo_collision)

        self.setLayout(self.layout_main)

    def change_collision_method(self, index):
        """
        Update the simulation engine collision method based on the dropdown selection.
        """
        if index == 0:
            self.ball_widget.simulation_engine.set_collision_method("uniform")
        elif index == 1:
            self.ball_widget.simulation_engine.set_collision_method("kd")
