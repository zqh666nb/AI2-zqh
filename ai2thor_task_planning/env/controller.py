from ai2thor.controller import Controller
from config import SCENE, GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT

class ThorController:

    def __init__(self):

        self.controller = Controller(
            scene=SCENE,
            agentMode="default",
            visibilityDistance=1.5,
            gridSize=GRID_SIZE,
            snapToGrid=True,
            rotateStepDegrees=90,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )

    def step(self, action, **kwargs):

        event = self.controller.step(
            action=action,
            **kwargs
        )

        return event

    def get_event(self):
        return self.controller.last_event
