class KitchenTasks:

    def __init__(self, planner):

        self.planner = planner

    def task_get_object(self):

        plan = []

        plan += self.planner.plan_open_cabinet()

        plan += self.planner.plan_find_object()

        return plan

    def task_place_object(self):

        plan = []

        plan += self.planner.plan_place()

        return plan
