import mesa
import mesa.space


# from utils import distance

class Player(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, team, angle=0.0):
        super().__init__(unique_id, model)
        self.team = team
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.skills = {
            'dribbling': 0,
            'defending': 0,
            'intercepting': 0,
            'intercepting': 0,
        }

    def step(self):
        pass

    def portrayal_method(self):
        Color = ["Red", "Blue"]
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": Color[self.team-1], "Layer": 3, 'x': self.x,
                     'y': self.y, "angle": self.angle}
        return portrayal
