from ai2thor.controller import Controller
from config import SCENE, GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT


class SceneManager:

    def __init__(self):

        self.controller = Controller(
            scene=SCENE,
            gridSize=GRID_SIZE,
            snapToGrid=True,
            rotateStepDegrees=90,
            visibilityDistance=1.5,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )

    def reset_scene(self):

        print("Resetting scene:", SCENE)

        self.controller.reset(scene=SCENE)

        return self.controller.last_event

    def randomize_scene(self):

        print("Randomizing objects")

        event = self.controller.step(
            action="InitialRandomSpawn",
            randomSeed=123
        )

        return event

    def get_controller(self):

        return self.controller

