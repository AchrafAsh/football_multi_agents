import mesa


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 0

    def portrayal_method(self):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "black",
                     "r": 5}
        return portrayal
