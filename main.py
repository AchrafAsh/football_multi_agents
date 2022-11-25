from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement, ModularServer, UserSettableParameter
from mesa.visualization.modules import ChartModule

from field import Field


class ContinuousCanvas(VisualizationElement):
    local_includes = [
        "./js/simple_continuous_canvas.js",
        "./js/jquery.js"
    ]

    def __init__(self, canvas_height=800,
                 canvas_width=800, instantiate=True):
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
        portrayal = self.portrayal_method(model.ball)
        if portrayal:
            portrayal["x"] = ((model.ball.x - model.space.x_min) /
                              (model.space.x_max - model.space.x_min))
            portrayal["y"] = ((model.ball.y - model.space.y_min) /
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
    chart = ChartModule([{"Label": "Shoots",
                          "Color": "Orange"}],
                        data_collector_name='datacollector')
    server = ModularServer(Field,
                           [ContinuousCanvas(), chart],
                           "Football game",
                           {"n_players": UserSettableParameter('slider', "Number of players", 5, 3, 10, 1),
                            "speed": UserSettableParameter('slider', "Speed", 50, 10, 200, 10)})
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    run_single_server()
