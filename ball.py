import mesa
import constants
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
                     "Color": "orange",
                     "r": 5}
        return portrayal

    def step(self):
        if self.player_with_the_ball is None:
            self.x, self.y = move(self.x, self.y, self.speed, self.angle)
            self.speed = int(self.speed / 2)
            self.x = min(max(self.x, 0), constants.FIELD_SIZE)
            self.y = min(max(self.y, 0), constants.FIELD_SIZE)
        else:
            self.speed = 0
            self.x, self.y = self.player_with_the_ball.x, self.player_with_the_ball.y
            # Reporters
            if self.player_with_the_ball.team == 1:
                self.model.possession_1 += 1
            if self.player_with_the_ball.team == 2:
                self.model.possession_2 += 1


