class ActionExecutor:

    def __init__(self, env):

        self.env = env

    def execute(self, plan):

        for action, params in plan:

            print("执行:", action)

            event = self.env.step(action, **params)

            if not event.metadata["lastActionSuccess"]:

                print("动作失败:", action)

                break
