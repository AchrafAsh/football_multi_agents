import random

import mesa
import mesa.space
from utils import go_to, move
import math
from ball import Ball

STILL_BALL_PROBABILITY = 0.2


# from utils import distance

class Player(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, team, angle=0.0):
        super().__init__(unique_id, model)
        self.team = team
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.interception_zone = 20
        self.skills = {
            'dribbling': 0,
            'defending': 0,
            'intercepting': 0,
            'intercepting': 0,
        }

    def position_utility(self, x, y):
        score = 1000
        for agent in self.model.schedule.agents:
            if agent != self:
                if isinstance(agent, Ball):
                    score -= math.dist([x, y], [agent.x,agent.y])
                elif agent.team == self.team:
                    if math.dist([x, y], [agent.x, agent.y]) < 100:
                        score += math.dist([x, y], [agent.x, agent.y]) - 100

        if self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team == self.team:
            score -= math.dist([x, y], [600 * (self.team%2), 300]) # Run toward the other goal (in x=0 or 600)
        elif self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team != self.team:
            score -= math.dist([x, y], [600 * (self.team - 1), 300])  # Run toward the other goal (in x=0 or 600)
        return score

    def step(self):
        # The player is moving to the new position that increase his utility
        max_utility = self.position_utility(self.x, self.y)
        max_utility_x, max_utility_y, max_utility_angle = self.x, self.y, self.angle
        angle = self.angle
        for i in range(10):  # Try 10 different way to move, pick out the best one
            x, y = move(self.x, self.y, self.speed, angle)
            if 0 < x < 600 and 0 < y < 600 and self.position_utility(x, y) > max_utility:
                max_utility = self.position_utility(x, y)
                max_utility_x, max_utility_y, max_utility_angle = x, y, angle
            angle = math.pi * random.random() * 2
        self.x, self.y, self.angle = max_utility_x, max_utility_y, max_utility_angle

        # If the player doesn't have the ball, he can intercept it or still it from a player from the other team
        if math.dist([self.x, self.y], [self.model.ball.x, self.model.ball.y]) < self.interception_zone:
            if self.model.ball.player_with_the_ball is None:
                if random.random() * 100 > self.model.ball.speed:  # Max shoot speed is 100
                    self.model.ball.player_with_the_ball = self
            elif self.model.ball.player_with_the_ball.team != self.team:
                if random.random() > STILL_BALL_PROBABILITY:
                    self.model.ball.player_with_the_ball = self

        # If in range to shoot, shoot (to simple, may have to change later)
        if self.model.ball.player_with_the_ball == self:
            if self.team == 1 and math.dist([self.x, self.y], [600, 300]) < 150:
                self.model.ball.player_with_the_ball = None
                self.model.ball.speed = 200
                self.model.ball.angle = math.atan2(self.y - 300,
                                                   self.x - 600) + math.pi
            elif self.team == 2 and math.dist([self.x, self.y], [0, 300]) < 150:
                self.model.ball.player_with_the_ball = None
                self.model.ball.speed = 200
                self.model.ball.angle = math.atan2(self.y - 300,
                                                   self.x - 0) + math.pi

        # If the player has the ball, he can make a pass according to the utility of his teammates
        if self.model.ball.player_with_the_ball == self:
            ally_utility = []
            ally_position = []
            for player in self.model.schedule.agents:
                if isinstance(player, Player) and player.team == self.team and player is not self:
                    ally_position.append([player.x, player.y])
                    ally_utility.append(self.position_utility(player.x, player.y))

            if max(ally_utility) > max_utility + 100:
                self.model.ball.player_with_the_ball = None
                i = ally_utility.index(max(ally_utility))
                self.model.ball.speed = min(200, int(math.dist([self.x, self.y],
                                                               [ally_position[i][0], ally_position[i][1]]) + 10))
                self.model.ball.angle = math.atan2(self.y - ally_position[i][1],
                                                   self.x - ally_position[i][0]) + math.pi

    def portrayal_method(self):
        Color = ["Red", "Blue"]
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": Color[self.team - 1], "Layer": 3,
                     'x': self.x,
                     'y': self.y, "angle": self.angle}
        return portrayal
