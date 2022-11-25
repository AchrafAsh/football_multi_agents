import math
import random
import uuid
import mesa
import mesa.space

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from player import Player
from ball import Ball


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def portrayal_method(self):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "black",
                     "r": 10}
        return portrayal


class Field(Model):
    collector = DataCollector(
        model_reporters={
            # "Mines": lambda model: len(model.mines),
            # "Danger markers": lambda model: len([m for m in model.markers if m.purpose == MarkerPurpose.DANGER]),
            # "Indication markers": lambda model: len([m for m in model.markers if m.purpose == MarkerPurpose.INDICATION]),
        }, agent_reporters={})

    def __init__(self, n_players, speed):
        width, height = 600, 600
        Model.__init__(self)
        self.space = mesa.space.ContinuousSpace(width, height, False)
        self.steps = 0
        self.Goals = []
        self.schedule = RandomActivation(self)

        for _ in range(n_players):  # Loop on teams
            x, y = random.random() * width / 2, random.random() * height
            self.schedule.add(
                Player(int(uuid.uuid1()), self, x, y, speed, 1, random.random() * 2 * math.pi))
        for _ in range(n_players):  # Loop on teams
            x, y = (random.random() + 1) * width / 2, random.random() * height
            self.schedule.add(
                Player(int(uuid.uuid1()), self, x, y, speed, 2, random.random() * 2 * math.pi))

        self.ball = Ball(int(uuid.uuid1()), self, 300, 300, 0)
        self.schedule.add(self.ball)

        self.Goals.append(Goal(0, height / 2 - 50))
        self.Goals.append(Goal(0, height / 2 + 50))
        self.Goals.append(Goal(width, height / 2 - 50))
        self.Goals.append(Goal(width, height / 2 + 50))

        self.datacollector = self.collector

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.steps += 1
        if (self.ball.x == 0 and 250 < self.ball.y < 350) or (self.ball.x == 600 and 250 < self.ball.y < 350):
            self.running = False
