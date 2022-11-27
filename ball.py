import mesa
from agent import MovingAgent
from utils import move

class Ball(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.model, x, y, speed):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.speed = speed
        self.player_with_the_ball = None  # True if no one has the ball
        self.angle = 0

    def portrayal_method(self):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 3,
                     "Color": "green",
                     "r": 5}
        return portrayal

    def step(self):
        if self.player_with_the_ball is None:
            self.x, self.y = move(self.x, self.y, self.speed, self.angle)
            self.speed = int(self.speed / 2)
            if self.x < 0:
                self.x = 0
            if self.y < 0:
                self.y = 0
            if self.y > 600:
                self.y = 600
            if self.x > 600:
                self.x = 600
        else:
            self.speed = 0
            self.x, self.y = self.player_with_the_ball.x, self.player_with_the_ball.y


