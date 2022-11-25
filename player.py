import random

import mesa
import mesa.space
from utils import go_to, move
import math


# from utils import distance

class Player(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, team, angle=0.0):
        super().__init__(unique_id, model)
        self.team = team
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.has_ball = False
        self.interception_zone = 10
        self.skills = {
            'dribbling': 0,
            'defending': 0,
            'intercepting': 0,
            'intercepting': 0,
        }

    def position_utility(self, x, y):
        return x + y

    def step(self):
        max_utility = self.position_utility(self.x, self.y)
        max_utility_x, max_utility_y, max_utility_angle = self.x, self.y, self.angle
        angle = self.angle
        for i in range(10):  # Try 10 different way to move, pick out the best one
            x, y = move(self.x, self.y, self.speed, angle)
            if x < 0 or y < 0 or x > 600 or y > 600:
                continue
            elif self.position_utility(x, y) > max_utility:
                max_utility = self.position_utility(x, y)
                max_utility_x, max_utility_y, max_utility_angle = x, y, angle
            angle = math.pi * random.random() * 2
        self.x, self.y, self.angle = max_utility_x, max_utility_y, max_utility_angle

        if self.has_ball:
            ally_utility = []
            for player in self.model.schedule:
                if player.team == self.team:
                    ally_utility.append(self.position_utility(player.x, player.y))

            if ally_utility.max() > max_utility:
                pass  # Il faut tirer

    def portrayal_method(self):
        Color = ["Red", "Blue"]
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": Color[self.team - 1], "Layer": 3,
                     'x': self.x,
                     'y': self.y, "angle": self.angle}
        return portrayal
