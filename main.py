import constants
from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement, ModularServer, UserSettableParameter
from mesa.visualization.modules import ChartModule

from field import Field


class ContinuousCanvas(VisualizationElement):
    local_includes = [
        "./js/football_field.js",
        "./js/jquery.js"
    ]

    def __init__(self, canvas_height=600,
                 canvas_width=600, instantiate=True):
        VisualizationElement.__init__(self)
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.identifier = "space-canvas"
        if (instantiate):
            new_element = ("new Simple_Continuous_Module({}, {},'{}')".
                           format(self.canvas_width, self.canvas_height, self.identifier))
            self.js_code = "elements.push(" + new_element + ");"

    def portrayal_method(self, obj):
        return obj.portrayal_method()

    def render(self, model):
        representation = defaultdict(list)
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            if portrayal:
                portrayal["x"] = ((obj.x - model.space.x_min) /
                                  (model.space.x_max - model.space.x_min))
                portrayal["y"] = ((obj.y - model.space.y_min) /
                                  (model.space.y_max - model.space.y_min))
            representation[portrayal["Layer"]].append(portrayal)
        for obj in model.Goals:
            portrayal = self.portrayal_method(obj)
            if portrayal:
                portrayal["x"] = ((obj.x - model.space.x_min) /
                                  (model.space.x_max - model.space.x_min))
                portrayal["y"] = ((obj.y - model.space.y_min) /
                                  (model.space.y_max - model.space.y_min))
            representation[portrayal["Layer"]].append(portrayal)
        return representation


def run_single_server():
    chart = ChartModule([
        {"Label": "Shots", "Color": "Orange"},
        {"Label": "Passes", "Color": "Red"}
        ], data_collector_name='datacollector')
    server = ModularServer(Field,
                           [ContinuousCanvas(constants.FIELD_SIZE, constants.FIELD_SIZE), chart],
                           "Football game",
                           {"n_players": UserSettableParameter('slider', "Number of players", 7, 3, 11, 2),
                            "speed": UserSettableParameter('slider', "Speed", 2, 2, 10, 2),
                            "distance_to_buts_weight_attack": UserSettableParameter('slider', "Weight of but distance in attack mode", 10, 0, 20, 2),
                            "distance_to_buts_weight_defense": UserSettableParameter('slider', "Weight of but distance in defense mode", 1, 0, 20 , 2),
                            "distance_to_adversary_weight_attack": UserSettableParameter('slider', "Weight of adversaries distance in attack mode", 0.2, 0, 20, 2),
                            "distance_to_adversary_weight_defense": UserSettableParameter('slider', "Weight of adversaries distance in defense mode", 0.8, 0, 20, 2),
                            "distance_to_ball_weight_attack": UserSettableParameter('slider', "Weight of ball distance in attack mode", 0.2, 0, 20, 2),
                            "distance_to_ball_weight_defense": UserSettableParameter('slider', "Weight of ball distance in defense mode", 0.8, 0, 20, 2),
                            "distance_to_teammate_weight": UserSettableParameter('slider', "Weight of teammates distance", 0.5, 0, 20, 2)
                            })
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    run_single_server()
