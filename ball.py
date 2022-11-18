import mesa

class Ball(mesa.Agent):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0

    def portrayal_method(self):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "white",
                     "r": 2}
        return portrayal