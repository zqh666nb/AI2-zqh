import time
from config import STEP_DELAY


class ActionExecutor:

    def __init__(self, env):

        self.env = env

    def step(self, action, params=None):

        if params is None:

            params = {}

        print("执行:", action)

        event = self.env.step(action, **params)

        if STEP_DELAY and STEP_DELAY > 0:

            time.sleep(STEP_DELAY)

        return event

    def execute(self, plan, stop_on_failure: bool = True):

        for action, params in plan:

            event = self.step(action, params)

            if not event.metadata["lastActionSuccess"]:

                print("动作失败:", action)

                if stop_on_failure:

                    break

