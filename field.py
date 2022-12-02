import math
import random
import uuid
import mesa
import mesa.space
import constants
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import BaseScheduler

from player import Player
from goalkeeper import GoalKeeper
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
                     "r": 4}
        return portrayal


class Field(Model):
    collector = DataCollector(
        model_reporters={
            "Shots": lambda model: model.shots,
            "Passes Team 1": lambda model: model.passes_1,
            "Passes Team 2": lambda model: model.passes_2,
            "Possession Team 1": lambda model: model.possession_1,
            "Possession Team 2": lambda model: model.possession_2,
        }, agent_reporters={})

    def __init__(self, n_players, speed, distance_to_buts_weight_attack, distance_to_buts_weight_defense, distance_to_adversary_weight_attack,
                 distance_to_adversary_weight_defense, distance_to_ball_weight_attack, distance_to_ball_weight_defense, 
                 distance_to_teammate_weight):
        width, height = constants.FIELD_SIZE, constants.FIELD_SIZE
        Model.__init__(self)
        self.space = mesa.space.ContinuousSpace(width, height, False)
        self.steps = 0
        self.shots = 0
        self.passes_1 = 0
        self.passes_2 = 0
        self.possession_1 = 0
        self.possession_2 = 0
        self.Goals = []
        self.distance_to_buts_weight_attack = distance_to_buts_weight_attack
        self.distance_to_buts_weight_defense = distance_to_buts_weight_defense
        self.distance_to_adversary_weight_attack = distance_to_adversary_weight_attack/n_players
        self.distance_to_adversary_weight_defense = distance_to_adversary_weight_defense/n_players
        self.distance_to_ball_weight_attack = distance_to_ball_weight_attack
        self.distance_to_ball_weight_defense = distance_to_ball_weight_defense
        self.distance_to_teammate_weight = distance_to_teammate_weight/n_players
        self.schedule = BaseScheduler(self)

        for _ in range(n_players):  # Loop on teams
            x, y = random.random() * width / 2, random.random() * height
            self.schedule.add(
                Player(int(uuid.uuid1()), self, x, y, speed, 1, random.random() * 2 * math.pi))
        for _ in range(n_players):  # Loop on teams
            x, y = (random.random() + 1) * width / 2, random.random() * height
            self.schedule.add(
                Player(int(uuid.uuid1()), self, x, y, speed, 2, random.random() * 2 * math.pi))

        self.schedule.add(GoalKeeper(uuid.uuid1(), self, 2, constants.FIELD_SIZE//2, speed, 1))
        self.schedule.add(GoalKeeper(uuid.uuid1(), self, constants.FIELD_SIZE - 2, constants.FIELD_SIZE//2, speed, 2))

        self.ball = Ball(int(uuid.uuid1()), self, constants.FIELD_SIZE//2, constants.FIELD_SIZE//2, 0)
        self.schedule.add(self.ball)

        self.Goals.append(Goal(0, height / 2 - constants.GOAL_SIZE //2))
        self.Goals.append(Goal(0, height / 2 + constants.GOAL_SIZE //2))
        self.Goals.append(Goal(width, height / 2 - constants.GOAL_SIZE //2))
        self.Goals.append(Goal(width, height / 2 + constants.GOAL_SIZE //2))

        self.datacollector = self.collector

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.steps += 1
        if (self.ball.x == 0 and (constants.FIELD_SIZE-constants.GOAL_SIZE)//2 < self.ball.y < (constants.GOAL_SIZE + constants.FIELD_SIZE)//2) \
            or (self.ball.x == constants.FIELD_SIZE and (constants.FIELD_SIZE - constants.GOAL_SIZE)//2 < self.ball.y < (constants.GOAL_SIZE + constants.FIELD_SIZE)//2):
            self.running = False
            
            print('%-12s%-12s%-12s' % ('Team', 'Possession', 'Passes'))
            print('%-12s%-12i%-12i' % ('1', self.possession_1, self.passes_1))
            print('%-12s%-12i%-12i' % ('2', self.possession_2, self.passes_2))
