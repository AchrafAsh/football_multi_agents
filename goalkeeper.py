import random
import constants
import mesa
import mesa.space
from utils import go_to, move
import math
from ball import Ball
from player import Player


class GoalKeeper(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, team):
        super().__init__(unique_id, model)
        self.team = team
        self.x = x
        self.y = y
        self.speed = speed
        self.interception_zone = 20
        self.counter = 0
        
    def player_utility(self, x, y):
        score = 100
        for agent in self.model.schedule.agents:
            if isinstance(agent, Ball):
                score -= math.dist([x, y], [agent.x,agent.y])
            elif agent == self and agent.team != self.team and math.dist([x, y], [agent.x, agent.y]) < 100:
                coef = 1 if self.model.ball.player_with_the_ball.team == self.team else -1
                score += (math.dist([x, y], [agent.x, agent.y]) - 100) * coef
            elif agent.team == self.team and math.dist([x, y], [agent.x, agent.y]) < 100:
                score += math.dist([x, y], [agent.x, agent.y]) - 100

        if self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team == self.team:
            # Player is in offense but does not have the ball: run towards the other goal (x=0 or 600)
            score -= math.dist([x, y], [constants.FIELD_SIZE * (self.team%2), constants.FIELD_SIZE//2])
        elif self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team != self.team:
            # Player is in defense: run towards their goal
            score -= math.dist([x, y], [constants.FIELD_SIZE * (self.team - 1), constants.FIELD_SIZE//2])
        return score


    def step(self):
        self.counter = max(0, self.counter - 1)

        if self.model.ball.y < constants.FIELD_SIZE // 2:
            (self.x, self.y), _ = go_to(self.x, self.y, self.speed, self.x, max((constants.FIELD_SIZE - constants.GOAL_SIZE) // 2 + 10, self.model.ball.y))
        else:
            (self.x, self.y), _ = go_to(self.x, self.y, self.speed, self.x, min((constants.FIELD_SIZE + constants.GOAL_SIZE) // 2 - 10, self.model.ball.y))

        # If the player doesn't have the ball, he can intercept it or still it from a player from the other team
        next_ball_position = list(move(self.model.ball.x, self.model.ball.y, self.model.ball.speed, self.model.ball.angle))
        next_ball_position[0] = min(max(next_ball_position[0], 0), constants.FIELD_SIZE)
        if math.dist([self.x, self.y], next_ball_position) < self.interception_zone:
            if self.model.ball.player_with_the_ball is None:
                # if (random.random() * 2) > self.model.ball.speed / constants.BALL_SPEED:  # Max shoot speed is 100
                if random.random() < 0.9:
                    self.model.ball.player_with_the_ball = self
                    self.counter = 10
            elif self.model.ball.player_with_the_ball.team != self.team:
                if random.random() > constants.STEAL_BALL_PROB:
                    self.model.ball.player_with_the_ball = self
                    self.counter = 10

        # If the player has the ball, he can make a pass according to the utility of his teammates
        if self.model.ball.player_with_the_ball == self and self.counter == 0:
            ally_utility = []
            ally_position = []
            for player in self.model.schedule.agents:
                if isinstance(player, Player) and player.team == self.team and player is not self:
                    ally_position.append([player.x, player.y])
                    ally_utility.append(self.player_utility(player.x, player.y))

            self.model.ball.player_with_the_ball = None
            i = ally_utility.index(max(ally_utility))
            self.model.ball.speed = min(constants.BALL_SPEED, int(math.dist([self.x, self.y],
                                                            [ally_position[i][0], ally_position[i][1]]) + 10))
            self.model.ball.angle = math.atan2(self.y - ally_position[i][1],
                                                self.x - ally_position[i][0]) + math.pi
            self.model.passes += 1


    def portrayal_method(self):
        Color = ["Red", "Blue"]
        portrayal = {"Shape": "circle", "Filled": "true", "Color": Color[self.team - 1], "Layer": 3, "r": 5}
                    #  'x': self.x,
                    #  'y': self.y}
        return portrayal
