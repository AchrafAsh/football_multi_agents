import mesa
from agent import MovingAgent
from utils import move

class Ball(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.model, x, y, speed):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.speed = speed
        self.free = True  # True if no one has the ball
        self.angle = 0

    def portrayal_method(self):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "black",
                     "r": 5}
        return portrayal

    def step(self):
        if self.free:
            self.x, self.y = move(self.x, self.y, self.speed, self.angle)
            self.speed = max(self.speed - 10, 0)
            if self.x < 0:
                self.x = 0
            if self.y < 0:
                self.y = 0
            if self.y > 600:
                self.y = 600
            if self.x > 600:
                self.x = 600


