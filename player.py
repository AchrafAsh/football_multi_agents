import mesa
import mesa.space
from utils import distance

class Player(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, sight_distance, team_color:str, angle=0.0):
        super().__init__(unique_id, model)
        self.team_color = team_color
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.sight_distance = sight_distance
        self.skills = {
            'dribbling': 0,
            'defending': 0,
            'intercepting': 0,
            'intercepting': 0,
        }

    def step(self):
       pass

    def portrayal_method(self):
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": "Red", "Layer": 3, 'x': self.x,
                     'y': self.y, "angle": self.angle}
        return portrayal