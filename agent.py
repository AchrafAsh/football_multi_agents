import mesa

class MovingAgent(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, x, y, speed=0):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.speed = speed
