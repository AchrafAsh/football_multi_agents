import random
import constants
import mesa
import mesa.space
from utils import go_to, move
import math
from ball import Ball


class Player(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed, team, angle=0.0):
        super().__init__(unique_id, model)
        self.team = team
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.counter = 0
        self.interception_zone = 10
        self.sight_distance = 200
        self.skills = {
            'dribbling': 0,
            'defending': 0,
            'intercepting': 0,
            'intercepting': 0,
        }

    def new_utility(self, x, y):
        score = 0
        for agent in self.model.schedule.agents:
            if isinstance(agent, Ball):
                score -= constants.DIST_JEU * abs(x - agent.x)
                if self.model.ball.player_with_the_ball and self.model.ball.player_with_the_ball.team == self.team:
                    if 20 < math.dist((x,y), (agent.x, agent.y)) < constants.SEUIL_DIST_BALL['attack']:
                        score += self.model.distance_to_ball_weight_attack * math.dist((x, y), (agent.x, agent.y))
                elif self.model.ball.player_with_the_ball:
                    if math.dist((x,y), (agent.x, agent.y)) < constants.SEUIL_DIST_BALL['defense']:
                        score -= self.model.distance_to_ball_weight_defense * math.dist((x, y), (agent.x, agent.y))

            else:
                if agent.team != self.team and math.dist((x, y), (agent.x, agent.y)) < self.sight_distance:
                    if self.model.ball.player_with_the_ball and self.model.ball.player_with_the_ball.team == self.team:
                        score += self.model.distance_to_adversary_weight_attack * math.dist((x, y), (agent.x, agent.y))
                    elif self.model.ball.player_with_the_ball and self.model.ball.player_with_the_ball.team != self.team:
                        score -= self.model.distance_to_adversary_weight_defense * math.dist((x, y), (agent.x, agent.y))

                if agent.team == self.team and math.dist((x, y), (agent.x, agent.y)) < self.sight_distance:
                    score += self.model.distance_to_teammate_weight * math.dist((x, y), (agent.x, agent.y))

        # Distance au but
        SEUIL_DIST_BUT = 5
        if self.model.ball.player_with_the_ball is not None:
            if self.model.ball.player_with_the_ball.team == self.team:
                # Player is in offense but does not have the ball: run towards the other goal (x=0 or 600)
                distance_to_goal = math.dist([x, y], [constants.FIELD_SIZE * (self.team%2), constants.FIELD_SIZE//2])
                if distance_to_goal > SEUIL_DIST_BUT:
                    score -= self.model.distance_to_buts_weight_attack * distance_to_goal
            elif self.model.ball.player_with_the_ball.team != self.team:
                # Player is in defense: run towards their goal
                distance_to_goal = math.dist([x, y], [constants.FIELD_SIZE * (self.team - 1), constants.FIELD_SIZE//2])
                if distance_to_goal > SEUIL_DIST_BUT:
                    score -= self.model.distance_to_buts_weight_defense * distance_to_goal
        return score

    def old_utility(self, x, y):
        score = 0
        for agent in self.model.schedule.agents:
            if isinstance(agent, Ball):
                score -= 2*math.dist([x, y], [agent.x,agent.y])
            elif self.model.ball.player_with_the_ball and agent.team != self.team and math.dist([x, y], [agent.x, agent.y]) < 100:
                # Attackers should stay away from defenders |??Defenders should stay close to attackers 
                coef = 0.5 if self.model.ball.player_with_the_ball.team == self.team else -2
                score += (math.dist([x, y], [agent.x, agent.y])-100)*coef
            elif agent.team == self.team and math.dist([x, y], [agent.x, agent.y]) < 100:
                # Teammates should stay away
                score += (math.dist([x, y], [agent.x, agent.y])-100)

        if self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team == self.team:
            # Player is in offense but does not have the ball: run towards the other goal (x=0 or 600)
            score -= math.dist([x, y], [constants.FIELD_SIZE * (self.team%2), constants.FIELD_SIZE//2])
        elif self.model.ball.player_with_the_ball is not None and self.model.ball.player_with_the_ball.team != self.team:
            # Player is in defense: run towards their goal
            score -= math.dist([x, y], [constants.FIELD_SIZE * (self.team - 1), constants.FIELD_SIZE//2])
        return score


    def step(self):
        self.counter = max(0, self.counter - 1)
        # If in range to shoot, shoot (to simple, may have to change later)
        if self.model.ball.player_with_the_ball == self:
            if self.team == 1 and math.dist([self.x, self.y], [constants.FIELD_SIZE, constants.FIELD_SIZE//2]) < 150:
                return self.shot(constants.FIELD_SIZE, constants.FIELD_SIZE//2)
            elif self.team == 2 and math.dist([self.x, self.y], [0, constants.FIELD_SIZE//2]) < 150:
                return self.shot(0, 300)

        # If nobody has the ball
        if not self.model.ball.player_with_the_ball and math.dist((self.x, self.y), (self.model.ball.x, self.model.ball.y)) < 200:
            if math.dist((self.x, self.y), (self.model.ball.x, self.model.ball.y)) < self.interception_zone:
                if random.random() * constants.BALL_SPEED > self.model.ball.speed:  # Max shoot speed is 100
                    self.model.ball.player_with_the_ball = self
                    self.counter = 3
            (self.x, self.y), self.angle = go_to(self.x, self.y, self.speed, self.model.ball.x, self.model.ball.y)
            return
       
        # If the player doesn't have the ball, he can intercept it or still it from a player from the other team
        if math.dist([self.x, self.y], [self.model.ball.x, self.model.ball.y]) < self.interception_zone and \
        self.model.ball.player_with_the_ball.team != self.team:
            if random.random() > constants.STEAL_BALL_PROB:
                self.model.ball.player_with_the_ball = self

        # The player is moving to the new position that increase his utility
        # utility = self.new_utility if self.team == 1 else self.old_utility
        utility = self.new_utility
        # utility = self.old_utility
        max_utility = utility(self.x, self.y)
        max_utility_x, max_utility_y, max_utility_angle = self.x, self.y, self.angle
        angle = self.angle
        for i in range(10):  # Try 10 different way to move, pick out the best one
            x, y = move(self.x, self.y, self.speed, angle)
            if 0 < x < constants.FIELD_SIZE and 0 < y < constants.FIELD_SIZE and utility(x, y) > max_utility:
                max_utility = utility(x, y)
                max_utility_x, max_utility_y, max_utility_angle = x, y, angle
            angle = math.pi * random.random() * 2
        self.x, self.y, self.angle = max_utility_x, max_utility_y, max_utility_angle
        
        # If the player has the ball, he can make a pass according to the utility of his teammates
        if self.model.ball.player_with_the_ball == self:
            ally_utility = []
            ally_position = []
            for player in self.model.schedule.agents:
                
                if isinstance(player, Player) and player.team == self.team and player is not self:
                    ally_position.append([player.x, player.y])
                    ally_utility.append(utility(player.x, player.y))

            if max(ally_utility) > max_utility + 10:
                # Pass the ball
                
                # Reporters
                if self.model.ball.player_with_the_ball.team == 1:
                    self.model.passes_1 += 1
                if self.model.ball.player_with_the_ball.team == 2:
                    self.model.passes_2 += 1
                
                self.model.ball.player_with_the_ball = None
                i = ally_utility.index(max(ally_utility))
                self.model.ball.speed = min(constants.BALL_SPEED,
                    int(math.dist([self.x, self.y],[ally_position[i][0], ally_position[i][1]])//2 + 10))
                self.model.ball.angle = math.atan2(self.y - ally_position[i][1],
                                                   self.x - ally_position[i][0]) + math.pi

    def shot(self, x, y):
        self.model.ball.player_with_the_ball = None
        self.model.ball.speed = constants.BALL_SPEED
        self.model.ball.angle = math.atan2(self.y - random.gauss(y, 15),
                                            self.x - x) + math.pi
        self.model.shots += 1

    def portrayal_method(self):
        Color = ["Red", "Blue"]
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": Color[self.team - 1], "Layer": 3,
                     'x': self.x,
                     'y': self.y, "angle": self.angle}
        return portrayal
